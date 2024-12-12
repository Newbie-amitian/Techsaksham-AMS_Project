import cv2
import os
import sys
import tkinter as tk
import time
from tkinter import messagebox
from utils import add_attendance, enter_subject_window, animate_detection_text

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS  # Path to temporary folder for bundled files
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Path to script folder during development

# Construct paths for Haarcascade files
face_cascade_path = os.path.join(base_path, "cv2", "data", "haarcascade_frontalface_default.xml")
eye_cascade_path = os.path.join(base_path, "cv2", "data", "haarcascade_eye.xml")
eyeglasses_cascade_path = os.path.join(base_path, "cv2", "data", "haarcascade_eye_tree_eyeglasses.xml")

# Ensuring Haarcascade files exist
for path in [face_cascade_path, eye_cascade_path, eyeglasses_cascade_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Haarcascade file not found at {path}!")

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
eyeglasses_cascade = cv2.CascadeClassifier(eyeglasses_cascade_path)

def enter_subject_window(callback):
    """Create a window to input the subject for attendance."""
    subject_window = tk.Toplevel()
    subject_window.title("Enter Subject Name")
    subject_window.geometry("370x250")  # Adjusted height to fit the label
    subject_window.configure(bg="#F4F4F4")  # Light grey background

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
        width=20,
        relief="flat",
        highlightbackground="#CCCCCC",
        highlightthickness=1,
        bd=0,
    )
    subject_entry.grid(row=0, column=1, padx=10, pady=10)

    # Function to handle button click
    def fill_attendance():
        subject = subject_entry.get().strip()
        if subject:
            callback(subject)
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
        command=fill_attendance,
    )
    fill_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Make the window modal
    subject_window.transient()
    subject_window.grab_set()
    subject_window.mainloop()


def automatic_attendance():
    """Automatically mark attendance by recognizing faces."""
    trainer_file_path = "TrainingImageLabel/trainer.yml"
    if not os.path.exists(trainer_file_path) or os.stat(trainer_file_path).st_size == 0:
        messagebox.showwarning("Warning", "No Data Found for Recognition.")
        return 

    def process_subject(subject):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_file_path)  # Read the trainer data
        font = cv2.FONT_HERSHEY_SIMPLEX

        cam = cv2.VideoCapture(0)
        last_recognized_id = None  # Track the last recognized ID to avoid multiple alerts
        detection_start_time = time.time()
        frame_count = 0
        animate_detection = True  # Flag to control animation
        recognized_face_time = 0  # Time when a face was last recognized

        while True:
            ret, img = cam.read()
            if not ret:
                messagebox.showerror("Error", "Failed to access the camera.")
                break

            # Animate the text independently without blocking the capturing
            if animate_detection:
                animate_detection_text(img, frame_count)
                frame_count += 1

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(30,30))

            recognized_face = False
            for (x, y, w, h) in faces:
                ID, conf = recognizer.predict(gray[y:y + h, x:x + w])

                if conf < 50:  # Face is recognized
                    # Get student info
                    student_info = get_student_info_by_enrollment(ID)
                    if student_info:
                        name, enrollment = student_info  # Extract name and enrollment
                        if last_recognized_id != ID:
                            last_recognized_id = ID

                        cv2.putText(img, f"Enrollment: {enrollment}", (x, y - 40), font, 1, (0, 255, 0), 2)
                        cv2.putText(img, f"Name: {name}", (x, y - 10), font, 1, (0, 255, 0), 2)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        recognized_face = True
                        recognized_face_time = time.time()
                else:  # Detection rectangle
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 193, 0), 2)  # Red rectangle for unknown face
                    
                    roi_gray = gray[y:y+h, x:x+w]

                    # Try detecting glasses
                    eyeglasses = eyeglasses_cascade.detectMultiScale(roi_gray)
                    if len(eyeglasses) > 0:
                        for (gx, gy, gw, gh) in eyeglasses:
                            cv2.rectangle(img, (x + gx, y + gy), (x + gx + gw, y + gy + gh), (255, 193, 0), 2)
                    else:
                        # If no glasses are detected
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(img, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 193, 0), 2)

            if recognized_face:
                animate_detection = False
            elif time.time() - recognized_face_time > 1:  # Resume animation after 1 second
                animate_detection = True

            cv2.imshow("Automatic Attendance", img)

            # Check if 10 seconds have passed
            if time.time() - detection_start_time > 10:
                if last_recognized_id is None: # no face was recognized within 10 seconds
                    messagebox.showwarning("Unknown User!", "User  Not Registered.")
                break

            # Exit when 'q' is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # Marking attendance when face is recognized
        if last_recognized_id is not None:
            messagebox.showinfo("Action", f"Automatic attendance marked for {name} ({enrollment}).")
            if enrollment and name:
                add_attendance(enrollment, name, subject , "Present")

    enter_subject_window(process_subject)



def manually_fill_attendance():
    def show_admin_login():
        # Admin login window
        login_window = tk.Toplevel()
        login_window.title("Admin Login")
        login_window.geometry("400x250")
        login_window.configure(bg="#F4F4F4")

        tk.Label(login_window, text="Enter Admin Credentials", font=("Helvetica", 12, "bold"), bg="#F4F4F4").pack(pady=20)

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
                    prompt_for_student_info()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password!")

            tk.Button(admin_login_window, text="Login", font=("Helvetica", 10, "bold"), bg="#5A9FD4", command=validate_admin).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(login_window, text="Login", font=("Helvetica", 12, "bold"), bg="#5A9FD4", command=admin_login).pack(pady=20)

    def prompt_for_student_info():
        # Prompt to enter student details including subject
        student_info_window = tk.Toplevel()
        student_info_window.title("Enter Student Info")
        student_info_window.geometry("300x350")
        student_info_window.configure(bg="#F4F4F4")

        tk.Label(student_info_window, text="Enter Student Name:", font=("Helvetica", 12, "bold"), bg="#F4F4F4").pack(pady=10)
        name_entry = tk.Entry(student_info_window, font=("Helvetica", 10), width=30)
        name_entry.pack(pady=10)

        tk.Label(student_info_window, text="Enter Enrollment Number:", font=("Helvetica", 12, "bold"), bg="#F4F4F4").pack(pady=10)
        enrollment_entry = tk.Entry(student_info_window, font=("Helvetica", 10), width=30)
        enrollment_entry.pack(pady=10)

        tk.Label(student_info_window, text="Enter Subject:", font=("Helvetica", 12, "bold"), bg="#F4F4F4").pack(pady=10)
        subject_entry = tk.Entry(student_info_window, font=("Helvetica", 10), width=30)
        subject_entry.pack(pady=10)

        def mark_attendance():
            name = name_entry.get().strip()
            enrollment = enrollment_entry.get().strip()
            subject = subject_entry.get().strip()
            if name and enrollment and subject:
                # Call the function to mark attendance
                add_attendance(enrollment, name, subject, "Present")
                messagebox.showinfo("Attendance", "Attendance marked successfully.")
                student_info_window.destroy()  # Close the window after marking attendance
            else:
                messagebox.showerror("Invalid Input", "Please fill all fields (name, enrollment, and subject).")

        tk.Button(student_info_window, text="Mark Attendance", font=("Helvetica", 12, "bold"), bg="#5A9FD4", command=mark_attendance).pack(pady=20)

    show_admin_login()


    
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
