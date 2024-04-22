import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
from tkinter import messagebox
import login
import tkinter as tk
from AboutDevelopers import aboutDevelopers_page
from Faculty_Mark_attendance import faculty_mark_attendance
from Faculty_attendance_View import faculty_attendance_view_page

def facultyHomePage():
    try:
        facultyHome_win = tk.Tk()
        facultyHome_win.geometry('500x250+590+250')
        facultyHome_win.title('Faculty Home')

        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        # Function to be called when the buttons are clicked
        def mark_attendance():
            facultyHome_win.withdraw()
            faculty_mark_attendance()

        def view_attendance():
            facultyHome_win.withdraw()
            faculty_attendance_view_page()

        def developers():
            facultyHome_win.withdraw()
            aboutDevelopers_page()

        def logout():
            facultyHome_win.destroy()
            login.login_page().login_win.deiconify()
            #login.login_page()

        # Create buttons
        button1 = tk.Button(facultyHome_win, text="Mark Attendance", font=f1, bg='light blue', command=mark_attendance)
        button2 = tk.Button(facultyHome_win, text="View Attendance", font=f1, bg='light blue',command=view_attendance)
        button3 = tk.Button(facultyHome_win, text="Developers", font=f1, bg='light blue',command=developers)
        button4 = tk.Button(facultyHome_win, text="Logout", font=f1, bg='light blue', command=logout)

        # Place buttons using pack
        button1.pack(pady=10)
        button2.pack(pady=10)
        button3.pack(pady=10)
        button4.pack(pady=10)

        facultyHome_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)

# Call the function to display the window

