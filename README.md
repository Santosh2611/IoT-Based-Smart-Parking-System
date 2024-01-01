# IoT-Based-Smart-Parking-System
Raspberry Pi is a miniature computer which has the adaptability with sensors. The automated car parking system uses the Raspberry Pi. This work proposes an automated car parking system that uses infrared sensors. The infrared sensor senses the movement of the vehicle and transmits the signal to the Pi. 

An LED display is installed at the main entrance of the parking area to provide enough information about slot availability. In a real-time scenario, the proposed work can be enhanced further for multiple levels containing n number of slots with multiple Raspberry Pi. 

# GPIO and Associated Peripherals

This project focuses on interfacing various peripherals with a Raspberry Pi, including GPIO control, LCD interfacing, Pi Camera integration, and data logging using Adafruit IO.

## Components and Libraries Used
- **RPi.GPIO**: Module for controlling GPIO on a Raspberry Pi.
- **RPLCD**: Raspberry Pi LCD library for displaying information.
- **picamera**: Interface to the Raspberry Pi camera module for capturing images.
- **PIL**: Python Imaging Library for image processing.
- **pytesseract**: Python wrapper for Tesseract-OCR for optical character recognition.
- **random**: Pseudo-random number generation for various distributions.
- **time**: Time-related functions for scheduling tasks.
- **Adafruit_IO**: For creating an instance of the REST client to connect with Adafruit IO.

The project utilizes these components to build a system for capturing and recognizing number plates, managing parking slots, and updating the status in real time via Adafruit IO feeds. The integration with IR sensors, motors, and an LCD enables the complete functionality of the parking system.

## Implementation and Usage
The code includes detailed variable initializations, pin configurations, and looping through the sensor input. Each section is extensively commented on, explaining the logic behind the hardware interactions and image processing. It provides instructions to set up the required hardware components and software libraries, as well as how to run the system effectively.

## Future Enhancements
Potential improvements to enhance the project could involve optimizing the image processing algorithms for better recognition accuracy, implementing a user interface for manual inputs or configuration, and additional error handling to ensure robust performance.

This repository contains all the necessary scripts, sample images, and documentation for setting up and using the project with a Raspberry Pi.
