import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
from tkinter import simpledialog
import mysql.connector
import login
import facultyHome
from tkinter import filedialog

def faculty_attendance_view_page():
    try:
        def pick_date():
            # Function to open a dialog box to pick a date
            selected_date = simpledialog.askstring("Pick a Date", "Enter a date (DD-MM-YYYY):", parent=root)
            if selected_date:
                date_entry.delete(0, tk.END)
                date_entry.insert(0, selected_date)

        def display_data():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            username = login.username
            sql = "select faculty_id from Faculty where Email=%s"
            value = (username,)
            cursor.execute(sql,value)
            faculty_id = cursor.fetchone()
            faculty_id = faculty_id[0]

            sql = "select * from Attendance where Faculty_id = %s"
            value = (faculty_id,)
            cursor.execute(sql, value)
            data = cursor.fetchall()
            for row in tree.get_children():
                tree.delete(row)

                # Insert new data into treeview
            for item in data:
                tree.insert("", tk.END, values=item)

        def item_on_click(event):
            # Get selected item
            selected_item = tree.focus()
            if selected_item:
                # Get item values
                values = tree.item(selected_item, 'values')
                # Insert values into entry fields
                attendance_id_entry.delete(0, tk.END)
                attendance_id_entry.insert(0, values[0])

                subject_name_entry.delete(0, tk.END)
                subject_name_entry.insert(0, values[1])

                faculty_id_entry.delete(0, tk.END)
                faculty_id_entry.insert(0, values[2])

                attendance_status_entry.set(values[3])

                date_entry.delete(0, tk.END)
                date_entry.insert(0, values[4])

                timeslot_entry.set(values[5])

                student_id_entry.delete(0, tk.END)
                student_id_entry.insert(0, values[6])

                class_id_entry.delete(0, tk.END)
                class_id_entry.insert(0, values[7])

                # Disable entry widgets
                attendance_id_entry.configure(state="disabled")
                subject_name_entry.configure(state="disabled")
                faculty_id_entry.configure(state="disabled")
                date_entry.configure(state="disabled")
                timeslot_entry.configure(state="disabled")
                student_id_entry.configure(state="disabled")
                class_id_entry.configure(state="disabled")

        def update_data():
            attendance_id = attendance_id_entry.get()
            attendance_status = attendance_status_entry.get()

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            if attendance_id and attendance_status:
                sql = "update Attendance SET Attendance = %s where Attendance_id = %s"
                values = (attendance_status,attendance_id)
                cursor.execute(sql, values)
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Student Attendance updated successfully!")
            else:
                messagebox.showerror("Error","Fetch Student first")

        def back():
            root.destroy()
            facultyHome.facultyHomePage().facultyHome_win.deiconify()

        def reset():
            # Enable entry widgets
            attendance_id_entry.configure(state="normal")
            subject_name_entry.configure(state="normal")
            faculty_id_entry.configure(state="normal")
            date_entry.configure(state="normal")
            timeslot_entry.configure(state="normal")
            student_id_entry.configure(state="normal")
            class_id_entry.configure(state="normal")

            # Clear all entry widgets
            attendance_id_entry.delete(0, tk.END)
            subject_name_entry.delete(0, tk.END)
            faculty_id_entry.delete(0, tk.END)
            attendance_status_entry.set("")
            date_entry.delete(0, tk.END)
            timeslot_entry.set("")
            student_id_entry.delete(0, tk.END)
            class_id_entry.delete(0, tk.END)

        def export_to_csv():
            # Open a file dialog for saving the CSV file
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                # Open the CSV file in write mode
                with open(filename, 'w', newline='') as csvfile:
                    # Create a CSV writer object
                    csv_writer = csv.writer(csvfile)

                    # Write the header row
                    header = [tree.heading(column)["text"] for column in tree["columns"]]
                    csv_writer.writerow(header)

                    # Write data rows
                    for item in tree.get_children():
                        values = tree.item(item, 'values')
                        csv_writer.writerow(values)

        def import_csv():
            # Establish a connection to the MySQL database
            filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not filename:
                return  # No file selected, exit function

            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Open the CSV file and read its contents
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the header row

                # Iterate over each row in the CSV file
                for row in csv_reader:
                    # Insert data into the database table
                    cursor.execute("INSERT INTO Attendance (Attendance_id, subject_name, faculty_id, Attendance, Date, Timeslot, Student_id, Class_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", row)

            # Commit changes to the database
            conn.commit()

            # Close the cursor and database connection
            cursor.close()
            conn.close()

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
                if selected_option == "Subject Name":
                    sql = f"SELECT * FROM Attendance WHERE subject_name LIKE %{search_value}%"
                elif selected_option == "Student ID":
                    sql = f"SELECT * FROM Attendance WHERE Student_id = {search_value}"
                elif selected_option == "Class ID":
                    sql = f"SELECT * FROM Attendance WHERE Class_id = {search_value}"
                else:
                    return  # Invalid search option

                # Execute the SELECT query
                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                # Clear the existing data in the right-side table

                tree.delete(*tree.get_children())
                # Insert the new data into the right-side table
                for row in rows:
                    tree.insert("", tk.END, values=row)
                search_performed = False
            except Exception as e:
                # Print error message
                print(f"Error searching data: {e}")



        def show_all():
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
                sql = "SELECT * FROM Attendance ORDER BY Attendance_id ASC";

                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                tree.delete(*tree.get_children())

                # Insert the new data into the right-side table
                for row in rows:
                    tree.insert("", tk.END, values=row)
                # search_performed=False
            except Exception as e:
                # Print error message
                print(f"Error fetching data: {e}")

        root = tk.Tk()
        root.title("Faculty Attendance View")

        # Main frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame
        left_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE)
        left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)

        # Left labels and entries
        attendance_id_label = tk.Label(left_frame, text="Attendance ID", font=("Helvetica", 14))
        attendance_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        attendance_id_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        attendance_id_entry.grid(row=0, column=1, sticky="we", padx=5, pady=2)

        subject_name_label = tk.Label(left_frame, text="Subject Name", font=("Helvetica", 14))
        subject_name_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        subject_name_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        subject_name_entry.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        faculty_id_label = tk.Label(left_frame, text="Faculty ID", font=("Helvetica", 14))
        faculty_id_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        faculty_id_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        faculty_id_entry.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        attendance_status_label = tk.Label(left_frame, text="Attendance Status", font=("Helvetica", 14))
        attendance_status_label.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        attendance_status_entry = ttk.Combobox(left_frame, values=["P", "A"], font=("Helvetica", 14))
        attendance_status_entry.grid(row=3, column=1, sticky="we", padx=5, pady=2)

        date_label = tk.Label(left_frame, text="Date", font=("Helvetica", 14))
        date_label.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        date_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        date_entry.grid(row=4, column=1, sticky="we", padx=5, pady=2)
        date_button = ttk.Button(left_frame, text="Pick Date", command=pick_date)
        date_button.grid(row=4, column=2, padx=5, pady=2)

        timeslot_label = tk.Label(left_frame, text="Timeslot", font=("Helvetica", 14))
        timeslot_label.grid(row=5, column=0, sticky="w", padx=5, pady=2)
        timeslot_entry = ttk.Combobox(left_frame, values=["9.00 - 10.00", "10.00 - 11.00", "11.15 - 12.15",
                                                        "12.15 - 13.15", "13.45 - 14.45", "13.45 - 15.45",
                                                        "14.45 - 15.45", "16.00 - 18.00"], font=("Helvetica", 14))
        timeslot_entry.grid(row=5, column=1, sticky="we", padx=5, pady=2)

        student_id_label = tk.Label(left_frame, text="Student ID", font=("Helvetica", 14))
        student_id_label.grid(row=6, column=0, sticky="w", padx=5, pady=2)
        student_id_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        student_id_entry.grid(row=6, column=1, sticky="we", padx=5, pady=2)

        class_id_label = tk.Label(left_frame, text="Class ID", font=("Helvetica", 14))
        class_id_label.grid(row=7, column=0, sticky="w", padx=5, pady=2)
        class_id_entry = tk.Entry(left_frame, font=("Helvetica", 14))
        class_id_entry.grid(row=7, column=1, sticky="we", padx=5, pady=2)

        # Control buttons
        submit_button = tk.Button(left_frame, text="Submit", width=10, font=("Helvetica", 14))
        submit_button.grid(row=8, column=0, padx=5, pady=5, sticky="we")

        back_button = tk.Button(left_frame, text="Back", width=10, font=("Helvetica", 14), command=back)
        back_button.grid(row=8, column=1, padx=5, pady=5, sticky="we")

        update_button = tk.Button(left_frame, text="Update", width=10, font=("Helvetica", 14), command=update_data)
        update_button.grid(row=9, column=0, padx=5, pady=5, sticky="we")

        reset_button = tk.Button(left_frame, text="Reset", width=10, font=("Helvetica", 14), command=reset)
        reset_button.grid(row=9, column=1, padx=5, pady=5, sticky="we")

        export_button = tk.Button(left_frame, text="Export CSV", width=10, font=("Helvetica", 14), command=export_to_csv)
        export_button.grid(row=10, column=0, padx=5, pady=5, sticky="we")

        import_button = tk.Button(left_frame, text="Import CSV", width=10, font=("Helvetica", 14), command=import_csv)
        import_button.grid(row=10, column=1, padx=5, pady=5, sticky="we")

        # Right frame
        right_frame = tk.Frame(main_frame, bd=2, relief=tk.GROOVE, width=300)
        right_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Search System label
        search_label = tk.Label(right_frame, text="Search System", font=("Helvetica", 14))
        search_label.grid(row=0, column=0, columnspan=3, pady=5)

        search_options = ["Subject Name", "Student ID", "Class ID"]
        rlabel1 = tk.Label(right_frame, text="Search: ", font=("Helvetica", 14))
        rlabel1.grid(row=1, column=0, padx=3, pady=10, sticky="e")
        rcombo1 = ttk.Combobox(right_frame, values=search_options, font=("Helvetica", 14))
        rcombo1.grid(row=1, column=1, padx=3, pady=10, sticky="we")
        rentry1 = tk.Entry(right_frame, font=("Helvetica", 14))
        rentry1.grid(row=1, column=2, padx=3, pady=10, sticky="we")
        rb1 = tk.Button(right_frame, text="Search", command=search, font=("Helvetica", 14))
        rb1.grid(row=2, column=1, padx=3, pady=10, sticky="we")
        rb2 = tk.Button(right_frame, text="Show all", command=show_all, font=("Helvetica", 14))
        rb2.grid(row=2, column=2, padx=3, pady=10, sticky="we")

        # Treeview
        tree = ttk.Treeview(right_frame, columns=("Attendance ID", "Subject Name", "Faculty ID", "Attendance Status", "Date", "Timeslot", "Student ID", "Class ID"), show="headings")
        tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        tree.bind("<<TreeviewSelect>>", item_on_click)

        # Adding headings to treeview
        for column in tree["columns"]:
            tree.heading(column, text=column)
            tree.column(column, width=100)  # Decrease column width

        # Setting font to Helvetica - 14
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14))

        display_data()

        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error",e)