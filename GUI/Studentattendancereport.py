import tkinter as tk
import ttkbootstrap as ttk
import mysql.connector
import login

def student_attendance_report_page():
    def fetch_details():
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="major_project"
        )
        # Create a cursor object
        cursor = conn.cursor()

        # from student_email fetch student_id and Student_name from Student table
        email = login.username
        sql = "select Student_id from Student where Email = %s"
        value = (email,)
        cursor.execute(sql, value)
        Student_id = cursor.fetchone()
        Student_id = Student_id[0]

        sql = "select Student_name from Student where Email = %s"
        value = (email,)
        cursor.execute(sql, value)
        Student_name = cursor.fetchone()
        Student_name = Student_name[0]

        default_text_1 = Student_name
        search_entry.delete(0, tk.END)  # Clear any existing text
        search_entry.insert(0, default_text_1)  # Insert the default value
        search_entry.config(state=tk.DISABLED)

        # from student_id fetch attendance from attendance table
        sql = "select Subject_name, Date, Timeslot, Attendance from Attendance where Student_id = %s"
        value = (Student_id,)
        cursor.execute(sql, value)
        attendance_details = cursor.fetchall()

        for i in attendance_details:
            table.insert("","end", values=i)

    def export_csv():
        # Logic to export CSV file
        print("Exporting CSV file...")

    root = tk.Tk()
    style = ttk.Style(theme="flatly")
    root.title("Student Attendance Report")

    heading_label = ttk.Label(root, text="Student Attendance Report", font=("Helvetica", 18, "bold"))
    heading_label.pack(pady=10)

    heading_line = ttk.Separator(root, orient="horizontal")
    heading_line.pack(fill="x")

    search_frame = ttk.Frame(root)
    search_frame.pack(pady=10, padx=20, anchor="w")

    search_label = ttk.Label(search_frame, text="Student's Name:")
    search_label.grid(row=0, column=0, padx=5)

    search_entry = ttk.Entry(search_frame)
    search_entry.grid(row=0, column=1, padx=5)

    export_button = ttk.Button(root, text="Export CSV", style="success.TButton", command=export_csv)
    export_button.pack(pady=10)

    table_frame = ttk.Frame(root)
    table_frame.pack(padx=20, pady=10)

    table = ttk.Treeview(table_frame, columns=("Subject Name", "Date", "Time Slot", "Attendance Status"))
    table.heading("Subject Name", text="Subject Name")
    table.heading("Date", text="Date")
    table.heading("Time Slot", text="Time Slot")
    table.heading("Attendance Status", text="Attendance Status")
    table.column("#0", width=50, stretch=tk.NO)
    table.column("Subject Name", width=150, stretch=tk.NO)
    table.column("Date", width=100, stretch=tk.NO)
    table.column("Time Slot", width=100, stretch=tk.NO)
    table.column("Attendance Status", width=150, stretch=tk.NO)
    table.pack()

    back_button = ttk.Button(root, text="Back", style="warning.TButton", command=root.quit)
    back_button.pack(pady=10)

    fetch_details()

    root.mainloop()
