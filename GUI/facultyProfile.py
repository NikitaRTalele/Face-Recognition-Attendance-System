import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
from tkinter import messagebox
from email_validator import validate_email, EmailNotValidError
import adminHome

# search_performed = False\
def facultyProfile_Page():
    try:
        def back():
            facultyProfile_win.destroy()
            adminHome.adminHomePage().alogin_win.deiconify()
        def display_data():
            # global search_performed, cursor, mydb
            try:
                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )

                # Create a cursor object
                cursor = mydb.cursor()

                # Execute SELECT query
                sql = "SELECT * FROM Faculty ORDER BY Faculty_id ASC";
                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                rtv1.delete(*rtv1.get_children())

                # Insert the new data into the right-side table
                for row in rows:
                    rtv1.insert("", tk.END, values=row)
                # search_performed=False
            except Exception as e:
                # Print error message
                print(f"Error fetching data: {e}")
            # finally:
            # Close the cursor and connection
            # cursor.close()
            # mydb.close()

        def save_data():
            try:
                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )
                print(mydb)
                # Create a cursor object
                cursor = mydb.cursor()

                # Retrieve data from Tkinter widgets
                first_name = e2.get()
                last_name = e3.get()
                faculty_id = e4.get()
                email = e5.get()
                phone_no = e6.get()

                # validations for ID exists or not
                sql = "SELECT * FROM Faculty WHERE Faculty_id = %s"
                cursor.execute(sql, (faculty_id,))
                row = cursor.fetchone()
                if row:
                    messagebox.showerror("Error", "ID already exists!, Please enter unique ID.")
                else:
                    if faculty_id.isdigit():
                        if len(first_name) > 1 and len(last_name) > 1:
                            if validate_email(email, check_deliverability=False):
                                if len(phone_no) == 10:
                                    if phone_no.isdigit():
                                        # Execute INSERT query
                                        sql = "INSERT INTO Faculty (Faculty_first_name, Faculty_last_name, Faculty_id, Email, phone_no) VALUES (%s,%s,%s,%s,%s)"
                                        values = (first_name, last_name, faculty_id, email, phone_no)
                                        cursor.execute(sql, values)

                                        # Commit the transaction
                                        mydb.commit()

                                        # Fetch the last inserted record
                                        cursor.execute("SELECT * FROM Faculty ORDER BY Faculty_id DESC LIMIT 1")
                                        row = cursor.fetchone()

                                        # Insert the new data into the right-side table
                                        rtv1.insert("", tk.END, values=(faculty_id,
                                        first_name, last_name, email, phone_no))
                                        mydb.commit()

                                        sql = "INSERT into login (username, password, security_question, security_answer, role, login_count) VALUES (%s, %s, %s, %s, %s, %s)"
                                        values = (email, "Terna@123", "", "", "Faculty", "0")
                                        cursor.execute(sql, values)
                                        mydb.commit()

                                        messagebox.showinfo("Success", "Faculty details Updated", parent=facultyProfile_win)
                                    else:
                                        messagebox.showerror("Error", "Phone number must be a long integer")
                                else:
                                    messagebox.showerror("Error", "Phone No. should be minimum 10 digits.")
                            elif EmailNotValidError:
                                messagebox.showerror("Error",
                                                     "Email is not valid, please enter a valid email address")
                        else:
                            messagebox.showerror("Error", "Name should be minimum 2 letters.")
                    else:
                        messagebox.showerror("Error", "ID should be a number")

            except EmailNotValidError as er1:
                messagebox.showerror("Error", "Email is not valid.")
            except Exception as e:
                # Print error message
                print(f"Error inserting data: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                mydb.close()

        def on_item_click(event):
            # Get the selected item
            item = rtv1.selection()[0]

            # Get values from the selected item
            values = rtv1.item(item, 'values')

            # Populate the input fields
            e2.delete(0, tk.END)
            e2.insert(0, values[1])  # Assuming Student ID is the second column
            e3.delete(0, tk.END)
            e3.insert(0, values[2])  # Assuming Name is the third column
            e4.delete(0, tk.END)
            e4.insert(0, values[0])  # Assuming Roll No is the fourth column
            e5.delete(0, tk.END)
            e5.insert(0, values[3])  # Assuming Email ID is the fifth column
            e6.delete(0, tk.END)
            e6.insert(0, values[4])  # Assuming Phone No is the sixth column

        def delete_data():
            try:
                # Get the selected item
                item = rtv1.selection()[0]

                # Get values from the selected item
                values = rtv1.item(item, 'values')

                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )

                # Create a cursor object
                cursor = mydb.cursor()

                # Execute DELETE query
                sql = "DELETE FROM Faculty WHERE Faculty_id = %s"
                value = (values[0],)
                cursor.execute(sql, value)

                # Commit the transaction
                mydb.commit()

                # Execute DELETE query
                sql = "DELETE FROM login WHERE username = %s"
                value = (values[3],)
                print(value)
                cursor.execute(sql, value)
                mydb.commit()

                # Close the cursor and connection

                # Print success message
                print("Data deleted successfully!")

                # Remove the selected item from the Treeview
                rtv1.delete(item)
            except Exception as e:
                # Print error message
                print(f"Error deleting data: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                mydb.close()

        def update_data():
            try:
                # Get the selected item
                item = rtv1.selection()[0]

                # Get values from the selected item
                values = rtv1.item(item, 'values')

                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )

                # Create a cursor object
                cursor = mydb.cursor()

                current_values = rtv1.item(item, 'values')
                # Retrieve data from Tkinter widgets
                first_name = e2.get()
                last_name = e3.get()
                faculty_id = e4.get()
                email_id = e5.get()
                phone_no = e6.get()

                # validations for ID exists or not
                sql = "SELECT * FROM Faculty WHERE faculty_id = %s"
                cursor.execute(sql, (faculty_id,))
                row = cursor.fetchone()
                if faculty_id.isdigit():
                    if len(first_name) > 1 and len(last_name)>1:
                        if validate_email(email_id, check_deliverability=True):
                            if len(phone_no) == 10:
                                if phone_no.isdigit():
                                    # Execute INSERT query
                                    sql = "UPDATE Faculty SET Faculty_first_name=%s, Faculty_last_name=%s, Faculty_id=%s, Email=%s, phone_no=%s WHERE Faculty_id=%s"
                                    values = (first_name, last_name, faculty_id, email_id, phone_no, faculty_id)

                                    cursor.execute(sql, values)

                                    # Commit the transaction
                                    mydb.commit()

                                    # Fetch the last inserted record
                                    cursor.execute("SELECT * FROM Faculty ORDER BY Faculty_id DESC LIMIT 1")
                                    row = cursor.fetchone()

                                    # Insert the new data into the right-side table
                                    rtv1.delete(item)  # Remove the selected item
                                    rtv1.insert("", tk.END, values=(faculty_id,
                                    first_name, last_name,  email_id,
                                    phone_no))  # Insert the updated data

                                    # Close the cursor and connection
                                    cursor.close()
                                    mydb.close()

                                    messagebox.showinfo("Success", "Faculty details added", parent=facultyProfile_win)
                                else:
                                    messagebox.showerror("Error", "Phone number must be a long integer")
                            else:
                                messagebox.showerror("Error", "Phone No. should be minimum 10 digits.")
                        elif EmailNotValidError:
                            messagebox.showerror("Error",
                                                         "Email is not valid, please enter a valid email address")
                    else:
                        messagebox.showerror("Error", "Name should be minimum 2 letters.")
                else:
                    messagebox.showerror("Error", "ID should be a number")

            except EmailNotValidError as er1:
                messagebox.showerror("Error", "Email is not valid.")

            except Exception as e:
                # Print error message
                print(f"Error updating data: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                mydb.close()

        def reset_data():
            # Clear all input fields
            e2.delete(0, tk.END)
            e3.delete(0, tk.END)
            e4.delete(0, tk.END)
            e5.delete(0, tk.END)
            e6.delete(0, tk.END)

        def search():
            global search_performed
            try:
                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )

                # Create a cursor object
                cursor = mydb.cursor()

                # Get the selected search option and the entered value
                selected_option = rcombo1.get()
                search_value = rentry1.get()

                # Construct the SQL query based on the selected option
                if selected_option == "Faculty ID":
                    sql = f"SELECT * FROM Faculty WHERE Faculty_id = {search_value}"
                elif selected_option == "First Name":
                    sql = f"SELECT * FROM Faculty WHERE First_name LIKE '%{search_value}%'"
                else:
                    return  # Invalid search option

                # Execute the SELECT query
                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                # Clear the existing data in the right-side table

                rtv1.delete(*rtv1.get_children())
                # Insert the new data into the right-side table
                for row in rows:
                    rtv1.insert("", tk.END, values=row)
                search_performed = False
            except Exception as e:
                # Print error message
                print(f"Error searching data: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                mydb.close()

        def show_all():
            # global search_performed, cursor, mydb
            try:
                # Connect to the MySQL database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="major_project"
                )

                # Create a cursor object
                cursor = mydb.cursor()

                # Execute SELECT query
                sql = "SELECT * FROM Faculty ORDER BY Faculty_id ASC";
                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                rtv1.delete(*rtv1.get_children())

                # Insert the new data into the right-side table
                for row in rows:
                    rtv1.insert("", tk.END, values=row)
                # search_performed=False
            except Exception as e:
                # Print error message
                print(f"Error fetching data: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                mydb.close()

        # def display_data():
        #     # Connect to the MySQL database
        #     mydb = mysql.connector.connect(
        #         host="localhost",
        #         user="root",
        #         password="nikita@2002",
        #         database="major_project"
        #     )

        #     # Create a cursor object
        #     cursor = mydb.cursor()

        #     # Execute SELECT query
        #     sql = "SELECT * FROM Student"
        #     cursor.execute(sql)

        #     # Fetch all the rows
        #     rows = cursor.fetchall()

        #     # Clear the existing data in the right-side table

        #     # Insert the new data into the right-side table
        #     for row in rows:
        #         rtv1.insert("", tk.END, values=row)

        #     # Close the cursor and connection
        #     cursor.close()
        #     mydb.close()

        facultyProfile_win = tk.Tk()
        facultyProfile_win.geometry("1300x590+125+50")
        facultyProfile_win.title("Faculty Profile")
        h1 = ("Arial", "40")
        f1 = ("Arial", "16")
        f2 = ("Arial", "14")

        frame_top = tk.Frame(facultyProfile_win, highlightbackground="black", highlightthickness=1)
        frame_top.grid(row=0, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")

        frame_left = tk.Frame(facultyProfile_win, highlightbackground="black", highlightthickness=1)
        frame_left.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        frame_left_1 = tk.Frame(frame_left, highlightbackground="black")
        frame_left_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_left_2 = tk.Frame(frame_left, highlightbackground="black")
        frame_left_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        frame_right = tk.Frame(facultyProfile_win, highlightbackground="black", highlightthickness=1)
        frame_right.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        frame_right_1 = tk.Frame(frame_right, highlightbackground="black")
        frame_right_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_right_2 = tk.Frame(frame_right, highlightbackground="black")
        frame_right_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Widgets for the top frame
        label_top = tk.Label(frame_top, text="Faculty Profile", bg="lightblue", font=h1)
        label_top.pack(anchor="center")

        # Widgets for the left frame
        '''class_options = ["FE Comps A", "FE Comps B", "FE Comps C", "SE Comps A", "SE Comps B", "SE Comps C",
                         "TE Comps A", "TE Comps B", "TE Comps C", "BE Comps A", "BE Comps B", "BE Comps C"]
        l1 = tk.Label(frame_left_1, text="Class: ", font=f1)
        l1.grid(row=0, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e1 = ttk.Combobox(frame_left_1, values=class_options, width=25, font=f2)
        e1.grid(row=0, column=2, padx=0, pady=10, columnspan=2, sticky="e")'''

        l4 = tk.Label(frame_left_1, text="Faculty ID: ", font=f1)
        l4.grid(row=1, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e4 = ttk.Entry(frame_left_1, width=26, font=f2)
        e4.grid(row=1, column=2, padx=0, pady=10, columnspan=2, sticky="e")

        l2 = tk.Label(frame_left_1, text="First Name: ", font=f1)
        l2.grid(row=2, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e2 = ttk.Entry(frame_left_1, width=26, font=f2)
        e2.grid(row=2, column=2, padx=0, pady=10, columnspan=2, sticky="e")

        l3 = tk.Label(frame_left_1, text="Last Name: ", font=f1)
        l3.grid(row=3, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e3 = ttk.Entry(frame_left_1, width=26, font=f2)
        e3.grid(row=3, column=2, padx=0, pady=10, columnspan=2, sticky="e")

        l5 = tk.Label(frame_left_1, text="Email ID: ", font=f1)
        l5.grid(row=4, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e5 = ttk.Entry(frame_left_1, width=26, font=f2)
        e5.grid(row=4, column=2, padx=0, pady=10, columnspan=2, sticky="e")

        l6 = tk.Label(frame_left_1, text="Phone No: ", font=f1)
        l6.grid(row=5, column=0, padx=0, pady=10, columnspan=2, sticky="w")
        e6 = ttk.Entry(frame_left_1, width=26, font=f2)
        e6.grid(row=5, column=2, padx=0, pady=10, columnspan=2, sticky="e")

        e9 = tk.Button(frame_left_2, command=save_data, text="Save", font=f1, width=8)
        e9.grid(row=9, column=0, padx=3, pady=10, columnspan=1, sticky="nsew")
        e10 = tk.Button(frame_left_2, command=update_data, text="Update", font=f1, width=8)
        e10.grid(row=9, column=1, padx=3, pady=10, columnspan=1, sticky="nsew")
        e11 = tk.Button(frame_left_2, command=delete_data, text="Delete", font=f1, width=8)
        e11.grid(row=9, column=2, padx=3, pady=10, columnspan=1, sticky="nsew")
        e12 = tk.Button(frame_left_2, command=reset_data, text="Reset", font=f1, width=8)
        e12.grid(row=9, column=3, padx=3, pady=10, columnspan=1, sticky="nsew")

        '''e13 = tk.Button(frame_left_2, text="Take Photo Sample", font=f1, width=10)
        e13.grid(row=10, column=0, padx=3, pady=10, columnspan=2, sticky="nsew")
        e14 = tk.Button(frame_left_2, text="Upload Photo Sample", font=f1, width=10)
        e14.grid(row=10, column=2, padx=3, pady=10, columnspan=2, sticky="nsew")'''

        # Widgets for the right frame 1
        search_options = ["Faculty ID", "Faculty Name"]
        rlabel1 = tk.Label(frame_right_1, text="Search: ", font=f1)
        rlabel1.grid(row=0, column=0, padx=3, pady=10, sticky="nsew")
        rcombo1 = ttk.Combobox(frame_right_1, values=search_options, font=f1)
        rcombo1.grid(row=0, column=1, padx=3, pady=10, sticky="nsew")
        rentry1 = tk.Entry(frame_right_1, font=f1)
        rentry1.grid(row=0, column=2, padx=3, pady=10, sticky="nsew")
        rb1 = tk.Button(frame_right_1, text="Search", command=search, font=f1)
        rb1.grid(row=1, column=1, padx=3, pady=10, sticky="nsew")
        rb2 = tk.Button(frame_right_1, text="Show all", command=show_all, font=f1)
        rb2.grid(row=1, column=2, padx=3, pady=10, sticky="nsew")

        # Widgets for the right frame 2
        rlabel2 = tk.Label(frame_right_2, text="Searching System ", font=f1)
        rlabel2.grid(row=0, column=0, padx=3, pady=10, sticky="nsew")

        """
        view_sb = tk.Scrollbar(rtv1, bd=5, width=10)

        """

        rtv1 = ttk.Treeview(frame_right_2, bootstyle="primary")
        rtv1.grid(row=1, column=0, padx=3, pady=10, sticky="nsew")

        vsb = ttk.Scrollbar(frame_right_2, orient="vertical", command=rtv1.yview)
        vsb.grid(row=1, column=0, padx=3, sticky="e", pady=10)

        rtv1.configure(yscrollcommand=vsb.set)
        # defining columns
        rtv1["columns"] = ("Faculty ID", "First Name", "Last Name", "Email ID", "Phone No")
        # formatting columns
        rtv1.column("#0", width=0, stretch=NO)
        rtv1.column("Faculty ID", anchor=W, width=100, stretch=NO)
        rtv1.column("First Name", anchor=W, width=70, stretch=NO)
        rtv1.column("Last Name", anchor=CENTER, width=90, stretch=NO)
        rtv1.column("Email ID", anchor=W, width=200, stretch=NO)
        rtv1.column("Phone No", anchor=W, width=150, stretch=NO)

        # creating headings
        rtv1.heading("#0", text="", anchor=W)
        rtv1.heading("Faculty ID", text="Faculty_ID", anchor=W)
        rtv1.heading("First Name", text="First Name", anchor=W)
        rtv1.heading("Last Name", text="Last Name", anchor=W)
        rtv1.heading("Email ID", text="Email ID", anchor=W)
        rtv1.heading("Phone No", text="Phone No", anchor=W)

        rtv1.bind("<ButtonRelease-1>", on_item_click)

        # Back Button

        rb3 = tk.Button(frame_right_2, text="Back", font=f1, width=20, command=back)
        rb3.grid(row=2, column=0, padx=3, pady=10)

        display_data()

        # Configure column and row weights to fit to window
        facultyProfile_win.columnconfigure(0, weight=2)
        facultyProfile_win.columnconfigure(1, weight=4)
        facultyProfile_win.rowconfigure(0, weight=0)
        facultyProfile_win.rowconfigure(1, weight=0)

        facultyProfile_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)


#facultyProfile_Page()