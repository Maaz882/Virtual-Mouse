#AI Virtual Mouse using Hand Gesture Recognition

**Author:** Maaz Hasan  
**Degree:** BTech CSE (AI)  
**Roll No.:** 2021-350-019

##Project Overview

The AI Virtual Mouse project is aimed at developing a hands-free mouse control system using computer vision and machine learning techniques. This project utilizes the MediaPipe library and OpenCV to detect hand gestures and control the mouse cursor accordingly. The virtual mouse system enables users to interact with computers without the need for physical input devices such as a mouse or touchpad.

##Objectives

Develop a real-time hand tracking system using MediaPipe and OpenCV. Implement fingertip detection to track hand movements accurately. Enable mouse cursor control based on hand gestures. Incorporate click functionality using hand gestures. Ensure user-friendly operation and intuitive interface.

---

##Features

- Detects hand landmarks using MediaPipe
- Tracks pinky fingertip to control cursor
- Smooth cursor movement with jitter reduction
- Scroll using thumb + index/middle finger gestures
- Click (left/right) using thumb + index/middle finger gestures (left hand only)
- Visual indicator for left/right hand detection in the top-right of the frame
- Region of Interest (ROI) shown for improved tracking
- Simple GUI interface using Tkinter to start and stop the program

---

##Hand Gesture Controls

| Gesture                             | Action                   |
|-------------------------------------|--------------------------|
| Move pinky fingertip                | Move cursor              |
| Right hand: Thumb + Index close     | Scroll up                |
| Right hand: Thumb + Middle close    | Scroll down              |
| Left hand: Thumb + Index close      | Left click               |
| Left hand: Thumb + Middle close     | Right click              |

---

## 🛠️ Technologies Used

- [MediaPipe](https://google.github.io/mediapipe/) – Hand landmark detection
- [OpenCV](https://opencv.org/) – Video frame capture and drawing
- [PyAutoGUI](https://pyautogui.readthedocs.io/) – Cursor and mouse automation
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – GUI interface

---

### 📋 Prerequisites

Make sure Python 3.7 or higher is installed, and run the following to install required libraries:

```bash
pip install mediapipe opencv-python pyautogui
