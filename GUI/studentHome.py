import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
import mysql.connector
import tkinter as tk
import login
from AboutDevelopers import aboutDevelopers_page
from Studentattendancereport import student_attendance_report_page

def studentHomePage():
    try:
        studentHome_win = tk.Tk()
        studentHome_win.geometry('300x200+690+300')
        studentHome_win.title('Student Home')

        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        # Function to be called when the buttons are clicked
        def student_attendance_report():
            studentHome_win.withdraw()
            student_attendance_report_page()

        def developers():
            studentHome_win.withdraw()
            aboutDevelopers_page()

        def logout():
            studentHome_win.destroy()
            login.login_page().login_win.deiconify()
            #login.login_page()

        # Create buttons
        button1 = tk.Button(studentHome_win, text="View Attendance Report", font=f1, bg='light blue', command=student_attendance_report)
        button2 = tk.Button(studentHome_win, text="Developers", font=f1, bg='light blue', command=developers)
        button3 = tk.Button(studentHome_win, text="Logout", font=f1, bg='light blue', command=logout)

        # Place buttons using pack
        button1.pack(pady=10)
        button2.pack(pady=10)
        button3.pack(pady=10)

        studentHome_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)


