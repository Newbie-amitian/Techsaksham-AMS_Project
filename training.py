import cv2
import numpy as np
import os
import sys
from PIL import Image
from tkinter import messagebox
from utils import check_for_registration_conflicts, animate_registering_text

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

# Function to take images and display animation
def take_images(enrollment_entry, name_entry):
    enrollment = enrollment_entry.get()
    name = name_entry.get()

    if not enrollment or not name:
        messagebox.showerror("Error", "Enrollment and Name fields cannot be empty.")
        return

    # Check for conflicts
    conflict_message = check_for_registration_conflicts(enrollment, name)
    if conflict_message:
        messagebox.showwarning("Warning!",conflict_message)
        return

    try:
        # Create directory for the user if it doesn't exist
        user_directory = os.path.join("My_Captures", name)
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        cam = cv2.VideoCapture(0)
        sample_num = 0
        frame_count = 0  # Counter to control the animation timing

        while True:
            ret, img = cam.read()
            if not ret:
                messagebox.showerror("Error", "Failed to access the camera.")
                break

            # Animate the text independently without blocking the capturing
            animate_registering_text(img, frame_count)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(30, 30))

            for (x, y, w, h) in faces:
                sample_num += 1

                # Save the captured face image
                cv2.imwrite(
                    os.path.join(user_directory, f"{enrollment}_{name}_{sample_num}.jpg"),
                    gray[y:y + h, x:x + w]
                )

                # Display a rectangle around the detected face
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 193, 0), 2)

                # Detecting eyes or glasses inside the facial region
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
            # Increment frame count for the text animation timing
            frame_count += 1

            cv2.imshow("Capturing Faces", img)

            # Exit loop when 'q' is pressed or when 150 samples are captured
            if cv2.waitKey(1) & 0xFF == ord('q') or sample_num >= 150:
                break

        cam.release()
        cv2.destroyAllWindows()

        if sample_num >= 150:
            messagebox.showinfo("Success", f"Images saved for Enrollment: {enrollment}, Name: {name}")
        else:
            messagebox.showwarning("Incomplete Capture", "Captured fewer than 150 images.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def train_images(enrollment_entry, name_entry):
    enrollment = enrollment_entry.get()
    name = name_entry.get()

    if not enrollment or not name:
        messagebox.showwarning("Error", "Enrollment and Name fields cannot be empty.")
        return

    try:
        # Ensure TrainingImageLabel directory exists
        training_directory = "TrainingImageLabel"
        if not os.path.exists(training_directory):
            os.makedirs(training_directory)  # Create the directory if it doesn't exist

        user_folder = os.path.join("My_Captures", name)
        if not os.path.exists(user_folder):
            messagebox.showerror("Error", "No images found. Please capture images first.")
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Load the existing model if it exists
        model_path = os.path.join(training_directory, "trainer.yml")
        if os.path.exists(model_path):
            recognizer.read(model_path)

        faces, ids = [], []

        # Loop through all images and add them to the model
        for file in os.listdir(user_folder):
            if file.endswith(".jpg"):
                path = os.path.join(user_folder, file)
                image = Image.open(path).convert("L")
                faces.append(np.array(image, "uint8"))
                # Extract enrollment number from filename
                file_parts = file.split('_')
                ids.append(int(file_parts[0]))  # Use the enrollment number

        # Train the recognizer using the existing and new images
        recognizer.update(faces, np.array(ids))

        # Save the updated model back to the file
        recognizer.save(model_path)
        messagebox.showinfo("Success", "Model training complete and updated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))



        
def get_name_from_enrollment(enrollment):
    # Load the existing model and map enrollment to name (you may need to adjust this part based on how you store names)
    model_path = "TrainingImageLabel/trainer.yml"
    if os.path.exists(model_path):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_path)

        faces, ids = [], []
        user_folder = "My_Captures"
        
        # Loop through all images and match them to the enrollment number
        for file in os.listdir(user_folder):
            if file.endswith(".jpg"):
                file_parts = file.split('_')
                current_enrollment = file_parts[0]

                if current_enrollment == str(enrollment):
                    name = '_'.join(file_parts[1:])  # Join the remaining parts to get the name
                    return name

    return None  # If no name is found
