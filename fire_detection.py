import cv2
import numpy as np
import pygame
import threading
import smtplib
import time
import datetime
from email.mime.text import MIMEText

# ================== EMAIL SETTINGS ==================
sender_email = "ayesha.h33n4@gmail.com"
sender_password = "lwfi wwcs obfi fbyl" 
receiver_email = "heena.begum.1781@gmail.com"
# ====================================================

# ================== INIT ==================
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


# ------------------ FIXED LOCATION ------------------
def get_location():
    location_text = "🚨 Fire Detected Location"
    maps_link = "https://share.google/ytRpocem2JPQEuKtG"
    return location_text, maps_link


# ------------------ ALARM ------------------
def play_alarm():
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play()


# ------------------ EMAIL ALERT ------------------
def send_email_alert(location, maps_link):
    global last_email_time

    current_time = time.time()

    # ⏱️ Avoid repeated emails
    if current_time - last_email_time < EMAIL_COOLDOWN:
        return

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = "🔥 Fire Detected Alert"
    body = f"""
🔥 Fire Detected!

Time: {time_now}
Location: {location}

📍 View on Google Maps:
{maps_link}

⚠️ Immediate attention required!
"""

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

        print("✅ Email sent successfully")
        last_email_time = current_time

    except Exception as e:
        print("❌ Email Error:", e)


# ------------------ FIRE DETECTION ------------------
def detect_fire(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Fire color range
    lower = np.array([10, 100, 100], dtype=np.uint8)
    upper = np.array([35, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    # Noise removal
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    fire_pixels = cv2.countNonZero(mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    fire_percentage = (fire_pixels / total_pixels) * 100

    output = cv2.bitwise_and(frame, frame, mask=mask)

    return output, fire_pixels, fire_percentage


# ================== MAIN ==================
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot access webcam")
        exit()

    fire_detected = False

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        fire_frame, fire_pixels, fire_percentage = detect_fire(frame)

        cv2.putText(frame, "🔥 Fire Monitoring Active", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Detection logic
        if fire_pixels > FIRE_PIXEL_THRESHOLD and fire_percentage > 1:
            fire_frame_count += 1
            no_fire_frame_count = 0
        else:
            no_fire_frame_count += 1
            fire_frame_count = 0

        # 🔥 FIRE CONFIRMED
        if fire_frame_count >= FIRE_CONFIRM_FRAMES and not fire_detected:
            print("🔥 Confirmed Fire Detected!")

            location_text, maps_link = get_location()

            # Alarm + Email in parallel
            threading.Thread(target=play_alarm).start()
            threading.Thread(
                target=send_email_alert,
                args=(location_text, maps_link)
            ).start()

            fire_detected = True

        # Reset system
        if no_fire_frame_count >= NO_FIRE_RESET_FRAMES:
            fire_detected = False

        cv2.imshow("Fire Detection", fire_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()