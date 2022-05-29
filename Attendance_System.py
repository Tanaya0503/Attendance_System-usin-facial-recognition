import cv2
import csv
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os
import numpy as np
import datetime as dt
import time




#Main window
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, bg='black')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry('1600x1600')
        self.frames = {}

        for F in (HomePage, SignUpPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




   #********************  Take Images  *******************
    def TakeImages(a, txt1, txt2):

        cam = cv2.VideoCapture(0)  #initializing camera

        id = int(txt1.get())
        name = (txt2.get())

        # face_detector is a classifier that detects a face since it has haarcascade features loaded onto it
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        print('Camera Opening. Focus On Camera')

        count = 0

        while True:

            # reading camera img and converting it to gray img
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # detectMultiScale is a pre-defined fun that helps us to find the features/loc of the grey img
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # putting the face imgs in TrainingImages folder
                # cv2.imwrite(filename, image)-->syntax of imwrite
                cv2.imwrite('Training Images/Users.' + str(id) + '.' + str(count) + '.jpg', gray[y:y + h, x:x + w])

                count = count + 1
                cv2.imshow('Video Capture', img)

            if count >= 50:
                break
            k=cv2.waitKey(100) & 0xff
            if k==27:
                break
        cam.release()
        cv2.destroyAllWindows()

        # Make entry of the user into UserDetails.csv
        row = [id, name]

        with open(r'Student Details.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)

            writer.writerow(row)
        csvFile.close()

        #**********  Train Images  **************

    def TrainImages(a):

        path = 'Training Images'
        # LBPH is a face recognition algo that extracts image info and performs the matching
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        faces = []
        ids = []

        # func for getting the labels/id corr to each image
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                # Images are converted into Numpy Array in height, width, channel format
                img_numpy = np.array(PIL_img, 'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces.append(img_numpy)
                ids.append(id)

            return faces, ids

        print("Training faces. Wait a few seconds ...")
        faces, ids = getImagesAndLabels(path)
        # Saving the trained faces and their respective ID's
        # in a model named as "trainer.yml".
        recognizer.train(faces, np.array(ids))
        recognizer.save('Trainer.yml')
        print("Number of faces trained : ", format(len(np.unique(ids))))

    #************  Mark Attendance ************

    def Attendance(a):
        i = 1

        # This fun returns the name of the user by matching it with the id
        def UserDetails(id):
            i = 0
            f = open('Student Details.csv')
            csv_f = csv.reader(f)
            for row in csv_f:
                for col in row:
                    if(col == str(id)):
                        i = 1
                        continue
                    if(i == 1):
                        return col

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('Trainer.yml')
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        font = cv2.FONT_HERSHEY_SIMPLEX

        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            for(x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                if (confidence < 75):
                    ts = time.time()
                    date = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = dt.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                    id1 = id
                    id = str(id) + ' ' + UserDetails(id)
                    confidence = "  {0}%".format(round(100 - confidence))
                    if (i == 1):
                        row = [id1, UserDetails(id1), date, timeStamp]
                        with open(r"Attendance Report.csv", 'a+') as csvFile:
                            writer = csv.writer(csvFile)
                            # Entry of the row in csv file
                            writer.writerow(row)
                        csvFile.close()
                        i = i + 1
                else:
                    id = "Unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cv2.imshow('Camera', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()


# ***************  GUI For Homepage *******************
class HomePage(tk.Frame):


    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,)

        #adding background image
        self.image = Image.open("Icons/Background.png")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)


        #display current date and time
        def tick():
            time_string = time.strftime('%H:%M:%S')
            clock.config(text=time_string)
            clock.after(200, tick)
            date = dt.datetime.now()
            format_date = f"{date:%a, %b %d, %Y}"
            label = Label(self, text=format_date,fg="grey1", bg="SpringGreen2", width=15, height=1, font=('times', 22, ' bold '))
            label.place(x=250,y=240)

        clock = tk.Label(self, fg="grey1", bg="SpringGreen2", width=10, height=1, font=('times', 22, ' bold '))
        clock.pack(fill='both', expand=1)
        clock.place(x=600, y=240)
        tick()


        #defining labels and entry fields
        msg = tk.Label(
            self, text="Attendance System",bg='yellow',
            fg="grey1", width=55,
            height=3, font=('times', 30, 'bold'))
        msg.place(x=20, y=20)


        lbl3 = tk.Label(self, text="Login", bg='peachpuff',
                        width=20, height=1,
                        font=('times', 30, ' bold '))
        lbl3.place(x=300, y=170)

        lbl1 = tk.Label(self, text="Roll No. : ",bg='ivory3',fg="grey1",
                        width=20, height=1,
                         font=('times', 20, ' bold '))
        lbl1.place(x=230, y=300)

        txt1 = tk.Entry(self,
                        width=20, bg="white",
                        fg="grey1", font=('times', 20, ' bold '))
        txt1.place(x=570, y=300)

        lbl2 = tk.Label(self, text="Name : ", bg = 'ivory3',
                        width=20, fg="grey1",
                        height=1, font=('times', 20, ' bold '))

        lbl2.place(x=230, y=380)

        txt2 = tk.Entry(self, width=20,
                        bg="white", fg="grey1",
                        font=('times', 20, ' bold '))
        txt2.place(x=570, y=380)

        lbl = tk.Label(self,
                       text="Instructions: For new registrations click on Sign Up otherwise mark the corresponding attendance",
                       width=100, fg="grey1", bg="white",
                       height=2, font=('times', 15, ' bold '))
        lbl.place(x=75, y=600)

        #adding image for homepage
        img=Image.open("Icons/Attendance_icon.png")
        img=img.resize((500,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self,image=self.photoimg)
        f_lbl.place(x=900,y=200,height=250,width=450)




        #defining buttons
        Attendance = tk.Button(self, text="Mark Attendance ",
                                      command=lambda:controller.Attendance(), fg="grey1", bg='yellow2',
                                      width=20, height=1, activebackground="Red",
                                      font=('times', 20, ' bold '))
        Attendance.place(x=160, y=500)



        signup = tk.Button(self, text=" Sign Up ",
                            command=lambda: controller.show_frame(SignUpPage), fg="grey1", bg="yellow2",
                            width=20, height=1, activebackground="Red",
                            font=('times', 20, ' bold '))
        signup.place(x=530, y=500)

        exit_button = Button(self, text="Exit", command=controller.destroy,fg="grey1", bg="firebrick1",
                            width=20, height=1, activebackground="Red",
                            font=('times', 20, ' bold '))
        exit_button.place(x=900,y=500)


    #function to resize added image
    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)



# **********  GUI for Signup Page  *************
class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='plum1')

        message = tk.Label(
            self, text="Sign Up",
            bg="purple1", fg="grey1", width=55,
            height=3, font=('times', 30, 'bold'))
        message.place(x=20, y=20)

        #defining labels and entry fields
        lbll = tk.Label(self, text="Enter Your Details ",
                        width=20, height=2, fg="#393e46",
                        bg="plum1", font=('times', 30, ' bold '))
        lbll.place(x=420, y=200)

        lbl1 = tk.Label(self, text="Roll No. : ",
                        width=20, height=2, fg="#393e46",
                        bg="plum1", font=('times', 15, ' bold '))
        lbl1.place(x=400, y=270)

        txt1 = tk.Entry(self, width=20, bg="#fff",
                        fg="grey1", font=('times', 15, ' bold '))
        txt1.place(x=600, y=285)

        lbl2 = tk.Label(self, text="Name : ",
                        width=20, fg="#393e46", bg="plum1",
                        height=2, font=('times', 15, ' bold '))
        lbl2.place(x=400, y=320)

        txt2 = tk.Entry(self, width=20,
                        bg="#fff", fg="grey1",
                        font=('times', 15, ' bold '))
        txt2.place(x=600, y=335)

        message1 = tk.Label(
            self,
            text="Instructions: Click on Take Images,your images will be clicked. After that click on Train Images.",
            bg='Chocolate3', fg="grey1", width=100,
            height=1, font=('times', 18, 'bold'))
        message1.place(x=0, y=580)

        message2 = tk.Label(
            self, text="Return to Main Menu",
            bg="Chocolate3", fg="grey1", width=100,
            height=1, font=('times', 18, 'bold'))
        message2.place(x=0, y=610)

        #adding image for signup page
        img = Image.open("Icons/signup.png")
        img = img.resize((500, 150), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self, image=self.photoimg,bg = 'plum1')
        f_lbl.place(x=900, y=160, height=350, width=450)

        #defining buttons
        TakeImage = tk.Button(self, text="Take Images",
                              command=lambda: controller.TakeImages(txt1, txt2), fg="#393e46", bg="SpringGreen2",
                              width=15, height=2, activebackground="Red",
                              font=('times', 15, ' bold '))
        TakeImage.place(x=380, y=420)

        TrainImage = tk.Button(self, text="Train Images ",
                               command=lambda: controller.TrainImages(), fg="#393e46", bg="SpringGreen2",
                               width=15, height=2, activebackground="Red",
                               font=('times', 15, ' bold '))
        TrainImage.place(x=650, y=419)

        MainMenu = tk.Button(self, text="Return to Main Menu",
                             command=lambda: controller.show_frame(HomePage), fg='#393e46'
                             , bg='DarkSlategray1', width=15, height=2, activebackground='red',
                             font=('times', 15, ' bold '))
        MainMenu.place(x=520, y=500)


app = tkinterApp()
app.mainloop()