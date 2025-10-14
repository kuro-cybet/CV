# 🌀 Optical Illusion Analyzer (Full Version)
# Author: Kuro + GPT-5
# Features:
# 1. Interactive Checker Shadow Illusion
# 2. Rotating Snakes Motion Illusion
# 3. Brightness Gradient Illusion
# 4. Pixel Intensity Analysis

import cv2
import numpy as np

# === GLOBAL VARIABLES ===
clicked_points = []

# ====================== Checker Shadow ======================
def create_checker_shadow(height=400, width=600, checker_size=50):
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    # Checkerboard
    for y in range(0, height, checker_size):
        for x in range(0, width, checker_size):
            if (x // checker_size + y // checker_size) % 2 == 0:
                cv2.rectangle(img, (x, y), (x+checker_size, y+checker_size), (100, 100, 100), -1)
    # Shadow
    shadow_color = (50, 50, 50)
    overlay = img.copy()
    cv2.rectangle(overlay, (200, 100), (400, 300), shadow_color, -1)
    alpha = 0.5
    img = cv2.addWeighted(overlay, alpha, img, 1-alpha, 0)
    return img

def click_event(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Clicked at {x}, {y} -> Intensity:", param[y, x])
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)

# ====================== Rotating Snakes ======================
def create_rotating_snakes(radius=150, rings=6, segments=12):
    size = radius*2 + 50
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    center = size//2
    angles = np.linspace(0, 2*np.pi, segments, endpoint=False)
    colors = [(0,0,0), (255,255,255)]
    for r in range(rings):
        rad_inner = r * radius // rings
        rad_outer = (r+1) * radius // rings
        for i, angle in enumerate(angles):
            color = colors[i % 2]
            pt1 = (int(center + rad_inner*np.cos(angle)), int(center + rad_inner*np.sin(angle)))
            pt2 = (int(center + rad_outer*np.cos(angle)), int(center + rad_outer*np.sin(angle)))
            cv2.line(img, pt1, pt2, color, 10)
    return img

# ====================== Brightness Gradient ======================
def create_brightness_gradient(width=600, height=100):
    gradient = np.tile(np.linspace(0, 255, width, dtype=np.uint8), (height, 1))
    gradient_img = cv2.merge([gradient]*3)
    return gradient_img

# ====================== MAIN ======================
checker_img = create_checker_shadow()
snake_img = create_rotating_snakes()
gradient_img = create_brightness_gradient()

cv2.namedWindow("Checker Shadow Illusion")
cv2.setMouseCallback("Checker Shadow Illusion", click_event, checker_img)

while True:
    cv2.imshow("Checker Shadow Illusion", checker_img)
    cv2.imshow("Rotating Snakes Motion Illusion", snake_img)
    cv2.imshow("Brightness Gradient Illusion", gradient_img)

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
