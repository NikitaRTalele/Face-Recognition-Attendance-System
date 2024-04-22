import tkinter as tk
from tkinter import messagebox
from Faculty_Subject_Assignment import faculty_subject_assignment_page
from faculty_sub_assignment1 import faculty_subject_assignment1
import adminHome

def assignSubject_Page():
    try:
        def back():
            assignSub_win.destroy()
            adminHome.adminHomePage().alogin_win.deiconify()

        def faculty_subject_assign():
            assignSub_win.withdraw()
            faculty_subject_assignment1()

        def faculty_subject_view():
            assignSub_win.withdraw()
            faculty_subject_assignment_page()

        assignSub_win = tk.Tk()
        assignSub_win.title("Assign Subjects")
        assignSub_win.geometry("500x200+600+250")

        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        # Create a frame to hold the buttons
        frame = tk.Frame(assignSub_win)
        frame.pack(expand=True)

        # Create the buttons
        b1 = tk.Button(frame, font=f1, text="Faculty", bg="purple", fg="white", command=faculty_subject_assign)
        b1.grid(row=0, column=0, padx=10, pady=10)

        b2 = tk.Button(frame, font=f1, text="Faculty Subject View", bg="Yellow", fg="white", command=faculty_subject_view)
        b2.grid(row=0, column=1, padx=10, pady=10)


        b3 = tk.Button(frame, font=f1, text="Back", bg="light blue", fg="black", command=back)
        b3.grid(row=1, column=1, padx=10, pady=10)

        # Center the frame in the window
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        assignSub_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", e)

