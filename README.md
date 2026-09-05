#  Computer Vision Robotic Hand (v1.0)


![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-Arduino-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![ESP32](https://img.shields.io/badge/Hardware-ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

3D Printed Robotic Hand with real time hand tracking.

---

##  Demo & Overview

<!-- Sem vlož link na obrázok alebo GIF z tvojho repozitára -->
![Robotic Hand Demo](demo.gif)

> **How it works:** OpenCV captures video feed $\rightarrow$ MediaPipe calculates 3D hand landmarks and finger angles $\rightarrow$ Python sends serialized data via PySerial $\rightarrow$ ESP32 moves servos using PCA9685.

---

##  Key Features
* **Real-Time Tracking:** fast hand landmark positioning via MediaPipe.
* **Low Latency:** Asynchronous PySerial communication to avoid buffer delays.
* **16-Channel Servo Control:** Driven via I2C interface on PCA9685 to conserve ESP32 GPIO pins.
* **Custom 3D Assembly:** Custom-printed mechanical joints for smooth finger actuation.

---

##  Tech Stack & Hardware

| Category | Component / Library |
| :--- | :--- |
| **Languages** | Python 3.12, C++ (Arduino Framework) |
| **Vision & Math** | OpenCV, MediaPipe, NumPy |
| **Communication** | PySerial (Custom Serial Protocol) |
| **Microcontroller**| ESP32 Dev Module |
| **Servo Driver** | PCA9685 16-Channel 12-bit PWM I2C |
| **Actuators** | SG90 / MG996R Servos |

All the STL and 3MF Files can be found here on my Printables profile: (https://www.printables.com/model/1813325-robotic-hand-assembly-personal-project)

---

##  Quick Start Guide

### 1. Hardware Connections
* **PCA9685 VCC** $\rightarrow$ ESP32 3.3V
* **PCA9685 GND** $\rightarrow$ ESP32 GND & External Power GND *(Common Ground)*
* **PCA9685 SDA/SCL** $\rightarrow$ ESP32 Default I2C Pins (Based on your model of ESP32)
* **PCA9685 V+** $\rightarrow$ External 5V Power Supply

### 2. Firmware Installation
1. Open the `/firmware` directory in Arduino IDE.
2. Select **ESP32 Dev Module** as your board.
3. Install `Adafruit PCA9685 PWM Servo Driver Library`.
4. Upload the sketch to your ESP32.

### 3. Python Setup
Clone the repository and install the required packages:

```bash
git clone [https://github.com/alexej-pucek/Robotic-Hand.git](https://github.com/alexej-pucek/Robotic-Hand.git)
cd Robotic-Hand
pip install opencv-python mediapipe pyserial numpy
