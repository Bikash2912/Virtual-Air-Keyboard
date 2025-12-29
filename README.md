# Virtual Air Keyboard

A real time **computer vision–based virtual keyboard** that enables **touchless typing** using hand gestures captured from a webcam.  
The system detects hand landmarks, tracks fingertip movement, and allows intentional typing using a **posture-gated interaction model**.

---

## 📌 Project Overview

This project implements a **virtual air-typing interface** where users can type characters by hovering their index finger over a virtual keyboard and confirming input using a controlled hand posture and pinch gesture.
The application is designed with a **modular architecture**, separating perception, interaction, and control logic, making it stable, extensible, and portfolio-ready.

---

## ✨ Key Features

- Real-time hand tracking using a standard webcam  
- Floating **QWERTY virtual keyboard** rendered on screen  
- **Mirror-mode camera view** for intuitive interaction  
- Fingertip-based cursor control  
- **Posture-gated typing mode** to prevent accidental input  
- Pinch-based key press confirmation with debounce  
- Visual feedback for:
  - Move mode vs Typing mode
  - Hovered keys
  - Fingertip and thumb positions  
- Typed text displayed clearly below the keyboard  

---

## 🧠 Interaction Design

### 🎨 User Interface Layout

- Top Section: Virtual Keyboard
-  Bottom Section: Typed Text Output
- Top-Left: Mode Indicator (MOVE / TYPING)
- Finger Markers:
- Yellow → Index finger
- Purple → Thumb

### Modes of Operation

#### 🔴 Move Mode
- Default state
- Free hand movement
- No typing allowed

#### 🟢 Typing Mode
Typing is enabled **only when**:
- Thumb is extended
- Index finger is extended
- Middle, ring, and pinky fingers are closed
- Hand posture is stable for a short duration
---

## 🎮 How Typing Works

1. Move your **index finger** to hover over a key  
2. Enter **Typing Mode** using the defined hand posture  
3. **Pinch thumb and index finger** to confirm the key press  
4. Release pinch to prepare for the next character  
---

## 🗂️ Project Structure

─ main.py # Application orchestration & UI layout
─ camera.py # Webcam handling
─ hand_track.py # MediaPipe hand landmark detection
─ finger_track.py # Fingertip tracking & smoothing
─ virt_key.py # Virtual keyboard layout & rendering
─ press_det.py # Pinch detection & debounce logic
─ gest_det.py # Typing mode posture detection
─ key_controller.py # OS-level keyboard input


---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – video capture, rendering, UI
- **MediaPipe Hands** – real-time hand landmark detection
- **PyAutoGUI** – keyboard input simulation
- **NumPy / Math** – geometric calculations

---


