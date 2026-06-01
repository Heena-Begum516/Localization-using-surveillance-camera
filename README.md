# Real-Time Fire Detection and Alert System Without Using Sensors

A computer vision-based fire detection system that monitors live video from a webcam, detects fire using image processing techniques, plays an alarm, and sends email alerts with location information — all without using traditional fire sensors.

---

## Overview

This project implements a real-time fire detection system using Python, OpenCV, and image processing techniques. Instead of relying on smoke or temperature sensors, the system analyzes webcam footage and identifies fire-like regions based on HSV color segmentation.

To improve reliability, the system includes:

* Fire confirmation using consecutive frame validation.
* Skin-color removal to reduce false positives.
* Morphological operations for noise reduction.
* Audible alarm notifications.
* Email alerts containing detection time and location information.
* Cooldown mechanism to avoid repeated email notifications.

---

## Features

* 🔥 Real-time fire detection using webcam.
* 🎨 HSV color-space fire segmentation.
* 🚫 Skin-tone filtering to reduce false alarms.
* 🧹 Morphological noise removal and image enhancement.
* ✅ Multi-frame confirmation before triggering alerts.
* 🔊 Audible alarm using Pygame.
* 📧 Automated email alerts with timestamp.
* 📍 Location and Google Maps link included in email.
* ⏱ Email cooldown mechanism to prevent spam.
* 🔄 Automatic reset when fire is no longer detected.
* 💻 Works without dedicated fire sensors.

---

## Technologies Used

### Programming Language

* Python

### Libraries

* OpenCV
* NumPy
* Pygame
* threading
* smtplib
* datetime
* time

---

## System Workflow

```text
Webcam Input
      │
      ▼
Capture Video Frame
      │
      ▼
Convert Frame to HSV
      │
      ▼
Detect Fire Colors
      │
      ▼
Remove Skin-Tone Regions
      │
      ▼
Noise Reduction
      │
      ▼
Calculate Fire Pixels
      │
      ▼
Consecutive Frame Validation
      │
      ▼
Fire Confirmed?
   ┌───────┴───────┐
   │               │
  No              Yes
   │               │
Continue      Alarm + Email Alert
Monitoring          │
                    ▼
            Continue Monitoring
```

---

## Installation

Install the required dependencies:

```bash
pip install opencv-python numpy pygame
```

---

## Project Structure

```text
Fire-Detection-System/
│
├── fire_detection.py
├── audio.mp3
├── README.md
```

---

## Configuration

Update the email credentials in the source code:

```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
receiver_email = "receiver_email@gmail.com"
```

For Gmail:

1. Enable Two-Factor Authentication.
2. Generate an App Password.
3. Use the generated App Password in the program.

---

## Run the Program

```bash
python fire_detection.py
```

Press **Q** to stop monitoring.

---

## Fire Detection Methodology

### 1. HSV Color Segmentation

The webcam frame is converted from BGR to HSV format:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

Fire-colored regions are detected using:

```python
lower_fire = np.array([5, 150, 150])
upper_fire = np.array([25, 255, 255])
```

---

### 2. Skin Color Removal

To reduce false alarms caused by human skin tones:

```python
lower_skin = np.array([0, 30, 60])
upper_skin = np.array([20, 150, 255])
```

The skin mask is removed from the fire mask:

```python
fire_mask = cv2.subtract(fire_mask, skin_mask)
```

---

### 3. Noise Reduction

Morphological operations are applied:

```python
cv2.morphologyEx()
cv2.dilate()
```

These operations eliminate small noise regions and strengthen detected fire areas.

---

### 4. Fire Confirmation Logic

A fire is confirmed only when:

```python
fire_pixels > 3000
```

and

```python
fire_percentage > 0.8
```

for at least:

```python
FIRE_CONFIRM_FRAMES = 10
```

consecutive frames.

---

### 5. Alert Generation

When fire is confirmed:

* Alarm sound is played.
* Email alert is sent.
* Detection time is recorded.
* Location and Google Maps link are included.

Example email:

```text
🔥 Fire Detected!

Time: 2026-06-01 15:45:10
Location: Fire Location

📍 https://maps.app.goo.gl/94J8VKF3hzUV2KZF6
```

---

## Results

### Performance

* Real-time fire detection using a standard webcam.
* Reliable detection of visible flames.
* Reduced false alarms through skin filtering and frame confirmation.
* Immediate audio and email notifications.
* Stable performance under varying lighting conditions.

### Alert Features

* Alarm activation upon confirmed fire.
* Timestamped email notifications.
* Google Maps location sharing.
* Email spam prevention through cooldown control.

---

## Future Enhancements

* Integrate Deep Learning models (CNN/YOLO).
* Smoke detection capability.
* GPS-based live location tracking.
* SMS and WhatsApp notifications.
* Automatic image capture during fire events.
* Cloud dashboard for remote monitoring.
* Multi-camera support.
* Mobile application integration.

---

## Limitations

* Detects visible flames only.
* Does not currently detect smoke.
* Bright orange objects may occasionally trigger false positives.
* Fixed location link is currently used instead of dynamic GPS coordinates.

---

## Contact

### Heena Begum

**LinkedIn:**
[Heena Begum LinkedIn Profile](https://www.linkedin.com/in/heena-begum-17aug01?utm_source=chatgpt.com)

---

### Project Summary

This project demonstrates how computer vision can be used to build a low-cost, real-time fire detection and alert system without relying on specialized hardware sensors. By combining image processing, automated alerts, and confirmation logic, the system provides an effective foundation for smart surveillance and fire safety applications.
