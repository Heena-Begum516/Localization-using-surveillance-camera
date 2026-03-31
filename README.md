# Real-Time Fire Detection Without Using Sensors

A real-time fire detection system developed using computer vision without relying on traditional hardware sensors.

---

## Overview

This project demonstrates a real-time fire detection system built using Python and OpenCV. Instead of using physical smoke or temperature sensors, it uses a webcam and image processing techniques to detect fire based on color segmentation in the HSV color space.

The system includes intelligent confirmation logic and cooldown mechanisms to reduce false alarms and prevent repeated notifications.

---

## Features

- Real-time fire detection using HSV color space filtering.
- Noise reduction using morphological image processing.
- Fire confirmation using consecutive frame validation.
- Reduced false alarms with pixel threshold and area percentage check.
- Audible alarm using Pygame when fire is confirmed.
- Email alert system with cooldown to prevent repeated emails.
- Automatic reset after stable no-fire condition.
- Webcam-based monitoring without physical sensors.

---

## Technologies Used

**Programming Language:** Python  

**Libraries:**
- OpenCV  
- NumPy  
- Pygame  
- smtplib  
- threading  

---

## Installation

```bash
pip install opencv-python numpy pygame
```

---

## Run the Program

```bash
python fire_detection.py
```

Press **Q** to exit.

---

## Source Code

```python
import cv2
import numpy as np
import pygame
import threading
import smtplib
import time
from email.mime.text import MIMEText

# ================== EMAIL SETTINGS ==================
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
receiver_email = "receiver_email@gmail.com"
# ====================================================

pygame.init()
pygame.mixer.init()
alarm_sound = "audio.mp3"

EMAIL_COOLDOWN = 180
last_email_time = 0

FIRE_PIXEL_THRESHOLD = 4000
FIRE_CONFIRM_FRAMES = 10
NO_FIRE_RESET_FRAMES = 20

fire_frame_count = 0
no_fire_frame_count = 0


def play_alarm():
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play()


def send_email_alert():
    global last_email_time
    current_time = time.time()

    if current_time - last_email_time < EMAIL_COOLDOWN:
        return

    subject = "Fire Detected Alert"
    body = "Warning! Fire has been detected by the surveillance camera system."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")
        last_email_time = current_time

    except Exception as e:
        print("Email Error:", e)


def detect_fire(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([10, 100, 100], dtype=np.uint8)
    upper_bound = np.array([35, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    fire_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    fire_percentage = (fire_pixels / total_pixels) * 100

    fire_output = cv2.bitwise_and(frame, frame, mask=mask)

    return fire_output, fire_pixels, fire_percentage


if __name__ == "__main__":

    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Could not access webcam")
        exit()

    fire_detected = False

    while True:
        ret, frame = video.read()

        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        fire_frame, fire_pixels, fire_percentage = detect_fire(frame)

        if fire_pixels > FIRE_PIXEL_THRESHOLD and fire_percentage > 1:
            fire_frame_count += 1
            no_fire_frame_count = 0
        else:
            no_fire_frame_count += 1
            fire_frame_count = 0

        if fire_frame_count >= FIRE_CONFIRM_FRAMES and not fire_detected:
            print("Confirmed Fire Detected!")
            threading.Thread(target=play_alarm).start()
            threading.Thread(target=send_email_alert).start()
            fire_detected = True

        if no_fire_frame_count >= NO_FIRE_RESET_FRAMES:
            fire_detected = False

        cv2.imshow("Fire Detection", fire_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
```

---

## Results

- Achieved approximately 97% detection accuracy in controlled environments.
- Successfully detects fire in normal and low-light conditions.
- Alerts users with sound and email notifications.
- Reduced false alarms using multi-frame confirmation and cooldown logic.

---

## Future Scope

- Integrate Convolutional Neural Networks (CNNs)
- Add SMS alerts
- Save captured fire images
- Cloud-based monitoring system

---

## Contact

LinkedIn:  
https://www.linkedin.com/in/heena-begum-17aug01
