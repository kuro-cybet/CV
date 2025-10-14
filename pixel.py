# 🎥 OpenCV Pixelated Background Webcam (No MediaPipe)
# Author: Kuro + GPT-5
# Description: Real-time pixelated background, foreground preserved using motion detection

import cv2
import numpy as np

pixel_size = 32  # Adjust for chunkiness
bg_replace = False  # Toggle background replacement
bg_image_path = "background.jpg"  # Optional background image

# Load optional background image
bg_image = cv2.imread(bg_image_path) if bg_replace else None

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("❌ Cannot open webcam")

# Create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

print("🎮 Controls: ↑/↓ to change pixel size, b to toggle background, q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # === Background subtraction mask ===
    mask = fgbg.apply(frame)
    mask = cv2.threshold(mask, 200, 1, cv2.THRESH_BINARY)[1]  # foreground=1, background=0
    mask_3ch = np.dstack([mask]*3)

    # Pixelate background
    temp = cv2.resize(frame, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
    pixelated_bg = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

    # Optional replace background with image
    if bg_replace and bg_image is not None:
        pixelated_bg = cv2.resize(bg_image, (w, h))

    # Combine foreground and background
    output = (frame * mask_3ch + pixelated_bg * (1 - mask_3ch)).astype(np.uint8)

    cv2.imshow("Pixelated Background (OpenCV)", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('b'):
        bg_replace = not bg_replace
        if bg_replace and bg_image is None:
            bg_image = np.zeros_like(frame)
    elif key == 82:  # Up arrow
        pixel_size = min(pixel_size + 4, 128)
    elif key == 84:  # Down arrow
        pixel_size = max(pixel_size - 4, 8)

cap.release()
cv2.destroyAllWindows()
