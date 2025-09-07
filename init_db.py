import sqlite3

DB = "events.db"

schema = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS colleges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  college_id INTEGER,
  title TEXT NOT NULL,
  description TEXT,
  event_type TEXT,
  start_time TEXT,
  end_time TEXT,
  capacity INTEGER,
  is_cancelled INTEGER DEFAULT 0,
  FOREIGN KEY(college_id) REFERENCES colleges(id)
);

CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  college_id INTEGER,
  name TEXT,
  email TEXT UNIQUE,
  roll_no TEXT,
  phone TEXT,
  FOREIGN KEY(college_id) REFERENCES colleges(id)
);

CREATE TABLE IF NOT EXISTS registrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  student_id INTEGER,
  status TEXT DEFAULT 'registered',
  UNIQUE(event_id, student_id),
  FOREIGN KEY(event_id) REFERENCES events(id),
  FOREIGN KEY(student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS attendance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  student_id INTEGER,
  method TEXT,
  UNIQUE(event_id, student_id),
  FOREIGN KEY(event_id) REFERENCES events(id),
  FOREIGN KEY(student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id INTEGER,
  student_id INTEGER,
  rating INTEGER,
  comment TEXT,
  FOREIGN KEY(event_id) REFERENCES events(id),
  FOREIGN KEY(student_id) REFERENCES students(id)
);
"""

seed = """
INSERT OR IGNORE INTO colleges (id, name) VALUES (1, 'Demo College');

INSERT OR IGNORE INTO events (id, college_id, title, event_type, start_time, end_time, capacity)
VALUES
  (1, 1, 'Tech Workshop', 'Workshop', '2025-09-10T10:00', '2025-09-10T13:00', 100),
  (2, 1, 'Campus Fest', 'Fest', '2025-09-15T09:00', '2025-09-15T18:00', 500);

INSERT OR IGNORE INTO students (id, college_id, name, email, roll_no, phone)
VALUES
  (1, 1, 'Aaryav Sharma', 'aaryav@example.com', 'B21CS001', '9999000001'),
  (2, 1, 'Shivani Gupta', 'shivani@example.com', 'B21IT002', '9999000002');

INSERT OR IGNORE INTO registrations (id, event_id, student_id)
VALUES (1, 1, 1);

INSERT OR IGNORE INTO attendance (id, event_id, student_id, method)
VALUES (1, 1, 1, 'manual');

INSERT OR IGNORE INTO feedback (id, event_id, student_id, rating, comment)
VALUES (1, 1, 1, 5, 'Great event!');
"""

def main():
    conn = sqlite3.connect(DB)
    conn.executescript(schema)
    conn.executescript(seed)
    conn.close()
    print("Database initialized with sample data.")

if __name__ == "__main__":
    main()
