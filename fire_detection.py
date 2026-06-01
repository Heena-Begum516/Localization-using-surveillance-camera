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

# ================== INIT ==================
pygame.init()
pygame.mixer.init()
alarm_sound = "audio.mp3"

EMAIL_COOLDOWN = 180
last_email_time = 0

FIRE_PIXEL_THRESHOLD = 3000   # lowered for working
FIRE_CONFIRM_FRAMES = 10
NO_FIRE_RESET_FRAMES = 20

fire_frame_count = 0
no_fire_frame_count = 0

# ------------------ LOCATION ------------------
def get_location():
    return "🚨 Fire Location", "https://maps.app.goo.gl/94J8VKF3hzUV2KZF6"

# ------------------ ALARM ------------------
def play_alarm():
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play()

# ------------------ EMAIL ------------------
def send_email_alert(location, maps_link):
    global last_email_time

    if time.time() - last_email_time < EMAIL_COOLDOWN:
        return

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = MIMEText(f"""
🔥 Fire Detected!

Time: {time_now}
Location: {location}

📍 {maps_link}
""")

    msg["Subject"] = "🔥 Fire Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("✅ Email Sent")
        last_email_time = time.time()

    except Exception as e:
        print("❌ Email Error:", e)

# ------------------ DETECTION ------------------
def detect_fire(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔥 Fire color (tight range)
    lower_fire = np.array([5, 150, 150], dtype=np.uint8)
    upper_fire = np.array([25, 255, 255], dtype=np.uint8)
    fire_mask = cv2.inRange(hsv, lower_fire, upper_fire)

    # 🚫 Skin removal (important)
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    fire_mask = cv2.subtract(fire_mask, skin_mask)

    # 🧹 Clean noise
    kernel = np.ones((5, 5), np.uint8)
    fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
    fire_mask = cv2.dilate(fire_mask, kernel, iterations=2)

    fire_pixels = cv2.countNonZero(fire_mask)
    total_pixels = frame.shape[0] * frame.shape[1]
    fire_percentage = (fire_pixels / total_pixels) * 100

    output = cv2.bitwise_and(frame, frame, mask=fire_mask)

    return output, fire_pixels, fire_percentage

# ================== MAIN ==================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not working")
    exit()

fire_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))

    fire_frame, fire_pixels, fire_percentage = detect_fire(frame)

    cv2.putText(frame, "🔥 Monitoring", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Detection logic
    if fire_pixels > FIRE_PIXEL_THRESHOLD and fire_percentage > 0.8:
        fire_frame_count += 1
        no_fire_frame_count = 0
    else:
        no_fire_frame_count += 1
        fire_frame_count = 0

    # 🔥 CONFIRMED
    if fire_frame_count >= FIRE_CONFIRM_FRAMES and not fire_detected:
        print("🔥 FIRE DETECTED!")

        loc, link = get_location()

        threading.Thread(target=play_alarm).start()
        threading.Thread(target=send_email_alert, args=(loc, link)).start()

        fire_detected = True

    # Reset
    if no_fire_frame_count >= NO_FIRE_RESET_FRAMES:
        fire_detected = False

    cv2.imshow("Fire Detection", fire_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()