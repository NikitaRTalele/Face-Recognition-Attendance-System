import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap import Style, DateEntry
from tkinter import messagebox
import mysql.connector
from Set_Password import set_password_page

username = ""
def forgot_password_page():
    try:

        def reset_password():
            global username
            username = entry_username.get()
            security_question = class_name_var.get()
            security_answer = entry_security_answer.get()

            if username and security_question and security_answer:
                # Connect to the MySQL database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )
                # Create a cursor object
                cursor = conn.cursor()

                sql = "select * from login where username = %s and security_question = %s and security_answer = %s"
                values = (username,security_question,security_answer)
                cursor.execute(sql,values)
                row = cursor.fetchone()
                if row:
                    root.withdraw()
                    set_password_page()
                else:
                    messagebox.showerror("Error","Details didn't match!, Please enter correct details!")
            else:
                messagebox.showerror("Error","Fill all the fields!")

        #==================================ROOT WINDOW=================================
        root = tk.Tk()
        root.title("Forgot Password")
        style = ttk.Style()
        style.theme_use("yeti")
        root.geometry("400x200+650+300")

        frame1 = ttk.Frame(root, borderwidth=2, relief="solid")
        frame1.grid(row=1, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)

        label_name = ttk.Label(frame1, text="Forgot Password", font=("Helvetica", 14, "bold"))
        label_name.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=5)

        label_username = ttk.Label(frame1, text="Username", font=("Helvetica", 12))
        label_username.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        entry_username = ttk.Entry(frame1, width=36)
        entry_username.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        label_security_question = ttk.Label(frame1, text="Security Question", font=("Helvetica", 12))
        label_security_question.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        options = ["My Birthplace?", "My favourite fast food?", "My favourite Colour?", "My first school name?"]
        class_name_var = tk.StringVar()
        class_name_var.set(options[0])  # Set default value

        class_name_dropdown = ttk.Combobox(frame1, values=options, width=34, textvariable=class_name_var)
        class_name_dropdown.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        label_security_answer = ttk.Label(frame1, text="Security Answer", font=("Helvetica", 12))
        label_security_answer.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        entry_security_answer = ttk.Entry(frame1, width=36)
        entry_security_answer.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        reset_button = ttk.Button(frame1, text="Reset Password", width=10, style="success.TButton",
                                  command=reset_password)
        reset_button.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=3, padx=3)


        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error",e)


# Fetch Email, Security Question and Security Answer
# check if it is right in login table or not
# if right then password change
# if wrong then give error that details didn't match