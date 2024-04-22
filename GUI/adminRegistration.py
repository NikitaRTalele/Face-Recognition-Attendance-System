import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import messagebox
import mysql.connector
from email_validator import validate_email, EmailNotValidError
import adminHome

def adminRegister_Page():
    try:
        def back():
            adminRegister_win.destroy()
            adminHome.adminHomePage().alogin_win.deiconify()
        def register_admin():
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            # Create a cursor object
            cursor = mydb.cursor()

            admin_id = entry_admin_id.get()
            first_name = entry_first_name.get()
            last_name = entry_last_name.get()
            phone_no = entry_contact_no.get()
            email_id = entry_email_id.get()

            sql = "SELECT * FROM Admin WHERE Admin_id = %s"
            cursor.execute(sql, (admin_id,))
            row = cursor.fetchone()
            if row:
                messagebox.showerror("Error", "ID already exists!, Please enter unique ID.")
            else:
                if admin_id.isdigit():
                    if len(first_name) > 1 and len(last_name)>1:
                        if len(phone_no) == 10:
                            if phone_no.isdigit():
                                if validate_email(email_id, check_deliverability=False):
                                    sql = "INSERT INTO Admin (Admin_id, first_name, last_name, phone_no, Email) VALUES (%s,%s,%s,%s,%s)"
                                    values = (admin_id, first_name, last_name, phone_no, email_id)
                                    cursor.execute(sql, values)

                                    # Commit the transaction
                                    mydb.commit()

                                    sql = "INSERT into login (username, password, security_question, security_answer, role, login_count) VALUES (%s, %s, %s, %s, %s, %s)"
                                    values = (email_id, "Terna@123", "", "", "Admin", "0")
                                    cursor.execute(sql, values)
                                    mydb.commit()

                                    messagebox.showinfo("Success","Admin added successfully")

                                    cursor.close()
                                    mydb.close()
                                elif EmailNotValidError:
                                    messagebox.showerror("Error",
                                                         "Email is not valid, please enter a valid email address")
                            else:
                                messagebox.showerror("Error","Phone no. should be a number")
                        else:
                            messagebox.showerror("Error","Phone number should be 10 digit.")
                    else:
                        messagebox.showerror("Error","Name should contain min 2 characters")
                else:
                    messagebox.showerror("Error","Admin ID should be a number.")
        adminRegister_win = tk.Tk()
        adminRegister_win.title("Admin Registration")
        adminRegister_win.geometry("550x330+575+150")
        style = Style(theme="yeti")

        frame1 = ttk.Frame(adminRegister_win, borderwidth=2, relief="solid", )
        frame1.grid(row=1, column=0, sticky="nsew")
        adminRegister_win.columnconfigure(0, weight=1)

        # Label for Admin Registration
        label_title = ttk.Label(frame1, text="Admin Registration", font=("Helvetica", 20, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=5)

        # Define font style for labels and entries
        font_style = ("Helvetica", 16)

        # Label and Entry for Admin ID
        label_admin_id = ttk.Label(frame1, text="Admin ID", font=font_style)
        label_admin_id.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        entry_admin_id = ttk.Entry(frame1, width=30, font=font_style)
        entry_admin_id.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        # Label and Entry for First Name
        label_first_name = ttk.Label(frame1, text="First Name", font=font_style)
        label_first_name.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        entry_first_name = ttk.Entry(frame1, width=30, font=font_style)
        entry_first_name.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        # Label and Entry for Last Name
        label_last_name = ttk.Label(frame1, text="Last Name", font=font_style)
        label_last_name.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        entry_last_name = ttk.Entry(frame1, width=30, font=font_style)
        entry_last_name.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        # Label and Entry for Contact No.
        label_contact_no = ttk.Label(frame1, text="Contact No.", font=font_style)
        label_contact_no.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        entry_contact_no = ttk.Entry(frame1, width=30, font=font_style)
        entry_contact_no.grid(row=4, column=1, sticky="e", padx=10, pady=5)

        # Label and Entry for Email ID
        label_email_id = ttk.Label(frame1, text="Email ID", font=font_style)
        label_email_id.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        entry_email_id = ttk.Entry(frame1, width=30, font=font_style)
        entry_email_id.grid(row=5, column=1, sticky="e", padx=10, pady=5)


        # Register Button
        btn_register = ttk.Button(frame1, text="Register", width=10, style="primary", command=register_admin)
        btn_register.grid(row=10, column=0, columnspan=2, sticky="nsew", pady=3, padx=3)

        # Back Button
        btn_back = ttk.Button(frame1, text="Back", width=10, style="primary", command=back)
        btn_back.grid(row=11, column=0, columnspan=2, sticky="nsew", pady=3, padx=3)

        adminRegister_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error",e)

