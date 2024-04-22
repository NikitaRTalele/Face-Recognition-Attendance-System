import tkinter as tk
from tkinter import *
from ttkbootstrap import Style, ttk, DateEntry

root = Tk()
root.title("Student Subject Allotment")
root.geometry("800x500+440+170")

frame1 = ttk.Frame(root, borderwidth=2, relief="solid",)
frame1.grid(row=1, column=0, sticky="nsew")


root.mainloop()
