# Techsaksham-Attendance_Management_System_Using_Face_Recognition_Project

This project is an Attendance Management System that utilizes face recognition technology to automate the attendance process. It is built using Python and the Tkinter library for the GUI, along with OpenCV for image processing.

## Features

- Capture and register student images.
- Train a face recognition model.
- Automatically mark attendance using face recognition.
- Manually fill attendance.
- View attendance records in a dashboard.

## Installation

1. Clone the repository or download the files.
    ```bash
   git clone https://github.com/Newbie-amitian/Techsaksham-AMS_Project.git
    
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the system:
   ```bash
   python main.py
   
5. Create a folder named cv2 in the same directory as main.py.

6. Download the Haarcascade files and place them in the cv2 folder:

- haarcascade_frontalface_default.xml
- haarcascade_eye.xml
- haarcascade_eye_tree_eyeglasses.xml

## Usage
- Run the main.py file to start the application.
- Follow the on-screen instructions to capture images, train the model, and mark attendance.

## Files Overview
- gui.py: Contains the GUI components and layout.
- main.py: The main entry point of the application.
- training.py: Handles image capturing and model training.
- testing.py: Manages attendance marking through face recognition.
- utils.py: Contains utility functions for file handling and encryption.

## ⭐️ Support the project
If you like this project and find it useful, please consider giving it a star! ⭐️

Your support helps to increase the visibility of the project and motivates me to continue improving it. Thank you! 🙏
