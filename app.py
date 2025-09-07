from flask import Flask, request, jsonify, g
import sqlite3

DB = "events.db"
app = Flask(__name__)

# -----------------
# Database helpers
# -----------------
def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

def row_to_dict(row):
    return {k: row[k] for k in row.keys()}

# -----------------
# Test Route
# -----------------
@app.route("/hello")
def hello():
    return "Hello, Flask is working!"

# -----------------
# List events
# -----------------
@app.route("/events", methods=["GET"])
def events():
    db = get_db()
    rows = db.execute("SELECT * FROM events WHERE is_cancelled=0").fetchall()
    return jsonify([row_to_dict(r) for r in rows])

# -----------------
# Register for event
# -----------------
@app.route("/events/<int:event_id>/register", methods=["POST"])
def register(event_id):
    student = request.json.get("student", {})
    email = student.get("email")
    name = student.get("name")

    db = get_db()
    cur = db.cursor()

    # Check if student exists
    cur.execute("SELECT id FROM students WHERE email=?", (email,))
    row = cur.fetchone()
    if row:
        sid = row["id"]
    else:
        cur.execute(
            "INSERT INTO students (college_id,name,email) VALUES (1,?,?)",
            (name, email),
        )
        sid = cur.lastrowid

    # Register for event
    try:
        cur.execute("INSERT INTO registrations (event_id,student_id) VALUES (?,?)", (event_id, sid))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "already registered"}), 400

    return jsonify({"status": "registered", "student_id": sid})

# -----------------
# Mark attendance
# -----------------
@app.route("/events/<int:event_id>/attendance", methods=["POST"])
def attendance(event_id):
    email = request.json.get("student_email")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM students WHERE email=?", (email,))
    s = cur.fetchone()
    if not s:
        return jsonify({"error": "student not found"}), 404

    try:
        cur.execute(
            "INSERT INTO attendance (event_id,student_id,method) VALUES (?,?,?)",
            (event_id, s["id"], "manual"),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "attendance already marked"}), 400

    return jsonify({"status": "checked_in"})

# -----------------
# Feedback
# -----------------
@app.route("/events/<int:event_id>/feedback", methods=["POST"])
def feedback(event_id):
    email = request.json.get("student_email")
    rating = request.json.get("rating")
    comment = request.json.get("comment", "")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM students WHERE email=?", (email,))
    s = cur.fetchone()
    if not s:
        return jsonify({"error": "student not found"}), 404

    cur.execute(
        "INSERT INTO feedback (event_id,student_id,rating,comment) VALUES (?,?,?,?)",
        (event_id, s["id"], rating, comment),
    )
    db.commit()
    return jsonify({"status": "feedback_saved"})

# -----------------
# Reports: popularity
# -----------------
@app.route("/reports/event_popularity", methods=["GET"])
def popularity():
    db = get_db()
    rows = db.execute("""
        SELECT e.title, COUNT(r.id) AS registrations
        FROM events e
        LEFT JOIN registrations r ON e.id = r.event_id
        GROUP BY e.id
        ORDER BY registrations DESC
    """).fetchall()
    return jsonify([row_to_dict(r) for r in rows])
# Report: Top students by attendance
@app.route("/reports/top_students", methods=["GET"])
def report_top_students():
    limit = int(request.args.get("limit", 5))  # default top 5
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
      SELECT s.id, s.name, s.email, COUNT(a.id) AS attended_count
      FROM students s
      JOIN attendance a ON s.id = a.student_id
      GROUP BY s.id
      ORDER BY attended_count DESC
      LIMIT ?
    """,
        (limit,),
    )
    rows = cur.fetchall()
    return jsonify([row_to_dict(r) for r in rows])
# -----------------
# Main entry
# -----------------
if __name__ == "__main__":
    app.run(debug=True)

