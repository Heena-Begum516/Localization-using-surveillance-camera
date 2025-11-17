import cv2
import numpy as np
import pygame
import threading

# Initialize pygame for sound
pygame.init()
pygame.mixer.init()
alarm_sound = "audio.mp3"  # Replace with your alarm sound file

# Function to play alarm sound
def play_alarm():
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play()

# Function for fire detection
def detect_fire(frame):
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV range for detecting fire-like colors
    lower_bound = np.array([18, 50, 50], dtype=np.uint8)  # Lower range for orange/yellow
    upper_bound = np.array([35, 255, 255], dtype=np.uint8)  # Upper range for orange/yellow

    # Create a mask for fire colors
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Perform bitwise AND to isolate fire-like regions
    fire_output = cv2.bitwise_and(frame, frame, mask=mask)

    # Count non-zero pixels in the mask
    fire_pixels = cv2.countNonZero(mask)

    return fire_output, fire_pixels

# Main function
if __name__ == "__main__":
    # Open the webcam
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error: Could not access the webcam.")
        exit()

    fire_detected = False

    while True:
        ret, frame = video.read()

        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Resize the frame for consistency
        frame = cv2.resize(frame, (640, 480))

        # Detect fire in the frame
        fire_frame, fire_pixels = detect_fire(frame)

        # If fire pixels exceed a threshold, trigger the alarm
        if fire_pixels > 2000:  # Threshold value for fire detection
            if not fire_detected:
                print("Fire detected! Triggering alarm...")
                threading.Thread(target=play_alarm).start()
                fire_detected = True
        else:
            fire_detected = False

        # Display the video feed with fire detection overlay
        cv2.imshow("Fire Detection", fire_frame)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
