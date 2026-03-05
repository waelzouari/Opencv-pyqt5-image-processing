# OpenCV PyQt5 Image Processing Application

A desktop application developed in Python for interactive image processing using OpenCV and PyQt5.

This project provides a graphical interface that allows users to load an image and explore several computer vision operations such as RGB channel visualization,
grayscale conversion, brightness and contrast adjustment, and histogram analysis.

## Features

* Load and display an image
* Display image dimensions (height, width, number of channels)
* Visualize individual RGB channels
* Display color histogram
* Convert image to grayscale
* Adjust brightness and contrast
* Display grayscale histogram

## Technologies Used

* Python
* PyQt5 (Graphical User Interface)
* OpenCV (Image processing)
* NumPy (Matrix operations)
* Matplotlib (Histogram visualization)

## Project Structure



├── main.py       # Main application logic
├── design.py     # Generated PyQt interface file
├── design.ui     # GUI layout created with Qt Designer
└── README.md     # Project documentation


## How to Run the Application

1. Install the required libraries:


pip install pyqt5 opencv-python numpy matplotlib


2. Run the application:


python main.py


3. Use the **Browse** button to load an image and explore the available processing tools.

## Learning Objectives

This project was developed as part of a computer vision laboratory to practice:

* Image manipulation with OpenCV
* GUI development with PyQt5
* Image histogram analysis
* Basic image enhancement techniques

## Author

Wael Zouari
