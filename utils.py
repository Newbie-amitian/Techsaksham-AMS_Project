import os
import sys
import csv
import cv2
from datetime import datetime
from tkinter import simpledialog
from cryptography.fernet import Fernet
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

##### For getting key in form of a file #####
"""def get_or_create_key():
    key_file = "key.key"
    if not os.path.exists(key_file):
        # Generate a new key and save it
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
        return key
    else:
        # Load the existing key
        with open(key_file, 'rb') as file:
            return file.read()"""
###############################################



SECRET_KEY = b'q_otc5tVVs56Y0uiLzwtu3I-xAPtnq8D3COs_5arrKI='
cipher = Fernet(SECRET_KEY)


def encrypt_file(filename):
    """Encrypts the specified file using the fixed key."""
    try:
        with open(filename, 'rb') as file:
            data = file.read()  # Read the file content
        encrypted_data = cipher.encrypt(data)
        with open(filename, 'wb') as file:
            file.write(encrypted_data)  # Overwrite with encrypted content
    except Exception as e:
        messagebox.showerror("Encryption Error", f"Error encrypting the file: {e}")



def decrypt_file(filename):
    """Decrypts the specified file using the fixed key."""
    try:
        with open(filename, 'rb') as file:
            encrypted_data = file.read()  # Read the encrypted content
        decrypted_data = cipher.decrypt(encrypted_data)
        with open(filename, 'wb') as file:
            file.write(decrypted_data)  # Overwrite with decrypted content
    except Exception as e:
        messagebox.showerror("Decryption Error", f"Error decrypting the file: {e}")

def check_and_create_directories():
    # Check and create 'TrainingImageLabel' directory
    if not os.path.exists('TrainingImageLabel'):
        os.makedirs('TrainingImageLabel')

    # Check and create 'My_Captures' directory
    if not os.path.exists('My_Captures'):
        os.makedirs('My_Captures')


def get_csv_filename():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"Attendance_{current_date}.csv"

def check_csv_file():
    filename = get_csv_filename()
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Enrollment', 'Subject', 'Status', 'Time'])
        encrypt_file(filename)





def check_registered_students():
    def show_login_window():
        # Create a login window
        login_window = tk.Toplevel()
        login_window.title("Login")
        login_window.geometry("400x250")
        login_window.configure(bg="#F4F4F4")

        tk.Label(login_window, text="Choose Login Type:", font=("Helvetica", 12, "bold"), bg="#F4F4F4").pack(pady=10)

        # Admin Login
        def admin_login():
            admin_login_window = tk.Toplevel(login_window)
            admin_login_window.title("Admin Login")
            admin_login_window.geometry("375x200")
            admin_login_window.configure(bg="#F4F4F4")

            tk.Label(admin_login_window, text="Admin Username:", font=("Helvetica", 10), bg="#F4F4F4").grid(row=0, column=0, padx=10, pady=10)
            username_entry = tk.Entry(admin_login_window, font=("Helvetica", 10), width=30)
            username_entry.grid(row=0, column=1, padx=10, pady=10)
            username_entry.insert(0, "Administrator")
            username_entry.config(state="disabled")
            
            tk.Label(admin_login_window, text="Admin Password:", font=("Helvetica", 10), bg="#F4F4F4").grid(row=1, column=0, padx=10, pady=10)
            password_entry = tk.Entry(admin_login_window, font=("Helvetica", 10), width=30, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=10)

            def validate_admin():
                if username_entry.get() == "Administrator" and password_entry.get() == "Password123":
                    admin_login_window.destroy()
                    login_window.destroy()
                    display_all_students()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password!")

            tk.Button(admin_login_window, text="Login", font=("Helvetica", 10, "bold"), bg="#5A9FD4", command=validate_admin).grid(row=2, column=0, columnspan=2, pady=10)

        # Student Login
        def student_login():
            student_login_window = tk.Toplevel(login_window)
            student_login_window.title("Student Login")
            student_login_window.geometry("390x200")
            student_login_window.configure(bg="#F4F4F4")

            tk.Label(student_login_window, text="Enrollment Number:", font=("Helvetica", 10), bg="#F4F4F4").grid(row=0, column=0, padx=10, pady=10)
            enrollment_entry = tk.Entry(student_login_window, font=("Helvetica", 10), width=30)
            enrollment_entry.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(student_login_window, text="Student Name:", font=("Helvetica", 10), bg="#F4F4F4").grid(row=1, column=0, padx=10, pady=10)
            name_entry = tk.Entry(student_login_window, font=("Helvetica", 10), width=30)
            name_entry.grid(row=1, column=1, padx=10, pady=10)

            def validate_student():
                name = name_entry.get().strip()
                enrollment = enrollment_entry.get().strip()
                if not name or not enrollment:
                    messagebox.showerror("Login Failed", "Please enter both Name and Enrollment!")
                    return

                filename = get_csv_filename()
                try:
                    decrypt_file(filename)  # Decrypt the file
                    with open(filename, mode='r') as file:
                        reader = csv.reader(file)
                        rows = list(reader)
                        header, *data = rows

                        matching_rows = [row for row in data if row[0] == enrollment and row[1] == name]
                    encrypt_file(filename)  # Encrypt the file again

                    if matching_rows:
                        display_student_data(header, matching_rows)
                    else:
                        messagebox.showerror("No Records", "No matching records found for the student.")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing the CSV file: {e}")
                    encrypt_file(filename)

            tk.Button(student_login_window, text="Login", font=("Helvetica", 10, "bold"), bg="#5A9FD4", command=validate_student).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(login_window, text="Admin Login", font=("Helvetica", 12, "bold"), bg="#5A9FD4", command=admin_login).pack(pady=20)
        tk.Button(login_window, text="Student Login", font=("Helvetica", 12, "bold"), bg="#5A9FD4", command=student_login).pack(pady=10)

    def display_all_students():
        filename = get_csv_filename()
        try:
            decrypt_file(filename)  # Decrypt the file
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                top = tk.Toplevel()
                top.title("Registered Students")
                top.geometry("700x400")

                treeview = ttk.Treeview(top, columns=("Enrollment", "Name", "Subject", "Status", "Time"), show="headings")
                for col in ["Enrollment", "Name", "Subject", "Status", "Time"]:
                    treeview.heading(col, text=col)
                    treeview.column(col, width=150, anchor="center")
                for row in rows[1:]:
                    treeview.insert("", "end", values=row)

                treeview.pack(fill=tk.BOTH, expand=True)

                def on_close():
                    encrypt_file(filename)  # Encrypt the file when window is closed
                    top.destroy()

                top.protocol("WM_DELETE_WINDOW", on_close)
                top.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Error processing the CSV file: {e}")
            encrypt_file(filename)  # Ensure file is encrypted if an error occurs

    def display_student_data(header, student_rows):
        top = tk.Toplevel()
        top.title("Student Information")
        top.geometry("700x300")

        treeview = ttk.Treeview(top, columns=header, show="headings")
        for col in header:
            treeview.heading(col, text=col)
            treeview.column(col, width=150, anchor="center")
        for row in student_rows:
            treeview.insert("", "end", values=row)
        treeview.pack(fill=tk.BOTH, expand=True)

    show_login_window()

def add_attendance(enrollment, name, subject, status):
    filename = get_csv_filename()
    current_time = datetime.now().strftime("%H:%M:%S")  # Time in 24-hour format with seconds

    try:
        decrypt_file(filename)
        # Add the attendance record directly without checking for existing records
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([enrollment, name, subject, status, current_time])
        encrypt_file(filename)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating attendance: {e}")




# In case want to Add with the date #
''' current_time = datetime.now()
    date = current_time.strftime("%Y-%m-%d")
    time = current_time.strftime("%H:%M:%S")

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([enrollment, name, subject, date, time]) '''

def enter_subject_window():
    return simpledialog.askstring("Subject", "Enter Subject Name:")



# Function to check for registration conflicts
def check_for_registration_conflicts(enrollment, name, attempts=3):
    if os.path.exists("My_Captures"):
        # Initialize mappings for name-to-enrollment and enrollment-to-name
        name_to_enrollment = {}
        enrollment_to_name = {}
        
        # Loop through all folders (user records)
        for folder_name in os.listdir("My_Captures"):
            folder_path = os.path.join("My_Captures", folder_name)
            
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".jpg"):
                        file_parts = file.split('_')
                        
                        if len(file_parts) >= 2:
                            file_enrollment, file_name = file_parts[0], file_parts[1]
                            
                            # Populate the mappings with existing records
                            name_to_enrollment[file_name] = file_enrollment
                            enrollment_to_name[file_enrollment] = file_name

                            # Check for specific conflict conditions
                            if enrollment == file_enrollment and name == file_name:
                                return "Credentials already registered under different user. Please verify your details."
                            elif enrollment == file_enrollment and name is None:
                                return "Enrollment already in use. Please verify your details."
                            elif name == file_name and enrollment is None:
                                return "Name already in use. Please verify your details."

        # Combined check: If either the name or the enrollment is registered with a different associated value
        if (name and name in name_to_enrollment and name_to_enrollment[name] != enrollment) or \
           (enrollment and enrollment in enrollment_to_name and enrollment_to_name[enrollment] != name):
            # If this is the last attempt, quit the program
            if attempts == 1:
                sys.exit("Mismatching of credentials detected. Program exiting.")
            else:
                # Otherwise, prompt the user with remaining attempts
                return f"Mismatching of credentials detected. \nLikelihood of fraud (60%).\n{attempts - 1} Attempts remaining."

    # If no conflicts are found, assume the user is new
    return None  # No conflict found





def get_student_info_by_enrollment(enrollment):
    """Retrieve student info by matching enrollment number."""
    user_directory = "My_Captures"
    for folder in os.listdir(user_directory):
        for file in os.listdir(os.path.join(user_directory, folder)):
            if file.endswith(".jpg"):
                file_parts = file.split('_')
                if str(enrollment) == file_parts[0]:
                    return folder, enrollment
    return None



# Function to animate the text independently
def animate_registering_text(img, frame_count):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Registering New Face"
    dot_count = (frame_count // 10) % 4  # Cycle through 0-3 dots every 10 frames
    dots = "." * dot_count
    current_text = text + dots

    # Get the size of the text to center it
    text_size = cv2.getTextSize(current_text, font, 1, 2)[0]
    text_x = (img.shape[1] - text_size[0]) // 2  # Center the text horizontally
    text_y = 30  # Position it near the top of the image
    cv2.putText(img, current_text, (text_x, text_y), font, 1, (255, 193, 0), 2)



def animate_detection_text(img, frame_count):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Trying to Detect"
    dot_count = (frame_count // 10) % 4  # Cycle through 0-3 dots every 10 frames
    dots = "." * dot_count
    current_text = text + dots

    # Get the size of the text to center it
    text_size = cv2.getTextSize(current_text, font, 1, 2)[0]
    text_x = (img.shape[1] - text_size[0]) // 2  # Center the text horizontally
    text_y = 30  # Position it near the top of the image
    cv2.putText(img, current_text, (text_x, text_y), font, 1, (255, 193, 0), 2)
