from tkinter import *
import json
from tkinter import messagebox

from TestingDataCreation import *
from TrainingDataCreation import *

import numpy as np

import cv2
import operator

from string import ascii_uppercase

from hunspell import Hunspell
import enchant

import tkinter as tk
from PIL import Image, ImageTk

from keras.models import model_from_json
import numpy as np
import imageio
from easygui import *
import os
from itertools import count
import string
import json

gestureList = []
nameDataset = open('gestureNames.json')
All_Names = json.load(nameDataset)
gestureNames = All_Names['gestureNames']

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"
class mainframe:


    userNames=[]
    def fetch_user_details(self):
        nameDataset = open('userdetails.json')
        All_Names = json.load(nameDataset)
        self.userNames = All_Names['details']
        
    def getcredentials(self):  #checked
        # self.ws.destroy()
        # self.mainhome()
        self.fetch_user_details()
        name = self.username.get()
        passw = self.password.get()
        print(self.userNames)
        
        if name in self.userNames:
            if str(self.userNames[name])==str(passw):
                print("Login success")
                messagebox.showinfo('Info', 'Login Successful!')
                self.ws.destroy()
                self.mainhome()
            else:
                print("Password is incorrect.")
                messagebox.showerror('Login Error', 'Password is incorrect!')
                self.passwordEntry.delete(0, END)
        else:
            print("Username is not present.")
            messagebox.showerror('Login Error', 'User is not registered! Please Register')
            self.usernameEntry.delete(0, END)
            self.passwordEntry.delete(0, END)

    def storeUserDetails(self):
        self.fetch_user_details()
        nameu = self.name.get()  #not used yet
        usern = self.username.get()
        passw = self.password.get()

        self.userNames[usern] = str(passw)
        print(self.userNames)
        data={
                "details":self.userNames
            }
        with open('userdetails.json', 'w') as outfile:
            outfile.write(json.dumps(data))
        messagebox.showinfo('Info', 'You are successfully registered! Please login to continue..')
        self.ws.destroy()
        self.home()
        
    def BacktoMain(self):
        self.tframe.destroy()
        self.mainhome()

    def BacktoSignHome(self):
        self.ws.destroy()
        cv2.destroyAllWindows()
        self.mainhome()

    def BacktoLogin(self):
        self.ws.destroy()
        self.home()

    def home(self):  #checked
        self.ws = Tk()
        self.ws.title('SignTextProject')
        self.ws.geometry('1366x768')
        self.ws.config(bg='white')
        self.img = PhotoImage(file="resources/images/1.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)
        
        self.username = StringVar()
        self.usernameEntry = Entry(
            self.ws, 
            textvariable=self.username, 
            width=20,
            font=("Helvetica", 20))  
        self.usernameEntry.place(x=990, y=515)
        
        
        self.password = StringVar()
        self.passwordEntry = Entry(
            self.ws, 
            textvariable=self.password, 
            width=20,
            font=("Helvetica", 20),
             show='*')
        self.passwordEntry.place(x=990, y=590)


        buttonLogin = Button(
            self.ws,
            text='LOGIN',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.getcredentials,
            height=1,
            width=12
        )
        buttonLogin.place(x=850, y=700)

        buttonRegister = Button(
            self.ws,
            text='REGISTER',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.registerUser,
            height=1,
            width=12
        )
        buttonRegister.place(x=1150, y=700)

        buttonClose = Button(
            self.ws,
            text='Close',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.ws.destroy,
            height=1,
            width=5
        )

        buttonClose.place(x=1270, y=20)

        self.ws.attributes('-fullscreen', True)

        self.ws.mainloop()

    def registerUser(self):
        self.ws.destroy()
        self.ws = Tk()
        self.ws.title('SignTextProject')
        self.ws.geometry('1366x768')
        self.ws.config(bg='white')
        self.img = PhotoImage(file="resources/images/2.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        self.name = StringVar()
        nameEntry = Entry(
            self.ws, 
            textvariable=self.name, 
            width=20,
            font=("Helvetica", 20))  
        nameEntry.place(x=990, y=295)
        
        self.username = StringVar()
        usernameEntry = Entry(
            self.ws, 
            textvariable=self.username, 
            width=20,
            font=("Helvetica", 20))  
        usernameEntry.place(x=990, y=390)
        
        
        self.password = StringVar()
        passwordEntry = Entry(
            self.ws, 
            textvariable=self.password, 
            width=20,
            font=("Helvetica", 20),
             show='*')
        passwordEntry.place(x=990, y=485)


        buttonRegister = Button(
            self.ws,
            text='REGISTER',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.storeUserDetails,
            height=1,
            width=12
        )
        buttonRegister.place(x=850, y=700)

        buttonCancel = Button(
            self.ws,
            text='CANCEL',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoLogin,
            height=1,
            width=12
        )
        buttonCancel.place(x=1100, y=700)

        self.ws.attributes('-fullscreen', True)

        self.ws.mainloop()
        

    def callSignToText(self):
        self.hs = Hunspell('en_US')
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None
        self.json_file = open("Models\model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()

        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("Models\model_new.h5")
        
        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        for i in ascii_uppercase:
          self.ct[i] = 0
        
        print("Loaded model from disk")
        self.tframe.destroy()
        self.ws = tk.Tk()
        self.ws.title("Sign Language To Text Conversion")
        self.ws.protocol('WM_DELETE_WINDOW', self.destructor)
        self.ws.geometry("1366x768")
        self.ws.attributes('-fullscreen', True)
        
        self.img = PhotoImage(file="resources/images/6.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        buttonClose = Button(
            self.ws,
            text='Close',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoSignHome,
            height=1,
            width=8    
        )
        buttonClose.place(x=1270 , y=20)

        self.panel = tk.Label(self.ws)
        self.panel.place(x = 65, y = 25, width = 675, height = 760)
        
        self.panel2 = tk.Label(self.ws) # initialize image panel
        self.panel2.place(x = 420, y = 170, width = 275, height = 305)

        self.panel3 = tk.Label(self.ws) # Current Symbol
        self.panel3.place(x = 1000, y = 300)

        self.panel4 = tk.Label(self.ws) # Word
        self.panel4.place(x = 1000, y = 380)

        self.panel5 = tk.Label(self.ws) # Sentence
        self.panel5.place(x = 1000, y = 460)
        
        self.panel6 = tk.Label(self.ws) #Suggestions
        self.panel6.place(x = 1000, y = 500)
        
        self.bt1 = tk.Button(self.ws, command = self.action1, height = 0, width = 0)
        self.bt1.place(x = 850, y = 600)

        self.bt2 = tk.Button(self.ws, command = self.action2, height = 0, width = 0)
        self.bt2.place(x = 1050, y = 600)

        self.bt3 = tk.Button(self.ws, command = self.action3, height = 0, width = 0)
        self.bt3.place(x = 1250, y = 600)

        self.str = ""
        self.word = ""
        self.sug = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()

        if ok:
            cv2image = cv2.flip(frame, 1)

            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = self.current_image)

            self.panel.imgtk = imgtk
            self.panel.config(image = imgtk)

            cv2image = cv2image[y1 : y2, x1 : x2]

            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)

            blur = cv2.GaussianBlur(gray, (5, 5), 2)

            th3 = cv2.adaptiveThreshold(blur, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            self.predict(res)

            self.current_image2 = Image.fromarray(res)

            imgtk = ImageTk.PhotoImage(image = self.current_image2)

            self.panel2.imgtk = imgtk
            self.panel2.config(image = imgtk)

            self.panel3.config(text = self.current_symbol, font = ("Courier", 30))

            self.panel4.config(text = self.word, font = ("Courier", 30))

            self.panel5.config(text = self.str,font = ("Courier", 30))

            predicts = self.hs.suggest(self.word)

            if(len(predicts) > 1):

                self.bt1.config(text = predicts[0], font = ("Courier", 20))

            else:

                self.bt1.config(text = "")

            if(len(predicts) > 2):

                self.bt2.config(text = predicts[1], font = ("Courier", 20))

            else:

                self.bt2.config(text = "")

            if(len(predicts) > 3):

                self.bt3.config(text = predicts[2], font = ("Courier", 20))

            else:

                self.bt3.config(text = "")

        self.ws.after(5, self.video_loop)

    def predict(self, test_image):

        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))

        prediction = {}

        prediction['blank'] = result[0][0]

        inde = 1

        for i in ascii_uppercase:

            prediction[i] = result[0][inde]

            inde += 1

        #LAYER 1

        prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'blank'):

            for i in ascii_uppercase:
                self.ct[i] = 0

        self.ct[self.current_symbol] += 1

        if(self.ct[self.current_symbol] > 60):

            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue

                tmp = self.ct[self.current_symbol] - self.ct[i]

                if tmp < 0:
                    tmp *= -1

                if tmp <= 20:
                    self.ct['blank'] = 0

                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            if self.current_symbol == 'blank':

                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""

            else:

                if(len(self.str) > 16):
                    self.str = ""

                self.blank_flag = 0

                self.word += self.current_symbol
    
    def action1(self):
            predicts = self.hs.suggest(self.word)
            if(len(predicts) > 0):
                self.word = ""
                self.str += " "
                self.str += predicts[0]

    def action2(self):
            predicts = self.hs.suggest(self.word)
            if(len(predicts) > 1):
                self.word = ""
                self.str += " "
                self.str += predicts[1]

    def action3(self):
            predicts = self.hs.suggest(self.word)
            if(len(predicts) > 2):
                self.word = ""
                self.str += " "
                self.str += predicts[2]

    def action4(self):
            predicts = self.hs.suggest(self.word)
            if(len(predicts) > 3):
                self.word = ""
                self.str += " "
                self.str += predicts[3]

    def action5(self):
            predicts = self.hs.suggest(self.word)
            if(len(predicts) > 4):
                self.word = ""
                self.str += " "
                self.str += predicts[4]
            
    def destructor(self):

        print("Closing Application...")

        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()
    def destructor(self):

        print("Closing Application...")
        
        self.ws.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

    
        pass
    def signToText(self):
        self.ws.destroy()
        
        self.tframe = Tk()
        self.tframe.title('SignTextProject')
        self.tframe.geometry('1366x768')
        self.tframe.config(bg='white')
        self.img = PhotoImage(file="resources/images/5.png")
        label = Label(
            self.tframe,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        button1 = Button(
            self.tframe,
            text='Translation',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.callSignToText,
            height=1,
            width=18    
        )

        button2 = Button(
            self.tframe,
            text='Create Dataset',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.CollectData,
            height=1,
            width=18  
        )

        button3 = Button(
            self.tframe,
            text='Back',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoMain,
            height=1,
            width=8    
        )
        button1.place(x=330 , y=470)
        button2.place(x=910, y=470)
        button3.place(x=700, y=700)
        self.tframe.attributes('-fullscreen', True)
        self.tframe.mainloop()

    def CollectData(self):
        self.tframe.destroy()
        
        self.tframe = Tk()
        self.tframe.title('SignTextProject')
        self.tframe.geometry('1366x768')
        self.tframe.config(bg='white')
        self.img = PhotoImage(file="resources/images/8.png")
        label = Label(
            self.tframe,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        button1 = Button(
            self.tframe,
            text='Collect Training Data',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = collectTrainData,
            height=1,
            width=18    
        )

        button2 = Button(
            self.tframe,
            text='Collect Testing Data',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = collectTestData,
            height=1,
            width=18  
        )

        button3 = Button(
            self.tframe,
            text='Back',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoMain,
            height=1,
            width=8    
        )
        button1.place(x=320 , y=490)
        button2.place(x=905, y=490)
        button3.place(x=700, y=700)
        self.tframe.attributes('-fullscreen', True)
        self.tframe.mainloop()

    def func(self):

        class ImageLabel(tk.Label):
            """a label that displays images, and print sequence of the images"""
            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                self.loc = 0
                self.frames = []

                try:
                    for i in count(1):
                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass

                try:
                    self.delay = im.info['duration']
                except:
                    self.delay = 100

                if len(self.frames) == 1:
                    self.config(image=self.frames[0])
                else:
                    self.next_frame()

            def unload(self):
                self.config(image=None)
                self.frames = None

            def next_frame(self):
                if self.frames:
                    self.loc += 1
                    self.loc %= len(self.frames)
                    self.config(image=self.frames[self.loc])
                    self.after(self.delay, self.next_frame)


        
        nameDataset = open('gestureNames.json')
        All_Names = json.load(nameDataset)
        gestureNames = All_Names['gestureNames']

        arr=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r', 's','t','u','v','w','x','y','z']
        i=0

        #a = self.sentence.lower()
        a = self.sentence.get()
        a = a.lower()
        print('You Said: ' + a)

        for c in string.punctuation:
            a= a.replace(c,"")

        
        if(a.lower()=='goodbye' or a.lower()=='good bye' ):
            print("Thank You..Good Bye")
        
        elif(a.lower() in gestureNames):
            self.lbl1 = ImageLabel(self.ws)
            self.lbl1.pack()
            self.lbl1.place(x=700, y=150)
            self.lbl1.load(r'Gestures/{0}.gif'.format(a.lower()))
            

        else:
            self.label = Label(
                self.ws,
                anchor= CENTER,
                
            )
            self.label.place(x=700, y=250)
            pathList = []
            images = []
            for i in range(len(a)):
                if(a[i] in arr):
                    path = 'Letters/'+a[i]+'.jpg'
                    pathList.append(path)
                                            
                else:
                    continue               
                
       
            for filename in pathList:
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
                images.append(imageio.imread(filename))
            imageio.mimsave('D:/Final_Bidirectional/Final/Letters/all.gif', images)
            self.lbl2 = ImageLabel(self.ws,width=640, height=480)
            self.lbl2.pack()
            self.lbl2.place(x=700, y=150)
            self.lbl2.config(bg="yellow")
            self.lbl2.load('Letters/all.gif'.format(a.lower()))
                       

    def captureGif(self):
        gestureName = self.gestName.get()
        cap = cv2.VideoCapture(0)
        frames = []
        image_count = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow("frame", frame)
            key = cv2.waitKey(0)
            if key == ord("a"):
                image_count += 1
                frames.append(frame)
                print("Adding new image:", image_count)
            elif key == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                break   
        print("Images added: ", len(frames))

        print("Saving GIF file")
        fileName = "Gestures/" + gestureName + ".gif"
        with imageio.get_writer(fileName, mode="I") as writer:
            for idx, frame in enumerate(frames):
                print("Adding frame to GIF file: ", idx + 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(rgb_frame)
                gestureList.append(gestureName)

        newlst = []
        for name in gestureList:
            newlst.append(str(name).lower())
        global gestureNames
        gestureNames+=newlst
        gestureNames=np.array(list(set(gestureNames)))
        gestureNames.sort()
        gestureNames=list(gestureNames)
        data={
            "gestureNames":gestureNames
        }
        with open('gestureNames.json', 'w') as outfile:
            outfile.write(json.dumps(data))

        self.gestNameEntry.delete(0, END)

    def Translation(self):
        self.tframe.destroy()
        
        self.ws = Tk()
        self.ws.title('SignTextProject')
        self.ws.geometry('1366x768')
        self.ws.config(bg='white')
        self.img = PhotoImage(file="resources/images/7.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        self.sentence = StringVar()
        self.sentenceEntry = Entry(
            self.ws, 
            textvariable=self.sentence, 
            width=20,
            font=("Helvetica", 20))  
        self.sentenceEntry.place(x=250, y=350)

        buttonSearch = Button(
            self.ws,
            text='Done',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.func,
            height=1,
            width=5
        )

        buttonSearch.place(x=370, y=400)

        buttonClose = Button(
            self.ws,
            text='Close',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoSignHome,
            height=1,
            width=5
        )

        buttonClose.place(x=1270, y=20)  

        self.ws.attributes('-fullscreen', True)

        self.ws.mainloop()
        

    def createGesture(self):
        self.tframe.destroy()
        
        self.ws = Tk()
        self.ws.title('SignTextProject')
        self.ws.geometry('1366x768')
        self.ws.config(bg='white')
        self.img = PhotoImage(file="resources/images/7.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        self.gestName = StringVar()
        self.gestNameEntry = Entry(
            self.ws, 
            textvariable=self.gestName, 
            width=20,
            font=("Helvetica", 20))  
        self.gestNameEntry.place(x=250, y=350)

        buttonCreate = Button(
            self.ws,
            text='Create',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.captureGif,
            height=1,
            width=5
        )

        buttonCreate.place(x=370, y=400)      

        buttonClose = Button(
            self.ws,
            text='Close',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoSignHome,
            height=1,
            width=5
        )

        buttonClose.place(x=1270, y=20)  
        
        self.ws.attributes('-fullscreen', True)

        self.ws.mainloop()
            

    def textToSign(self):
        self.ws.destroy()
        
        self.tframe = Tk()
        self.tframe.title('SignTextProject')
        self.tframe.geometry('1366x768')
        self.tframe.config(bg='white')
        self.img = PhotoImage(file="resources/images/4.png")
        label = Label(
            self.tframe,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        button1 = Button(
            self.tframe,
            text='Translation',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.Translation,
            height=1,
            width=18    
        )

        button2 = Button(
            self.tframe,
            text='Create Gestures',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.createGesture,
            height=1,
            width=18  
        )

        button3 = Button(
            self.tframe,
            text='Back',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoMain,
            height=1,
            width=8    
        )
        button1.place(x=330 , y=470)
        button2.place(x=910, y=470)
        button3.place(x=700, y=700)
        self.tframe.attributes('-fullscreen', True)
        self.tframe.mainloop()
        


    def mainhome(self):

        self.ws = Tk()

        self.ws.title('SignTextProject')
        self.ws.geometry('1366x768')
        self.ws.config(bg='white')
        self.img = PhotoImage(file="resources/images/3.png")
        label = Label(
            self.ws,
            anchor= CENTER,
            image=self.img
            
        )
        label.config(anchor=CENTER)
        label.place(x=60, y=20)

        
        button1 = Button(
            self.ws,
            text='Sign To Text',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.signToText,
            height=2,
            width=18    
        )

        button2 = Button(
            self.ws,
            text='Text To Sign',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.textToSign,
            height=2,
            width=18  
        )

        button3 = Button(
            self.ws,
            text='Logout',
            relief=RAISED,
            font=('Arial Bold', 18),
            command = self.BacktoLogin,
            height=1,
            width=5  
        )
        button1.place(x=230 , y=388)
        button2.place(x=230, y=520)
        button3.place(x=1260, y=20)
        self.ws.attributes('-fullscreen', True)

        self.ws.mainloop()
    
s=mainframe()
s.home()
