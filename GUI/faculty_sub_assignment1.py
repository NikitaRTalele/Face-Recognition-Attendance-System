import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import assignSub

def faculty_subject_assignment1():
    try:
        global selected_subject_var1
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="major_project"
        )
        print(conn)
        cursor = conn.cursor()

        def back():
            facultySub_win.iconify()
            assignSub.assignSubject_Page().assignSub_win.deiconify()

        def save_assignment():
            class_name = class_name_dropdown.get()
            faculty_id = faculty_name_entry.get()
            selected_subject = selected_subject_var1.get()
            term = term_dropdown.get()
            print(class_name)
            print(faculty_id)
            print(selected_subject)
            print(term)

            if class_name and faculty_id and selected_subject and term:
                if faculty_id.isdigit():
                    sql = "SELECT * FROM faculty WHERE Faculty_id = %s"
                    cursor.execute(sql, (faculty_id,))
                    row = cursor.fetchone()
                    if row:
                        sql = "SELECT Class_id FROM master_class WHERE Class_name = %s and Term = %s"
                        cursor.execute(sql, (class_name, term))
                        class_id_row = cursor.fetchall()
                        if class_id_row:
                            class_id = class_id_row[0][0]
                            print(class_id)
                            sql = "INSERT INTO subject_allocation (faculty_id, class_id, subject_name) VALUES (%s, %s, %s)"
                            cursor.execute(sql, (faculty_id, class_id, selected_subject))
                            conn.commit()
                            messagebox.showinfo("Success", "Assignment saved successfully.")

                            faculty_name_entry.delete(0,'end')
                            class_name_dropdown.set('')
                            term_dropdown.set('')

                        else:
                            messagebox.showerror("Error", "Class not found.")
                    else:
                        messagebox.showerror("Error", "Faculty ID does not exist in the database.")
                else:
                    messagebox.showerror("Error", "Faculty ID must be a number.")
            else:
                messagebox.showerror("Error", "Please fill all the fields.")

        def on_next():
            Class_name = class_name_dropdown.get()
            Term_name = term_dropdown.get()
            print(Class_name)
            print(Term_name)
            if Class_name and Term_name:
                sql = "SELECT Subject_1, Subject_2, Subject_3, Subject_4, Subject_5, Subject_6 FROM master_class WHERE Term=%s AND class_name = %s"
                cursor.execute(sql, (Term_name, Class_name))
                row = cursor.fetchone()
                print(row)
                subjects = list(row)
                print(subjects)
                for i in range(len(subjects)):
                    radio_buttons[i]["text"] = subjects[i]
                    radio_buttons[i]["value"] = subjects[i]

                # Perform save operation here
            else:
                messagebox.showerror("Error","Please fill all the fields")

        facultySub_win = tk.Toplevel()
        facultySub_win.title("Faculty Subject Assignment")
        facultySub_win.geometry("420x400+650+270")

        # Create frame 1
        frame1 = ttk.Frame(facultySub_win, padding=(20, 10))
        frame1.pack(fill=tk.BOTH, expand=True)

        # Label for class name
        class_name_label = ttk.Label(frame1, text="Class Name:", font=("Helvetica", 12))
        class_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        # Dropdown for class name
        class_name_var = tk.StringVar()
        class_names = ["FE Comps A", "FE Comps B", "FE Comps C", "SE Comps A", "SE Comps B", "SE Comps C", "TE Comps A", "TE Comps B", "TE Comps C", "BE Comps A", "BE Comps B", "BE Comps C"]  # Example class names
        class_name_dropdown = ttk.Combobox(frame1, textvariable=class_name_var, values=class_names, state="readonly")
        class_name_dropdown.grid(row=1, column=1, padx=5, pady=5)

        term_label = ttk.Label(frame1, text="Term:", font=("Helvetica", 12))
        term_label.grid(row=2, column=0, sticky="w")
        term_dropdown = ttk.Combobox(frame1, values=["I", "II"], width=20)
        term_dropdown.grid(row=2, column=1, sticky="w")

        btn_next = ttk.Button(frame1, text="Next", command=on_next)
        btn_next.grid(row=1, column=2, padx=5, pady=5)

        # Label for faculty name
        faculty_name_label = ttk.Label(frame1, text="Faculty ID:", font=("Helvetica", 12))
        faculty_name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Entry for faculty name
        faculty_name_entry = ttk.Entry(frame1, font=("Helvetica", 12))
        faculty_name_entry.grid(row=0,column=1, padx=5, pady=5)

        # Create frame 2
        frame2 = ttk.Frame(facultySub_win, padding=(20, 10))
        frame2.pack(fill=tk.BOTH, expand=True)

        # Radio button selection variable
        selected_subject_var1 = tk.StringVar()

        # Create radio buttons
        radio_buttons = []

        for i in range(6):
            radio_button = ttk.Radiobutton(frame2, text=f"Subject {i+1}", variable=selected_subject_var1, value=f"Subject {i+1}")
            radio_button.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            radio_buttons.append(radio_button)

        # Create frame 3
        frame3 = ttk.Frame(facultySub_win, padding=(20, 10))
        frame3.pack(fill=tk.BOTH, expand=True)

        # Save button
        save_button = ttk.Button(frame3, text="Save", command=save_assignment, style="TButton", width=10)
        save_button.pack(pady=10)

        back_button = ttk.Button(frame3, text="Back", command=back, style="TButton", width=10)
        back_button.pack(pady=10)

        facultySub_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error",e)

#faculty_subject_assignment1()
