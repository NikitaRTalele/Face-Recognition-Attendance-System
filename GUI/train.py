import tkinter as tk
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
import cv2
import os
import csv
from tkinter import messagebox,filedialog
import datetime
from PIL import Image
import numpy as np
from tkinter import messagebox as mess
from sklearn.metrics import accuracy_score
import adminHome

# import adminHome

root = tk.Tk()
root.geometry("1300x590+125+50")
root.title("Student Profile")
h1 = ("Arial", "40")
f1 = ("Arial", "16")
f2 = ("Arial", "14")


def train_page():
    return 
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

# Widgets for the top frame
label_top = tk.Label(frame_top, text="Student Profile", bg="lightblue", font=h1)
label_top.pack(anchor="center")

# Widgets for the left frame
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

e9 = tk.Button(frame_left_2, text="Save", font=f1, width=8)  # command=save_data
e9.grid(row=9, column=0, padx=3, pady=10, columnspan=1, sticky="nsew")
e10 = tk.Button(frame_left_2, text="Update", font=f1, width=8)  # command=update_data
e10.grid(row=9, column=1, padx=3, pady=10, columnspan=1, sticky="nsew")
e11 = tk.Button(frame_left_2, text="Delete", font=f1, width=8)  # command=delete_data,
e11.grid(row=9, column=2, padx=3, pady=10, columnspan=1, sticky="nsew")
e12 = tk.Button(frame_left_2, text="Reset", font=f1, width=8)  # command=reset_data,
e12.grid(row=9, column=3, padx=3, pady=10, columnspan=1, sticky="nsew")

e13 = tk.Button(frame_left_2, text="Take Photo Sample", command=TakeImages, font=f1, width=15)
e13.grid(row=10, column=0, padx=3, pady=10, columnspan=2, sticky="nsew")
e14 = tk.Button(frame_left_2, text="Train Images",command=TrainImages, font=f1, width=15)
e14.grid(row=10, column=2, padx=3, pady=10, columnspan=2, sticky="nsew")


# Widgets for the right frame 1
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

# Configure column and row weights to fit to window
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=4)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)

root.mainloop()




