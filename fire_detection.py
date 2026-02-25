import cv2
import numpy as np
import pygame
import threading
import smtplib
import time
from email.mime.text import MIMEText

# ================== EMAIL SETTINGS ==================
sender_email = "ayesha.h33n4@gmail.com"
sender_password = "lwfi wwcs obfi fbyl"
receiver_email = "heena.begum.1781@gmail.com"
# ====================================================

pygame.init()
pygame.mixer.init()
alarm_sound = "audio.mp3"

# Email cooldown (seconds)
EMAIL_COOLDOWN = 180   # Increased to 3 minutes
last_email_time = 0

# Fire confirmation settings
FIRE_PIXEL_THRESHOLD = 4000      # Increased threshold
FIRE_CONFIRM_FRAMES = 10         # Fire must appear in 10 continuous frames
NO_FIRE_RESET_FRAMES = 20        # Reset after 20 no-fire frames

fire_frame_count = 0
no_fire_frame_count = 0


# ------------------ ALARM FUNCTION ------------------
def play_alarm():
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play()


# ------------------ EMAIL FUNCTION ------------------
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


# ------------------ FIRE DETECTION ------------------
def detect_fire(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Slightly improved fire color range
    lower_bound = np.array([10, 100, 100], dtype=np.uint8)
    upper_bound = np.array([35, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Morphological operations to reduce noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    fire_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    fire_percentage = (fire_pixels / total_pixels) * 100

    fire_output = cv2.bitwise_and(frame, frame, mask=mask)

    return fire_output, fire_pixels, fire_percentage


# ================== MAIN PROGRAM ==================
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

        # Confirm fire only after continuous frames
        if fire_frame_count >= FIRE_CONFIRM_FRAMES and not fire_detected:
            print("Confirmed Fire Detected!")
            threading.Thread(target=play_alarm).start()
            threading.Thread(target=send_email_alert).start()
            fire_detected = True

        # Reset system after stable no-fire condition
        if no_fire_frame_count >= NO_FIRE_RESET_FRAMES:
            fire_detected = False

        cv2.imshow("Fire Detection", fire_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()