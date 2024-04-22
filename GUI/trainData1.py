import tkinter as tk
from tkinter import messagebox
import adminHome

import tkinter as tk
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
import cv2
import os
import csv
from tkinter import messagebox, filedialog
import datetime
from PIL import Image
import numpy as np

def train():
    root = tk.Tk()
    root.geometry("1300x590+125+50")
    root.title("Student Profile")
    h1 = ("Arial", "40")
    f1 = ("Arial", "16")
    f2 = ("Arial", "14")

    def show_message_box(title, message):
        messagebox.showinfo(title, message)

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def check_haarcascadefile():
        exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if not exists:
            messagebox.showerror('File Missing', 'haarcascade_frontalface_default.xml not found. Please contact support.')
            root.destroy()

    def take_images():
        check_haarcascadefile()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
        assure_path_exists("StudentDetails/")
        assure_path_exists("TrainingImage/")
        serial = 0
        exists = os.path.isfile("StudentDetails/StudentDetails.csv")
        if exists:
            with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = (serial // 2)
        else:
            with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1

        Id = e2.get()
        name = e3.get()

        if name.isalpha() or ' ' in name:
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0

            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('Taking Images', img)

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 100:
                    break

            cam.release()
            cv2.destroyAllWindows()

            res = f"Images Taken for ID: {Id}"
            row = [serial, '', Id, '', name]

            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)

            show_message_box("Success", res)

        else:
            if not name.isalpha():
                show_message_box("Error", "Enter correct name")

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        Ids = []
        for imagePath in image_paths:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(ID)
        return faces, Ids

    def train_images():
        check_haarcascadefile()
        assure_path_exists("TrainingImageLabel/")
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, ID = get_images_and_labels("resized_trainingImage")
        try:
            recognizer.train(faces, np.array(ID))
        except:
            messagebox.showerror('Error', 'Please Register someone first!!!')
            return
        recognizer.save("TrainingImageLabel\Trainner22.yml")
        show_message_box("Success", "Profile Saved Successfully")

    def upload_photo_sample():
        file_path = filedialog.askopenfilename(title="Select Photo Sample", filetypes=[("Image Files", "*.jpg;*.png")])

        if file_path:
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                image_folder = f"TrainingImage/{timestamp}/"
                assure_path_exists(image_folder)

                image_name = os.path.basename(file_path)
                destination_path = os.path.join(image_folder, image_name)
                os.rename(file_path, destination_path)

                show_message_box("Success", f"Photo Sample '{image_name}' uploaded successfully!")

            except Exception as e:
                error_message = f"Error uploading photo sample: {e}"
                show_message_box("Error", error_message)

    frame_top = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    frame_top.grid(row=0, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")

    frame_left = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    frame_left.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    frame_left_1 = tk.Frame(frame_left, highlightbackground="black")
    frame_left_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_left_2 = tk.Frame(frame_left, highlightbackground="black")
    frame_left_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    frame_right = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    frame_right.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    frame_right_1 = tk.Frame(frame_right, highlightbackground="black")
    frame_right_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame_right_2 = tk.Frame(frame_right, highlightbackground="black")
    frame_right_2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    label_top = tk.Label(frame_top, text="Student Profile", bg="lightblue", font=h1)
    label_top.pack(anchor="center")

    class_options = ["FE Comps A", "FE Comps B", "FE Comps C", "SE Comps A", "SE Comps B", "SE Comps C", "TE Comps A",
                     "TE Comps B", "TE Comps C", "BE Comps A", "BE Comps B", "BE Comps C", "FE I.T A", "FE I.T B",
                     "FE I.T C", "SE I.T A", "SE I.T B", "SE I.T C", "TE I.T A", "TE I.T B", "TE I.T C", "BE I.T A",
                     "BE I.T B", "BE I.T C", "FE Mech A", "FE Mech B", "FE Mech C", "SE Mech A", "SE Mech B", "SE Mech C",
                     "TE Mech A", "TE Mech B", "TE Mech C", "BE Mech A", "BE Mech B", "BE Mech C", "FE Civil A", "FE Civil B",
                     "FE Civil C", "SE Civil A", "SE Civil B", "SE Civil C", "TE Civil A", "TE Civil B", "TE Civil C",
                     "BE Civil A", "BE Civil B", "BE Civil C", "FE EXTC A", "FE EXTC B", "FE EXTC C", "SE EXTC A", "SE EXTC B",
                     "SE EXTC C", "TE EXTC A", "TE EXTC B", "TE EXTC C", "BE EXTC A", "BE EXTC B", "BE EXTC C",
                     "FE Electrical A", "FE Electrical B", "FE Electrical C", "SE Electrical A", "SE Electrical B",
                     "SE Electrical C", "TE Electrical A", "TE Electrical B", "TE Electrical C", "BE Electrical A",
                     "BE Electrical B", "BE Electrical C"]
    l1 = tk.Label(frame_left_1, text="Class: ", font=f1)
    l1.grid(row=0, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e1 = ttk.Combobox(frame_left_1, values=class_options, width=25, font=f2)
    e1.grid(row=0, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    l2 = tk.Label(frame_left_1, text="Student ID: ", font=f1)
    l2.grid(row=1, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e2 = ttk.Entry(frame_left_1, width=26, font=f2)
    e2.grid(row=1, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    l3 = tk.Label(frame_left_1, text="Name: ", font=f1)
    l3.grid(row=2, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e3 = ttk.Entry(frame_left_1, width=26, font=f2)
    e3.grid(row=2, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    l4 = tk.Label(frame_left_1, text="Roll No: ", font=f1)
    l4.grid(row=3, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e4 = ttk.Entry(frame_left_1, width=26, font=f2)
    e4.grid(row=3, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    l5 = tk.Label(frame_left_1, text="Email ID: ", font=f1)
    l5.grid(row=4, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e5 = ttk.Entry(frame_left_1, width=26, font=f2)
    e5.grid(row=4, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    l6 = tk.Label(frame_left_1, text="Phone No: ", font=f1)
    l6.grid(row=5, column=0, padx=0, pady=10, columnspan=2, sticky="w")
    e6 = ttk.Entry(frame_left_1, width=26, font=f2)
    e6.grid(row=5, column=2, padx=0, pady=10, columnspan=2, sticky="e")

    e9 = tk.Button(frame_left_2, text="Save", font=f1, width=8)
    e9.grid(row=9, column=0, padx=3, pady=10, columnspan=1, sticky="nsew")
    e10 = tk.Button(frame_left_2, text="Update", font=f1, width=8)
    e10.grid(row=9, column=1, padx=3, pady=10, columnspan=1, sticky="nsew")
    e11 = tk.Button(frame_left_2, text="Delete", font=f1, width=8)
    e11.grid(row=9, column=2, padx=3, pady=10, columnspan=1, sticky="nsew")
    e12 = tk.Button(frame_left_2, text="Reset", font=f1, width=8)
    e12.grid(row=9, column=3, padx=3, pady=10, columnspan=1, sticky="nsew")

    e13 = tk.Button(frame_left_2, text="Take Photo Sample", command=take_images, font=f1, width=15)
    e13.grid(row=10, column=0, padx=3, pady=10, columnspan=2, sticky="nsew")
    e14 = tk.Button(frame_left_2, text="Train Images", command=train_images, font=f1, width=15)
    e14.grid(row=10, column=2, padx=3, pady=10, columnspan=2, sticky="nsew")
    e15 = tk.Button(frame_left_2, text="Upload Photo Sample", command=upload_photo_sample, font=f1, width=15)
    e15.grid(row=11, column=0, padx=3, pady=10, columnspan=2, sticky="nsew")

    search_options = ["Student ID", "Student Name"]
    rlabel1 = tk.Label(frame_right_1, text="Search: ", font=f1)
    rlabel1.grid(row=0, column=0, padx=3, pady=10, sticky="nsew")
    rcombo1 = ttk.Combobox(frame_right_1, values=search_options, font=f1)
    rcombo1.grid(row=0, column=1, padx=3, pady=10, sticky="nsew")
    rentry1 = tk.Entry(frame_right_1, font=f1)
    rentry1.grid(row=0, column=2, padx=3, pady=10, sticky="nsew")
    rb1 = tk.Button(frame_right_1, text="Search", font=f1)  # command=search
    rb1.grid(row=1, column=1, padx=3, pady=10, sticky="nsew")
    rb2 = tk.Button(frame_right_1, text="Show all", font=f1)  # command=show_all
    rb2.grid(row=1, column=2, padx=3, pady=10, sticky="nsew")


    # Widgets for the right frame 2
    rlabel2 = tk.Label(frame_right_2, text="Searching System ", font=f1)
    rlabel2.grid(row=0, column=0, padx=3, pady=10, sticky="nsew")

    rtv1 = ttk.Treeview(frame_right_2, bootstyle="primary")
    rtv1.grid(row=1, column=0, padx=3, pady=10, sticky="nsew")

    vsb = ttk.Scrollbar(frame_right_2, orient="vertical", command=rtv1.yview)
    vsb.grid(row=1, column=0, padx=3, sticky="e", pady=10)

    rtv1.configure(yscrollcommand=vsb.set)
# defining columns
    rtv1["columns"] = ("Class", "Student ID", "Name", "Roll No", "Email ID", "Phone No")
    # formatting columns
    rtv1.column("#0", width=0, stretch=NO)
    rtv1.column("Class", anchor=W, width=70, stretch=NO)
    rtv1.column("Student ID", anchor=CENTER, width=90, stretch=NO)
    rtv1.column("Name", anchor=W, width=200, stretch=NO)
    rtv1.column("Roll No", anchor=W, width=60, stretch=NO)
    rtv1.column("Email ID", anchor=W, width=150, stretch=NO)
    rtv1.column("Phone No", anchor=W, width=150, stretch=NO)

    # creating headings
    rtv1.heading("#0", text="", anchor=W)


    # creating headings
    rtv1.heading("#0", text="", anchor=W)
    rtv1.heading("Class", text="Class", anchor=W)
    rtv1.heading("Student ID", text="Student ID", anchor=W)
    rtv1.heading("Name", text="Name", anchor=W)
    rtv1.heading("Roll No", text="Roll No", anchor=W)
    rtv1.heading("Email ID", text="Email ID", anchor=W)
    rtv1.heading("Phone No", text="Phone No", anchor=W)

    rtv1.bind("<ButtonRelease-1>",) #on_item_click

    # Back Button

    rb3 = tk.Button(frame_right_2, text="Back", font=f1, width=20)
    rb3.grid(row=2,column=0, padx=3, pady=10)

    # display_data()
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=4)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)


    root.mainloop()

if __name__ == "__main__":
    train()

