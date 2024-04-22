import tkinter as tk
import ttkbootstrap as ttk
import mysql.connector
from tkinter import messagebox
from ttkbootstrap.constants import *
from Set_Questions import set_security_page
from adminHome import adminHomePage
from facultyHome import facultyHomePage
from studentHome import studentHomePage
from Forgot_password import forgot_password_page

username = ""
def login_page():
    try:
        def login():
            # Creating mysql connection
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='major_project'
            )
            # wrote this statement to check status of connection with database
            print(conn)

            c1 = conn.cursor()

            # retrieve username and pass from user
            global username
            username = username_entry.get()
            password = password_entry.get()

            # we have to check if usr_name & pass exists in db
            # Check username and password in the database
            sql = "SELECT * FROM login WHERE username = %s AND password = %s"
            val = (username, password)
            c1.execute(sql, val)
            result = c1.fetchone()

            if result:
                print("Login Successful!")
                sql = "SELECT login_count FROM login WHERE username = %s AND password = %s"
                val = (username, password)
                c1.execute(sql, val)
                login_count = c1.fetchone()
                print(login_count[0])
                if login_count[0] == 0:
                    login_win.destroy()
                    set_security_page()
                elif login_count[0] != 0:
                    sql = "SELECT role FROM login WHERE username = %s AND password = %s"
                    val = (username, password)
                    c1.execute(sql, val)
                    role = c1.fetchone()
                    if role[0] == "admin":
                        login_win.withdraw()
                        adminHomePage()
                    elif role[0] == "student":
                        login_win.withdraw()
                        studentHomePage()
                    elif role[0] == "faculty":
                        login_win.withdraw()
                        facultyHomePage()
                    conn.commit()
                    conn.close()
            elif username == "" and password != "":
                messagebox.showerror("Error", "Username field is empty")
            elif username != "" and password == "":
                messagebox.showerror("Error", "Password field is empty")
            elif username == "" and password == "":
                messagebox.showerror("Error", "Username and Password fields are empty")
            else:
                print("Invalid username or password")
                messagebox.showerror("Error", "Invalid username or password")

        def forgot_password():
            login_win.withdraw()
            forgot_password_page()

        login_win = tk.Tk()
        login_win.geometry('590x430+490+150')
        login_win.title('Login')

        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        fr1 = tk.Frame(login_win, highlightbackground="black")
        fr1.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        fr2 = tk.Frame(login_win, highlightbackground="black", highlightthickness=1)
        fr2.grid(row=1, column=0, padx=10, pady=5)

        # Frame 1 contents
        l1 = tk.Label(fr1, text='Face Recognition Attendance System', font=h1)
        l1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame 2 contents
        l2 = tk.Label(fr2, text='Login', font=h2)
        l2.grid(row=0, column=0, padx=30, pady=10, columnspan='2', sticky="nsew")
        l3 = tk.Label(fr2, text='Username: ', font=f1)
        l3.grid(row=1, column=0, padx=50, pady=10, columnspan='1', sticky="nse")
        username_entry = ttk.Entry(fr2, font=f2)
        username_entry.grid(row=1, column=1, padx=10, pady=10, columnspan='1', sticky="nsw")
        l4 = tk.Label(fr2, text='Password: ', font=f1)
        l4.grid(row=2, column=0, padx=50, pady=10, columnspan='1', sticky="nse")
        password_entry = ttk.Entry(fr2, font=f2, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10, columnspan='1', sticky="nsw")
        b1 = tk.Button(fr2, text='Login', font=f1, background='light blue', command=login)
        b1.grid(row=3, column=0, padx=50, pady=10, columnspan='2')

        def on_enter(event):
            l5.config(fg="blue")  # Change label background and foreground color on hover

        def on_leave(event):
            l5.config(fg="black")  # Restore original colors when mouse leaves

        l5 = tk.Label(fr2, text='Forgot Password?', font=f1, cursor="hand2")
        l5.grid(row=4, column=0, padx=50, pady=10, columnspan='2', sticky="nsew")
        l5.bind("<Enter>", on_enter)  # Binds the hover event to the label
        l5.bind("<Leave>", on_leave)  # Binds the mouse leave event to the label
        l5.bind("<Button-1>", lambda event: forgot_password())
        login_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)


