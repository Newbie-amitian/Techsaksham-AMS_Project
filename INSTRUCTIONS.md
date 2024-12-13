# Summary of Attendance Management System Code

## gui.py
- Defines the graphical user interface (GUI) for the application.
- Contains functions to create the main window, clear entry fields, and handle subject input.
- Implements hover effects for buttons to enhance user experience.

## main.py
- Serves as the main entry point for the application.
- Initializes the GUI and sets up buttons for capturing images, training the model, and marking attendance.
- Integrates utility functions to check CSV files and manage student records.

## training.py
- Handles the image capturing process for student registration.
- Implements functions to train the face recognition model using captured images.
- Checks for registration conflicts to prevent duplicate entries.

## testing.py
- Manages the automatic attendance marking process using face recognition.
- Implements functions to detect faces and recognize students based on the trained model.
- Provides a manual attendance filling option for administrators.

## utils.py
- Contains utility functions for file handling, encryption, and attendance management.
- Implements functions to create necessary directories, check CSV files, and manage student records.
- Provides encryption and decryption functionalities for secure attendance data storage.
