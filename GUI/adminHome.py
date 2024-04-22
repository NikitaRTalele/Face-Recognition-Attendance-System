import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from studentProfile import studentProfile_Page
from facultyProfile import facultyProfile_Page
from assignSub import assignSubject_Page
from adminRegistration import adminRegister_Page
from AboutDevelopers import aboutDevelopers_page
from trainData1 import train
# from main2 import TakeImages
import login

def adminHomePage():
    try:
        def studentProfile():
            alogin_win.withdraw()
            studentProfile_Page()

        def facultyProfile():
            alogin_win.withdraw()
            facultyProfile_Page()

        def assignSubject():
            alogin_win.withdraw()
            assignSubject_Page()

        def trainData():
            alogin_win.withdraw()
            train()
            
            

        def registerAdmin():
            alogin_win.withdraw()
            adminRegister_Page()
        def developer():
            alogin_win.lower()
            aboutDevelopers_page()

        def photos():
            pass

        def logout():
            alogin_win.destroy()
            login.login_page().login_win.deiconify()
            #login.login_page()
        alogin_win = tk.Tk()

        alogin_win.geometry('400x500+620+100')
        alogin_win.title('Attendance System Admin Login')

        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        l1 = ttk.Label(alogin_win, text='Attendance System', font=h1)
        l1.pack(pady=20)
        b1 = tk.Button(alogin_win, text='Student Profile', font=f1, width=20, command=studentProfile)
        b1.pack(pady=5)
        b2 = tk.Button(alogin_win, text='Faculty Profile', font=f1, width=20, command=facultyProfile)
        b2.pack(pady=5)
        b3 = tk.Button(alogin_win, text='Assign Subject', font=f1, width=20, command=assignSubject)
        b3.pack(pady=5)
        b4 = tk.Button(alogin_win, text='Train Data', font=f1, width=20, command=trainData)
        b4.pack(pady=5)
        b5 = tk.Button(alogin_win, text='Register Admin', font=f1, width=20, command=registerAdmin)
        b5.pack(pady=5)
        b6 = tk.Button(alogin_win, text='Developer', font=f1, width=20, command=developer)
        b6.pack(pady=5)
        b7 = tk.Button(alogin_win, text='Photos', font=f1, width=20, command=photos)
        b7.pack(pady=5)

        button_style = {
            "font": ("Arial", 16),  # Change font and size here
            "bg": "#Ff0000",  # Background color
            "fg": "black",  # Foreground (text) color
            "pady": 5,  # Vertical padding
            "text": "Logout",  # Button text
        }

        b8 = tk.Button(alogin_win, width=20, **button_style, command=logout)
        b8.pack(pady=5)

        alogin_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)
