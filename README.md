# Attendance_System-using-facial-recognition

This program is written in Python language. I have used facial recogition to mark attendance of students. Haarcascade classifier method is used to train the captured images for new student signup. LBPH face recognizer function is used to recognize the registered faces for marking the attendance in a csv file. I have used tkinter library to create a GUI for Attendanca System.

Flow of System:
1. If already registered, fill up login details and mark attendance.
2. If not registered, click on signup and register yourself. To register, fill up given fields, click on Take Images. After completion click on Train Images. All the details will be stored in Student Details.csv file.
3. Then return to main menu.
4. Login with newly created credentials.
5. Mark the attendance. Exit the camera by pressing esc button
