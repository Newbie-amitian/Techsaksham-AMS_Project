import tkinter as tk
from tkinter import messagebox

def create_main_window():
    # Create the main window
    root = tk.Tk()
    root.title("Attendance Management System using Face Recognition")
    root.geometry("700x390")
    root.configure(bg="#F8F9F9")

    # Title Label
    title_label = tk.Label(
        root,
        text="Attendance Management System using Face Recognition",
        font=("Times New Roman", 20, "bold"),
        bg="#2E86C1",
        fg="white",
        padx=10,
        pady=10,
    )
    title_label.pack(fill=tk.X)

    # Enrollment Section
    enrollment_label = tk.Label(
        root, 
        text="Enter Enrollment:", 
        font=("Times New Roman", 12, "bold"), 
        bg="#F8F9F9", 
        fg="#2C3E50"
    )
    enrollment_label.place(x=50, y=80)

    enrollment_entry = tk.Entry(
        root, 
        font=("Times New Roman", 12), 
        width=30
    )
    enrollment_entry.place(x=200, y=80)

    clear_enrollment_btn = tk.Button(
        root, 
        text="Clear", 
        font=("Times New Roman", 10), 
        bg="#2E86C1", 
        fg="white", 
        command=lambda: clear_entry(enrollment_entry)
    )
    clear_enrollment_btn.place(x=600, y=78)

    # Name Section
    name_label = tk.Label(
        root, 
        text="Enter Name:", 
        font=("Times New Roman", 12, "bold"), 
        bg="#F8F9F9", 
        fg="#2C3E50"
    )
    name_label.place(x=50, y=130)

    name_entry = tk.Entry(
        root, 
        font=("Times New Roman", 12), 
        width=30
    )
    name_entry.place(x=200, y=130)

    clear_name_btn = tk.Button(
        root, 
        text="Clear", 
        font=("Times New Roman", 10), 
        bg="#2E86C1", 
        fg="white", 
        command=lambda: clear_entry(name_entry)
    )
    clear_name_btn.place(x=600, y=128)

    return root, enrollment_entry, name_entry

def clear_entry(entry_field):
    # Clear the content of the entry field
    entry_field.delete(0, tk.END)

def enter_subject_window(callback):
    # Create a new window for subject input
    subject_window = tk.Toplevel()
    subject_window.title("Enter Subject Name")
    subject_window.geometry("350x180")
    subject_window.configure(bg="#F4F4F4")  # Light grey background for a clean look

    # Label for subject
    subject_label = tk.Label(
        subject_window,
        text="Enter Subject:",
        font=("Helvetica", 12, "bold"),
        bg="#F4F4F4",
        fg="#333333",
    )
    subject_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    # Entry for subject input
    subject_entry = tk.Entry(
        subject_window,
        font=("Helvetica", 12),
        width=30,
        relief="flat",
        highlightbackground="#CCCCCC",
        highlightthickness=1,
        bd=0
    )
    subject_entry.grid(row=0, column=1, padx=10, pady=10)

    # Function to handle button click
    def fill_attendance():
        subject = subject_entry.get().strip()
        if subject:
            callback(subject)  # Pass the subject to the callback function
            subject_window.destroy()  # Close the window
        else:
            messagebox.showwarning("Input Error", "Subject name is required!")

    # Button for filling attendance
    fill_button = tk.Button(
        subject_window,
        text="Fill Attendance",
        font=("Helvetica", 12, "bold"),
        bg="#5A9FD4",
        fg="white",
        activebackground="#1D75C9",
        activeforeground="white",
        relief="flat",
        command=fill_attendance
    )
    fill_button.grid(row=1, column=0, columnspan=2, pady=20)

    # Make the window modal
    subject_window.transient()
    subject_window.grab_set()
    subject_window.mainloop()

def on_enter(event, widget):
    widget.config(bg="#5A9FD4", fg="white")

def on_leave(event, widget):
    widget.config(bg="#85C1E9", fg="black")
