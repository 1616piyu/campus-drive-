# campus-drive-

TOIPIC IS Campus Event Management 
This project is create to manage college events,workshops etc. 
  1.By creating this admins can create events(workshops,hackathons,fests).
  2.Students can register, attend and give feedback.
  3.Reports shows event popularity, participation of student there attendance and top students. 
  
#Main use of project
  This project is built to conduct events ,tracking registrations ,attendance and  collect           feedback.

  #How to run 
   python app/app.py
   Open browser : http://127.0.0.1:5000
   Open Browser and run it : 1. For Test the Hello route :http://127.0.0.1:5000/hello
                             2. For Events               :http://127.0.0.1:5000/events

    Output of this :  Hello, Flask is working!

   #Main API'S  

   GET /events/  = List all events    
   POST /students/register = Register student to event
   POST /attendance/ = Mark attendance
   POST /feedback/ = Submit feedback
   GET /reports/event_popularity = Most popular events
   GET /reports/student_participation = Student participation
   GET /reports/top_students = Top 3 active students                

   We also add all the documents and other essentiual things which need for the completion of project. 
        <img width="641" height="201" alt="ER_ Diagram" src="https://github.com/user-attachments/assets/e2c5fdec-d967-462c-9ff6-2f1f056240ec" />
        

   
   
