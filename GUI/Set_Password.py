import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import mysql.connector
import Forgot_password
import login

def set_password_page():
    try:
        def reset_password2():
            # Add your reset password logic here
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()
            if new_password == confirm_password:
                # Connect to the MySQL database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )
                # Create a cursor object
                cursor = conn.cursor()
                username = Forgot_password.username
                print(username)
                sql = "UPDATE login set password = %s where username = %s"
                values = (new_password, username)
                cursor.execute(sql, values)
                conn.commit()
                messagebox.showinfo("Success","Password reset successfully!")
                root.destroy()
                Forgot_password.forgot_password_page().root.destroy()
                login.login_page().login_win.deiconify()
            else:
                messagebox.showerror("Error","Passwords didn't match!")

        root = tk.Tk()
        root.title("Set Password")
        root.geometry("420x160+650+250")
        style = ttk.Style(theme="yeti")

        frame1 = ttk.Frame(root, borderwidth=2, relief="solid")
        frame1.grid(row=1, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)

        label_name = ttk.Label(frame1, text="Set Password", font=("Helvetica", 14, "bold"))
        label_name.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=5)

        label_new_password = ttk.Label(frame1, text="New Password", font=("Helvetica", 12))
        label_new_password.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        entry_new_password = ttk.Entry(frame1, width=36)
        entry_new_password.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        label_confirm_password = ttk.Label(frame1, text="Confirm Password", font=("Helvetica", 12))
        label_confirm_password.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        entry_confirm_password = ttk.Entry(frame1, width=36)
        entry_confirm_password.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        reset_button = ttk.Button(frame1, text="Reset Password", width=10, style="success.TButton", command=reset_password2)
        reset_button.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=3, padx=3)

        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error",e)

