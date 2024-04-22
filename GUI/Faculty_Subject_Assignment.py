import tkinter as tk
from tkinter import *
from ttkbootstrap import Style, ttk, DateEntry
from tkinter import messagebox
import mysql.connector
import assignSub
def faculty_subject_assignment_page():

    try:
        #==================================ROOT WINDOW=================================

        root = tk.Tk()
        root.title("Faculty Subjects View")
        style = Style(theme="yeti")

        #=========================RIGHT FRAME================================
        def back():
            root.destroy()
            assignSub.assignSubject_Page().assignSub_win.deiconify()


        def display_data():
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
                sql = "SELECT * FROM subject_allocation ORDER BY allocation_id ASC";
                cursor.execute(sql)

                # Fetch all the rows
                rows = cursor.fetchall()

                table.delete(*table.get_children())

                # Insert the new data into the right-side table
                for row in rows:
                    table.insert("", tk.END, values=row)
                # search_performed=False
            except Exception as e:
                # Print error message
                messagebox.showerror("Error",e)

        def delete_data():
            try:
                # Get the selected item
                item = table.selection()[0]

                # Get values from the selected item
                values = table.item(item, 'values')

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
                sql = "DELETE FROM subject_allocation WHERE allocation_id = %s"
                value = (values[0],)  # Assuming Student ID is the second column
                cursor.execute(sql, value)

                # Commit the transaction
                mydb.commit()

                # Close the cursor and connection

                # Print success message
                print("Data deleted successfully!")

                # Remove the selected item from the Treeview
                table.delete(item)
            except Exception as e:
                # Print error message
                print(f"Error deleting data: {e}")

        def search_data():
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
                selected_option = dropdown_search_by.get()
                search_value = dropdown_search_by.get()

                # Construct the SQL query based on the selected option
                if selected_option == "Faculty_id":
                    sql = f"SELECT * FROM subject_allocation WHERE faculty_id = {search_value}"
                elif selected_option == "Class_Name":
                    sql = f"SELECT * FROM subject_allocation WHERE class_name LIKE '%{search_value}%'"
                elif selected_option == "Subject_Name":
                    sql = f"SELECT * FROM subject_allocation WHERE Subject_name LIKE '%{search_value}%'"
                else:
                    print("Invalid Option")

                # Execute the SELECT query
                cursor.execute(sql,(search_value,))

                # Fetch all the rows
                rows = cursor.fetchall()

                # Clear the existing data in the right-side table

                table.delete(*table.get_children())
                # Insert the new data into the right-side table
                for row in rows:
                    table.insert("", tk.END, values=row)
                search_performed = False
            except Exception as e:
                # Print error message
                print(f"Error searching data: {e}")


        frame2 = ttk.Frame(root, borderwidth=2, relief="solid")
        frame2.grid(row=1, column=1, sticky="nsew")
        root.columnconfigure(1, weight=9)

        # Create a sub-frame for the form
        form_frame = ttk.Frame(frame2, borderwidth=2,padding=(2,2,2, 0))
        form_frame.grid(row=1, column=0, pady=2, padx=3)


        # Create a sub-frame for the form
        form_frame = ttk.Frame(frame2, borderwidth=2, padding=(2, 2, 2, 0))
        form_frame.grid(row=1, column=0, pady=2, padx=3)

        # Create the labels
        label_search_by = ttk.Label(form_frame, text="Search By", font=("Helvetica", 12))
        label_search_by.grid(row=0, column=0, sticky="e", padx=3, pady=0)

        label_search_info = ttk.Label(form_frame, text="Search Info", font=("Helvetica", 12))
        label_search_info.grid(row=0, column=2, sticky="e", padx=3, pady=0)

        # Create the dropdown for "Search By"
        search_by_options = ["Faculty_id", "Class_Name", "Subject_Name"]
        dropdown_search_by = ttk.Combobox(form_frame, values=search_by_options, width=14)
        dropdown_search_by.grid(row=0, column=1, sticky="w", padx=3, pady=0)

        # Create the entry for "Search Info"
        entry_search_info = ttk.Entry(form_frame, width=16)
        entry_search_info.grid(row=0, column=3, sticky="w", padx=3, pady=0)

        search_button = ttk.Button(form_frame, text="Search",bootstyle="primary",width=10, command=search_data)
        search_button.grid(row=1, column=1,padx=10 ,pady=5)

        show_all_button = ttk.Button(form_frame, text="Show all",bootstyle="secondary",width=10)
        show_all_button.grid(row=1, column=3, pady=5,sticky="n")

        table_frame = ttk.Frame(frame2)
        table_frame.grid(row=2, column=0, pady=20, padx=(3, 3))

        columns = ["Allotment ID", "Faculty ID", "Class Name", "Subject name"]

        scrollhor=ttk.Scrollbar(table_frame,orient=HORIZONTAL,bootstyle="info")
        scrollver=ttk.Scrollbar(table_frame,orient=VERTICAL,bootstyle="info")
        table = ttk.Treeview(table_frame, columns=columns, show="headings",height=15,xscrollcommand=scrollhor.set,yscrollcommand=scrollver.set)
        scrollhor.pack(side=BOTTOM,fill=X)
        scrollver.pack(side=RIGHT,fill=Y)
        scrollhor.config(command=table.xview)
        scrollver.config(command=table.yview)

        heading_frame = ttk.Frame(table_frame)

        #making the table
        table.heading("Allotment ID",text="Allotment ID")
        table.heading("Faculty ID",text="Faculty ID")
        table.heading("Class Name", text="Class Name")
        table.heading("Subject name",text="Subject name")

        table["show"]="headings"

        table.column("Allotment ID",width=125)
        table.column("Faculty ID",width=125)
        table.column("Class Name", width=125)
        table.column("Subject name",width=125)

        table.pack(fill=BOTH,expand=10)

        btn_frame = ttk.Frame(frame2)
        btn_frame.grid(row=3, column=0, pady=20, padx=(3, 3))

        delete_button = ttk.Button(btn_frame, text="Delete", width=10, bootstyle="danger", command=delete_data)
        delete_button.grid(row=3, column=0, pady=3, padx=10)

        reset_button = ttk.Button(btn_frame, text="Reset", width=10, bootstyle="warning")
        reset_button.grid(row=3, column=1, pady=3, padx=10)

        Back_button = ttk.Button(btn_frame, text="Back",width=10,bootstyle="dark", command=back)
        Back_button.grid(row=4, column=0,columnspan=2,sticky="nsew",pady=3,padx=3)

        title_label = ttk.Label(root, text="FACULTY SUBJECT ASSIGNMENT", font=("Helvetica", 20, "bold"), style="TLabel", padding=20)
        title_label.grid(row=0, column=0, columnspan=2)

        display_data()

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error",e)

