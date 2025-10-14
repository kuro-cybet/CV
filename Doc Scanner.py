import cv2
import numpy as np

print("🧾 Document Scanner Started")
print("➡️ Hold a paper or document in front of your webcam.")
print("➡️ Press 's' to scan and save, or 'q' to quit.")

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not detected!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    orig = frame.copy()

    # Preprocess
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)

    # Find document contour
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    # Show the actual webcam view with guides
    if screenCnt is not None:
        cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
        cv2.putText(frame, "✅ Document Detected - Press 's' to Scan",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "📄 Adjust the paper... Press 's' anytime to save.",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow("Live Document Scanner", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        print("📸 Scanning current frame...")
        if screenCnt is not None:
            warped = four_point_transform(orig, screenCnt.reshape(4, 2))
        else:
            warped = orig.copy()  # fallback if no contour

        warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        scanned = cv2.adaptiveThreshold(warped_gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
        cv2.imshow("Scanned Document", scanned)
        cv2.imwrite("scanned_output.jpg", scanned)
        print("✅ Saved as 'scanned_output.jpg'")

cap.release()
cv2.destroyAllWindows()
