import cv2
import os
import time

# Ask user name
user_name = input("Enter user name: ").strip()

if user_name == "":
    print("Invalid name.")
    exit()

# Create folder structure
if not os.path.exists("users"):
    os.makedirs("users")

user_folder = os.path.join("users", user_name)

if not os.path.exists(user_folder):
    os.makedirs(user_folder)
    print("User folder created.")
else:
    print("User folder already exists. New images will be added.")

# Open camera
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Cannot access camera.")
    exit()

print("Camera started.")
print("Capturing 5 images. Look slightly left/right for better accuracy.")

image_count = 5
captured = 0

try:
    while captured < image_count:

        ret, frame = cam.read()
        if not ret:
            print("Camera read error.")
            break

        frame = cv2.resize(frame, (640, 480))

        # Show preview
        cv2.imshow("Register Face - Press Q to quit", frame)

        # Capture every 2 seconds
        if int(time.time()) % 2 == 0:
            img_path = os.path.join(user_folder, f"img_{captured}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Captured image {captured + 1}")
            captured += 1
            time.sleep(1)

        # Quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Registration completed successfully!")

finally:
    cam.release()
    cv2.destroyAllWindows()