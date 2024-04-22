import tkinter as tk
from tkinter import messagebox
import login
import mysql.connector
import subprocess


def set_security_page():
    try:
        username1 = login.username
        print(username1)

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database='major_project'
        )
        # wrote this statement to check status of connection with database
        print(conn)
        c1 = conn.cursor()

        sql = "SELECT role FROM login WHERE username = %s"
        val = (username1,)
        c1.execute(sql, val)
        result = c1.fetchall()
        role = result[0][0]

        def set_default_value(event):
            default_text_1 = username1
            username_entry.delete(0, tk.END)  # Clear any existing text
            username_entry.insert(0, default_text_1)  # Insert the default value
            username_entry.config(state=tk.DISABLED)

            default_text_2 = role
            role_entry.delete(0, tk.END)  # Clear any existing text
            role_entry.insert(0, default_text_2)  # Insert the default value
            role_entry.config(state=tk.DISABLED)

        def set_security():
            question = security_question_var.get()
            print(question)
            answer = security_answer_entry.get()
            print(answer)
            if answer == "":
                messagebox.showerror("Error","Please fill the security answer! ")
            else:
                # Update security question and answer in the database
                update_sql = "UPDATE login SET security_question = %s, security_answer = %s WHERE username = %s"
                update_val = (question, answer, username1)
                c1.execute(update_sql, update_val)
                conn.commit()

                # Increment login count by 1
                increment_sql = "UPDATE login SET login_count = login_count + 1 WHERE username = %s"
                c1.execute(increment_sql, (username1,))
                conn.commit()

                messagebox.showinfo("Success", "Security question and answer set successfully.")
                set_questions_win.destroy()
                subprocess.run(['python', 'main.py'], check=True)



        set_questions_win = tk.Tk()
        set_questions_win.geometry('590x430+490+150')
        set_questions_win.title('Set security question and answer')

        # Fonts
        h1 = ('Arial', '25')
        h2 = ('Arial', '20')
        f1 = ('Arial', '16')
        f2 = ('Arial', '14')

        # First Frame
        frame1 = tk.Frame(set_questions_win)
        frame1.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        # Label in Frame 1
        label_frame1 = tk.Label(frame1, text="Set Security Questions and Answers", font=h1)
        label_frame1.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        # Second Frame
        frame2 = tk.Frame(set_questions_win)
        frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Username Label and Entry Field
        username_label = tk.Label(frame2, text="Username:", font=f1)
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        username_entry = tk.Entry(frame2, font=f1)
        username_entry.bind("<Enter>", set_default_value)
        username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


        # Role Label and Entry Field

        role_label = tk.Label(frame2, text="Role:", font=f1)
        role_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        role_entry = tk.Entry(frame2, font=f1)
        role_entry.bind("<Enter>", set_default_value)
        role_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Security Question Label and Dropdown
        security_question_label = tk.Label(frame2, text="Security Question:", font=f1)
        security_question_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        security_question_var = tk.StringVar()
        security_question_var.set("My Birthplace?")
        security_question_dropdown = tk.OptionMenu(frame2, security_question_var,
                                                   "My Birthplace?", "My favourite fast food?",
                                                   "My favourite Colour?", "My first school name?")
        security_question_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Security Answer Label and Entry Field
        security_answer_label = tk.Label(frame2, text="Security Answer:", font=f1)
        security_answer_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        security_answer_entry = tk.Entry(frame2, font=f1)
        security_answer_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Button
        set_button = tk.Button(frame2, text="Set", font=f1, bg="light blue", command=set_security)
        set_button.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        # Configure row and column weights
        set_questions_win.grid_rowconfigure(0, weight=0)  # First row (frame1)
        set_questions_win.grid_rowconfigure(1, weight=1)  # Second row (frame2)
        set_questions_win.grid_columnconfigure(0, weight=1)  # First column (frame1 and frame2)

        for i in range(5):  # Number of rows including the button
            frame2.grid_rowconfigure(i, weight=1)
        for i in range(2):  # Two columns
            frame2.grid_columnconfigure(i, weight=1)

        set_questions_win.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Example usage
if __name__ == "__main__":
    set_security_page()
