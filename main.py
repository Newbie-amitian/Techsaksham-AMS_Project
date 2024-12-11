import tkinter as tk
from tkinter import messagebox
from gui import create_main_window
from training import take_images, train_images
from testing import automatic_attendance, manually_fill_attendance
from utils import check_csv_file, check_registered_students, check_for_registration_conflicts

def on_enter(event, widget):
    widget.config(bg="#5A9FD4", fg="white")

def on_leave(event, widget):
    widget.config(bg="#85C1E9", fg="black")

def main():
    attempts = 3

    # Create root and other GUI components
    root, enrollment_entry, name_entry = create_main_window()
    check_csv_file()

    button_config = {
        "font": ("Times New Roman", 12, "bold"),
        "width": 20,
        "height": 1,
        "bg": "#85C1E9",
        "fg": "black",
        "activebackground": "#3498DB",
        "activeforeground": "white",
    }

    # Create buttons with specific placements (as in File 1)
    take_images_btn = tk.Button(root, text="Capture Images", command=lambda: take_images(enrollment_entry, name_entry), **button_config)
    take_images_btn.place(x=50, y=200)

    train_images_btn = tk.Button(root, text="Train Images", command=lambda: train_images(enrollment_entry, name_entry), **button_config)
    train_images_btn.place(x=250, y=200)

    automatic_attendance_btn = tk.Button(root, text="Automatic Attendance", command=lambda: automatic_attendance(), **button_config)
    automatic_attendance_btn.place(x=450, y=200)

    manually_fill_btn = tk.Button(root, text="Manually Fill Attendance", command=lambda: manually_fill_attendance(), **button_config)
    manually_fill_btn.place(x=150, y=300)

    check_registered_btn = tk.Button(root, text="Attendance Dashboard", command=check_registered_students, **button_config)
    check_registered_btn.place(x=350, y=300)
    
    # Hover effects (same as File 1)
    for button in [take_images_btn, train_images_btn, automatic_attendance_btn, manually_fill_btn, check_registered_btn]:
        button.bind("<Enter>", lambda event, b=button: on_enter(event, b))
        button.bind("<Leave>", lambda event, b=button: on_leave(event, b))

    root.mainloop()

if __name__ == "__main__":
    main()
