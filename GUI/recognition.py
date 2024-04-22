from logging import exception
from tkinter import *
from tkinter import ttk
from PIL import ImageTk , Image
from time import strftime
from datetime import datetime
from tkinter import messagebox
import mysql.connector
import os
import cv2
import numpy as np

class Recognition: #creating class
    def __init__(self,root): #calling constructor; root is the root window..base window...the first window or the home page
        self.root=root #initialising self
        self.root.title("Face Recognition") #giving title to root window
        self.root.geometry("1560x800+0+0") #setting screen size for root window

        lt=Label(self.root,text="ATTENDANCE SYSTEM USING FACE RECOGNITION",font=("algerian",30,"bold"),bg="black",fg="white")
        lt.place(x=0,y=0,width=1560,height=75)

        img1 = Image.open(r"Photos_required\cropped2_face-scanning-1-e1575541339743.jpg")
        img1=img1.resize((630,725),Image.ANTIALIAS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        l1=Label(self.root,image=self.photoimg1)
        l1.place(x=0,y=75,width=630,height=725)

        img2 = Image.open(r"Photos_required\cropped2_AI-FR-BTVON.jpg")
        img2=img2.resize((910,725),Image.ANTIALIAS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        l2=Label(self.root,image=self.photoimg2)
        l2.place(x=630,y=75,width=910,height=725)

        b1_1=Button(self.root,text="FACE RECOGNITION",command=self.face_recog,cursor='hand2',borderwidth=5,font=("algerian",22,"bold"),bg="black",fg="white")
        b1_1.place(x=610,y=410,width=300,height=60)

    #=====================Attendance======================== 
    def mark_attendance(self,fetch_data_id,fetch_data_name,fetch_data_rollno,fetch_data_div,fetch_data_department):
        with open("StudentAttendance.csv","r+",newline="\n") as f: #r+ mtlb read first then write it...simply r hota to u can onlu read but not write...w+ mtlb write first then read
            myDataList=f.readlines()
            name_list=[] #creating an empty list for storing data
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((fetch_data_id not in name_list) and (fetch_data_name not in name_list) and (fetch_data_rollno not in name_list) and (fetch_data_div not in name_list) and (fetch_data_department not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"{fetch_data_id},{fetch_data_name},{fetch_data_rollno},{fetch_data_div},{fetch_data_department},{dtString},{d1},Present\n")
                


    #=====================Face Recognition========================
    def face_recog(self):
        def boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            grey_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(grey_img,scaleFactor,minNeighbors)
            coord=[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                id,predict=clf.predict(grey_img[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300))) #formula for confidence

                conn=mysql.connector.connect(host="localhost",username="root", password="VruRo&Ot#MySQL%1947", database="face_recognition")
                my_cursor=conn.cursor()

                my_cursor.execute("select name from student where stdid="+str(id))
                #print(my_cursor)
                fetch_data_name=my_cursor.fetchone()
                #print(type(fetch_data_name))
                fetch_data_name="+".join(fetch_data_name)

                my_cursor.execute("select division from student where stdid="+str(id))
                fetch_data_div=my_cursor.fetchone()
                fetch_data_div="+".join(fetch_data_div)

                my_cursor.execute("select rollno from student where stdid="+str(id))                
                fetch_data_rollno=my_cursor.fetchone()
                fetch_data_rollno="+".join(fetch_data_rollno)

                my_cursor.execute("select department from student where stdid="+str(id))
                fetch_data_department=my_cursor.fetchone()
                fetch_data_department="+".join(fetch_data_department)

                my_cursor.execute("select stdid from student where stdid="+str(id))
                fetch_data_id=my_cursor.fetchone()
                fetch_data_id="+".join(fetch_data_id)

                try: 
                    if confidence>77:                    
                        cv2.putText(img,f"ID: {fetch_data_id}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,255),2)
                        cv2.putText(img,f"Name: {fetch_data_name}",(x,y-60),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,255),2)
                        cv2.putText(img,f"Roll No: {fetch_data_rollno}",(x,y-45),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),2)
                        cv2.putText(img,f"Division: {fetch_data_div}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,0),2)
                        cv2.putText(img,f"Department: {fetch_data_department}",(x,y-15),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,0),2)
                        self.mark_attendance(fetch_data_id,fetch_data_name,fetch_data_rollno,fetch_data_div,fetch_data_department) #,fetch_data_name                   

                    else:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                        cv2.putText(img,"Unknown Face",(x,y-20),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,0,0),2)

                except Exception as es:
                    messagebox.showerror("ERROR",f"Due To: {str(es)}",parent=self.root)

                coord=[x,y,w,h]
            return coord

        def recognize(img,clf,faceCascade):
            coord = boundary(img,faceCascade,1.1,10,(255,0,255),"Face",clf)
            return img

        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("TrainDataClassifier.xml")

        capture=cv2.VideoCapture(0+cv2.CAP_DSHOW)
        #print(capture)
        try:
            while True:
                #capture=cv2.VideoCapture(0,cv2.CAP_DSHOW)
                ret,img=capture.read()
                img=recognize(img,clf,faceCascade)
                cv2.imshow("Welcome To Face Recognition",img)

                k = cv2.waitKey(1) & 0xFF
                #print(k)
                if k== ord('q'):
                    cv2.destroyAllWindows()
                    break
            capture.release()
            cv2.destroyAllWindows()

        except Exception as es:
            messagebox.showerror("ERROR",f"{str(es)}",parent=self.root)

        # while True:
        #     k = cv2.waitKey(0) & 0xFF
        #     print(k)
        #     if k== ord('q'):
        #         cv2.destroyAllWindows()
        #         break            
            #if cv2.waitKey(1) == 'q':
                #break               
             
                       
if __name__=="__main__":
   root = Tk() #calling root using toolkit (tk)
   obj=Recognition(root)
   root.mainloop()