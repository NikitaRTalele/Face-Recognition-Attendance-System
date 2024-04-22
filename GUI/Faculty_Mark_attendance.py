import tkinter as tk
from ttkbootstrap import Style, ttk
from tkinter import messagebox
import mysql.connector
import login
from itertools import chain
import datetime
import tkinter as tk
from ttkbootstrap import Style, ttk
from tkinter import messagebox
import mysql.connector
from itertools import chain
import datetime
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
import csv

def faculty_mark_attendance():
    try:
        recognized_student_ids = set()
        def start_attendance():
            faculty_id = faculty_id_entry.get()
            class_name = class_name_entry.get()
            sem = sem_entry.get()
            time_slot = time_slot_entry.get()
            subject_name = subject_name_entry.get()

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )   
            cursor = conn.cursor()

            sql = "SELECT Class_id FROM master_class WHERE Class_name = %s and term = %s"
            cursor.execute(sql, (class_name,sem))
            class_id_result = cursor.fetchone()  # Fetch the result
            if class_id_result:
                class_id = class_id_result[0]  # Extracting class_id from the tuple
                # print(class_id+" class Id")
            else:
                messagebox.showerror("Error", "Class not found!")
                return

            # Code from LBPH+Mobilenet.py
        # Load Face Detection Model
            face_cascade = cv2.CascadeClassifier(r'C:\Project - Copy\Face_Antispoofing_System\models\haarcascade_frontalface_default.xml')
        # Load Anti-Spoofing Model graph
            json_file = open(r'C:\Project - Copy\Face_Antispoofing_System\antispoofing_models\antispoofing_model.json')
            loaded_model_json = json_file.read()
            json_file.close()
            antispoof_model = model_from_json(loaded_model_json)
            antispoof_model.load_weights(r'C:\Project - Copy\Face_Antispoofing_System\antispoofing_models\antispoofing_model.h5')
            print("Liveness Detection Model loaded from disk")
            # Load Face Recognition Model
            face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            face_recognizer.read('TrainingImageLabel/Trainner22.yml')
            print("Face Recognition Model loaded from disk")
            # Confidence threshold for face recognition
            confidence_threshold = 70  # Adjust this threshold as needed
        # Initialize video capture
            video = cv2.VideoCapture(0)
            # Load student details
            def get_user_names():
                user_names = {}
                with open("StudentDetails/StudentDetails.csv", 'r') as csvFile:
                    reader = csv.reader(csvFile)
                # Skip the header row
                    next(reader, None)
                    for row in reader:
                        if len(row) >= 4 and row[2].strip():  # Assuming the ID is in the third column and NAME in the fifth column
                            try:
                                user_names[int(row[2])] = row[3]
                            except ValueError:
                                print(f"Invalid ID: {row[2]}")
                        else:
                            print("Invalid row format")
                return user_names
            # Get user names
            user_names = get_user_names()

            # Initialize a dictionary to store the count of recognized IDs
            recognized_ids_count = {}
            frame_counter = 0

            # Continue capturing frames until 'q' key is pressed
            while True:
                ret, frame = video.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    face = gray[y:y + h, x:x + w]
                # Perform liveness detection (anti-spoofing) with MobileNetV2
                    resized_face = cv2.resize(frame[y-5:y+h+5, x-5:x+w+5], (160, 160))
                    resized_face = resized_face.astype("float") / 255.0
                    resized_face = np.expand_dims(resized_face, axis=0)
                    preds = antispoof_model.predict(resized_face)[0]
                # Recognize the face using LBPH recognizer
                    Id, conf = face_recognizer.predict(face)
                    if preds > 0.5:
                        label = "spoof"
                        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    else:
                        if conf < confidence_threshold:
                            label = f"ID: {Id}, (Real)"
                            # Increment the count of recognized ID
                            recognized_ids_count[Id] = recognized_ids_count.get(Id, 0) + 1
                        else:
                            label = "Unknown (real)"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 225,0), 2)
                cv2.imshow('Face Recognition and Liveness Detection', frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    # Release video capture and close all windows
                    video.release()
                    cv2.destroyAllWindows()
                    break
                frame_counter += 1
                # If 5 frames have been processed, insert the data into the database
                if frame_counter % 6 == 0 and recognized_ids_count:
                # Get the ID with the highest count
                    most_frequent_id = max(recognized_ids_count, key=recognized_ids_count.get)

                    
                    # sql = "SELECT Class FROM Student WHERE student_id = %s"
                    # cursor.execute(sql, (most_frequent_id,))
                    # recognized_student_class_id = cursor.fetchone()
                    # if recognized_student_class_id is not None:
                    #     recognized_student_class_id = recognized_student_class_id[0]
                    #     if recognized_student_class_id == class_name:
                    #         # Insert the most frequent ID into the database
                    #         try:
                    #             cursor.execute("INSERT INTO attendance (attendance_id,subject_name, faculty_id, Attendance, Date, Timeslot, Student_id, Class_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (subject_name, faculty_id, "P", datetime.datetime.now().strftime("%Y-%m-%d"), time_slot, most_frequent_id, class_id))
                    #             conn.commit()
                    #             print(class_name)
                    #             attendance_id += 1
                    #             recognized_ids_count.clear()  # Clear the dictionary for the next set of frames
                    #             print("Data inserted into database successfully.")
                    #         except:
                    #             print("attendance already marked");
                                
                    #     else:
                    #         print("Please check class")
                    # else:
                    #     print("Error: Student not found in the database.")





                    # Insert the most frequent ID into the database
                    # cursor.execute("INSERT INTO attendance (subject_name, faculty_id, Attendance, Date, Timeslot, Student_id, class_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (subject_name, faculty_id, "P", datetime.datetime.now().strftime("%Y-%m-%d"), time_slot, most_frequent_id, class_id))
                    # conn.commit()
                    # recognized_ids_count.clear()  # Clear the dictionary for the next set of frames
                    # # recognized_ids_count.clear()  # Clear the dictionary for the next set of frames
                    # print("Data inserted into database successfully.")





                    sql_check = "SELECT * FROM attendance WHERE Student_id = %s AND subject_name = %s AND Date = %s AND Timeslot = %s"
                    cursor.execute(sql_check, (most_frequent_id, subject_name, datetime.datetime.now().strftime("%Y-%m-%d"), time_slot))
                    existing_record = cursor.fetchone()
                    print(most_frequent_id)

                    if existing_record: 
                        print("Attendance already marked for this student.")
                    else:
                        # Check if the student belongs to the specified class
                        sql_class_check = "SELECT Class FROM Student WHERE student_id = %s"
                        cursor.execute(sql_class_check, (most_frequent_id,))
                        recognized_student_class_id = cursor.fetchone()
                        # print(recognized_student_class_id);

                        if recognized_student_class_id is not None:
                            recognized_student_class_id = recognized_student_class_id[0]
        
                            if recognized_student_class_id == class_name:
                                # Insert the new attendance record into the database
                                sql_insert = "INSERT INTO attendance (subject_name, faculty_id, Attendance, Date, Timeslot, Student_id, Class_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                cursor.execute(sql_insert, (subject_name, faculty_id, "P", datetime.datetime.now().strftime("%Y-%m-%d"), time_slot, most_frequent_id, class_id))
                                conn.commit()
                                recognized_ids_count.clear()  # Clear the dictionary for the next set of frames
                                print("Data inserted into database successfully.")
                            else:
                                print("Please check class")
                        else:
                            print("Error: Student not found in the database.")




    

        recognized_student_ids.clear()
        def back():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            subject_name = subject_name_entry.get()
            faculty_id = faculty_id_entry.get()
            current_date = datetime.date.today()
            date = current_date.strftime("%d-%m-%Y")
            time = time_slot_entry.get()
            class_name = class_name_entry.get()
            student_name = student_name_entry.get()
            sem = sem_entry.get()

            # fetch student_id from student_name and class_name
            sql = "select student_id from student where student_name = %s and Class = %s"
            values = (student_name, class_name)
            cursor.execute(sql, values)
            student_id = cursor.fetchone()
            student_id = student_id[0]

            # fetch class_id from class name and sem
            sql = "select class_id from master_class where class_name = %s and term = %s"
            values = (class_name, sem)
            cursor.execute(sql, values)
            class_id = cursor.fetchone()
            class_id = class_id[0]
            student_list = []
            present_student_list = []

            if faculty_id:
                if sem:
                    if class_name:
                        if time:
                            if subject_name:
                                sql = "select student_id from Student where Class = %s"
                                value = (class_name,)
                                cursor.execute(sql,value)
                                student_list = cursor.fetchall()
                                student_list = list(chain.from_iterable(student_list))
                                print(student_list)

                                sql = "select student_id from Attendance where Attendance = %s and class_id = %s"
                                values = ("P",class_id)
                                cursor.execute(sql,values)
                                present_student_list = cursor.fetchall()
                                present_student_list = list(chain.from_iterable(present_student_list))
                                print(present_student_list)

                                absent_student_ids = []
                                set1 = set(student_list)
                                set2 = set(present_student_list)
                                absent_student_list = list(set1 - set2)
                                print(absent_student_list)
                                '''for i in absent_student_list:
                                    sql = "select student_id from Student where Student_name = %s"
                                    value = (i,)
                                    cursor.execute(sql,value)
                                    id = cursor.fetchone()
                                    absent_student_ids.append(id)
                                absent_student_ids = list(chain.from_iterable(absent_student_ids))
                                print(absent_student_ids)'''

                                for i in absent_student_list:
                                    sql = "insert into Attendance (subject_name,faculty_id,Attendance,Date,Timeslot,Student_id,Class_id) values (%s,%s,%s,%s,%s,%s,%s)"
                                    values = (subject_name, faculty_id, "A", date, time, i, class_id)
                                    cursor.execute(sql, values)
                                    conn.commit()
                                conn.close()
                                messagebox.showinfo("Success", "Absentees Marked!")
                            else:
                                messagebox.showerror("Error", "Subject not fetched!")
                        else:
                            messagebox.showerror("Error", "Time Slot not selected!")
                    else:
                        messagebox.showerror("Error", "Class not selected!")
                else:
                    messagebox.showerror("Error", "Semester not selected")
            else:
                messagebox.showerror("Error", "Faculty_ID not found!")

            root.destroy()

        def fetch_details():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            # Fetch faculty_id and display it
            sql = "select Faculty_id from faculty where Email=%s"
            username1 = login.username
            value = (username1,)
            cursor.execute(sql,value)
            faculty_id = cursor.fetchone()
            print(faculty_id[0])

            default_text_1 = faculty_id[0]
            faculty_id_entry.delete(0, tk.END)  # Clear any existing text
            faculty_id_entry.insert(0, default_text_1)  # Insert the default value
            faculty_id_entry.config(state=tk.DISABLED)

            # Fetch class_name according to faculty_id and display it
            sql = "select Class_id from subject_allocation where Faculty_id = %s"
            value = (faculty_id[0],)
            cursor.execute(sql,value)
            class_ids = cursor.fetchall()
            print(class_ids)

            class_ids_list = list(chain.from_iterable(class_ids))
            print(class_ids_list)
            for i in class_ids_list:
                sql = "select Class_name from master_class where Class_id = %s"
                value = (i,)
                cursor.execute(sql,value)
                class_name = cursor.fetchone()
                class_name_values.extend(class_name)
            print(class_name_values)
            class_name_entry['values'] = class_name_values

        def fetch_subject():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            faculty_id = faculty_id_entry.get()
            class_name = class_name_entry.get()
            time_slot = time_slot_entry.get()
            sem = sem_entry.get()
            if faculty_id and class_name and time_slot and sem:
                #fetch class_id by matching class_name and sem
                sql = "select Class_id from master_class where Class_name = %s and Term = %s"
                values = (class_name,sem)
                cursor.execute(sql,values)
                class_id = cursor.fetchone()
                # select subject_name from subject_allocation by matching faculty_id and class_id
                sql = "select Subject_name from subject_allocation where faculty_id = %s and Class_id = %s"
                values = (faculty_id,class_id[0])
                cursor.execute(sql,values)
                subject_name = cursor.fetchone()
                if subject_name:
                    default_text_2 = subject_name[0]
                    subject_name_entry.delete(0, tk.END)  # Clear any existing text
                    subject_name_entry.insert(0, default_text_2)  # Insert the default value
                    subject_name_entry.config(state=tk.DISABLED)

                    # Fetch students to dropdown
                    sql = "select Student_name from Student where Class = %s"
                    value = (class_name,)
                    cursor.execute(sql,value)
                    student_names = cursor.fetchall()
                    student_names_list = list(chain.from_iterable(student_names))
                    student_name_entry['values'] = student_names_list
                else:
                    messagebox.showerror("Error","Subject not assigned to particular faculty.")
            else:
                messagebox.showerror("Error","Fill all entries")

        def mark_attendance():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="major_project"
            )
            cursor = conn.cursor()

            subject_name = subject_name_entry.get()
            faculty_id = faculty_id_entry.get()
            current_date = datetime.date.today()
            date = current_date.strftime("%d-%m-%Y")
            time = time_slot_entry.get()
            class_name = class_name_entry.get()
            student_name = student_name_entry.get()
            sem = sem_entry.get()

            # fetch student_id from student_name and class_name
            sql = "select student_id from student where student_name = %s and Class = %s"
            values = (student_name,class_name)
            cursor.execute(sql,values)
            student_id = cursor.fetchone()
            student_id = student_id[0]

            # fetch class_id from class name and sem
            sql = "select class_id from master_class where class_name = %s and term = %s"
            values = (class_name,sem)
            cursor.execute(sql,values)
            class_id = cursor.fetchone()
            class_id = class_id[0]

            if faculty_id:
                if sem:
                    if class_name:
                        if time:
                            if subject_name:
                                if student_name:
                                    sql = "insert into Attendance (subject_name,faculty_id,Attendance,Date,Timeslot,Student_id,Class_id) values (%s,%s,%s,%s,%s,%s,%s)"
                                    values = (subject_name,faculty_id,"P",date,time,student_id,class_id)
                                    cursor.execute(sql,values)
                                    conn.commit()
                                    conn.close()
                                    messagebox.showinfo("Success","Attendance Marked Successfully!")
                                else:
                                    messagebox.showerror("Error","Student not selected")
                            else:
                                messagebox.showerror("Error","Subject not fetched!")
                        else:
                            messagebox.showerror("Error","Time Slot not selected!")
                    else:
                        messagebox.showerror("Error","Class not selected!")
                else:
                    messagebox.showerror("Error","Semester not selected")
            else:
                messagebox.showerror("Error","Faculty_ID not found!")



        root = tk.Tk()
        root.title("Mark Attendance")
        root.geometry("600x350+550+250")
        style = Style(theme="yeti")

        # Left Frame
        frame1 = ttk.Frame(root, borderwidth=0, relief="solid")
        frame1.grid(row=1, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)

        faculty_id_label = ttk.Label(frame1, text="Faculty ID", font=("Helvetica", 12))
        faculty_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        faculty_id_entry = ttk.Entry(frame1, font=("Helvetica", 12))
        faculty_id_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        sem_label = ttk.Label(frame1, text="Semester", font=("Helvetica", 12))
        sem_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        sem_entry = ttk.Combobox(frame1, values=["I","II"],
                                        width=34)
        sem_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        class_name_values = []
        class_name_label = ttk.Label(frame1, text="Class name", font=("Helvetica", 12))
        class_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        class_name_entry = ttk.Combobox(frame1, values=class_name_values,
                                        width=34)
        class_name_entry.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        time_slot_label = ttk.Label(frame1, text="Time Slot", font=("Helvetica", 12))
        time_slot_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        time_slot_entry = ttk.Combobox(frame1, values=["9.00 - 10.00", "10.00 - 11.00", "11.15 - 12.15",
                                                        "12.15 - 13.15", "13.45 - 14.45", "13.45 - 15.45",
                                                        "14.45 - 15.45", "16.00 - 18.00"],
                                       width=34)
        time_slot_entry.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        subject_names_list = []
        subject_name_label = ttk.Label(frame1, text="Subject name", font=("Helvetica", 12))
        subject_name_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        subject_name_entry = ttk.Entry(frame1, width=34)
        subject_name_entry.grid(row=4, column=1, sticky="e", padx=10, pady=5)

        student_name_values = []
        student_name_label = ttk.Label(frame1, text="Student names", font=("Helvetica", 12))
        student_name_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        student_name_entry = ttk.Combobox(frame1, values=student_name_values, width=34)
        student_name_entry.grid(row=5, column=1, sticky="e", padx=10, pady=5)

        fetch_sub_button = ttk.Button(frame1, text="Fetch Subject", width=20, style="dark", command=fetch_subject)
        fetch_sub_button.grid(row=6, column=0, columnspan=1, pady=3, padx=3)

        mark_button = ttk.Button(frame1, text="Mark Attendance", width=20, style="dark", command=mark_attendance)
        mark_button.grid(row=6, column=1, columnspan=1, pady=3, padx=3)

        back_button = ttk.Button(frame1, text="Back", width=20, style="dark", command=back)
        back_button.grid(row=7, column=0, columnspan=2, pady=3, padx=3)

        # Right Frame
        frame2 = ttk.Frame(root, borderwidth=0, relief="solid")
        frame2.grid(row=1, column=1, sticky="nsew")
        root.columnconfigure(1, weight=9)
        start_button = ttk.Button(frame1, text="Start Attendance", width=20, style="dark", command=start_attendance)
        start_button.grid(row=8, column=0, columnspan=2, pady=3, padx=3)
        

        frame6 = ttk.Frame(frame2, borderwidth=0, relief="solid")
        frame6.grid(row=1, column=0, sticky="nsew")
        root.columnconfigure(1, weight=9)

        label_name = ttk.Label(frame2, text="Mark Attendance", font=("Helvetica", 14,"bold"))
        label_name.grid(row=0, column=0, sticky="w", padx=10, pady=3)

        def on_button_click():
            print("Button clicked!")

        def on_enter(event):
            canvas.config(cursor="hand2")

        def on_leave(event):
            canvas.config(cursor="")

        def create_round_button(canvas, x, y, radius, text, outline_width=2):
            button = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue", outline="black", width=outline_width)
            text = canvas.create_text(x, y, text=text, font=("Helvetica", 12), anchor="center")
            return button, text

        # Create a Canvas widget
        canvas = tk.Canvas(frame6, width=200, height=200, bg="white")
        canvas.pack()

        # Create a round button on the canvas
        button, text = create_round_button(canvas, 100, 100, 90, "    Click here to\nMark Attendance!!", outline_width=4)

        # Bind events to change cursor
        canvas.tag_bind(button, "<Button-1>", lambda event: on_button_click())
        canvas.tag_bind(button, "<Enter>", on_enter)
        canvas.tag_bind(button, "<Leave>", on_leave)

        title_label = ttk.Label(root, text="MARK STUDENT ATTENDANCE", font=("Helvetica", 20, "bold"), style="TLabel", padding=20)
        title_label.grid(row=0, column=0, columnspan=2)

        fetch_details()

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))

#faculty_mark_attendance()