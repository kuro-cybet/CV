import cv2
import mss

threshold = 15
prev_board = None

with mss.mss() as sct:
    monitor = {"top": 100, "left": 100, "width": 480, "height": 480}  # Set online board area

    running = True
    while running:
        screenshot = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Divide into 8x8 squares
        h, w = gray.shape[:2]
        square_h, square_w = h//8, w//8
        board_intensity = np.zeros((8,8))
        for i in range(8):
            for j in range(8):
                square = gray[i*square_h:(i+1)*square_h, j*square_w:(j+1)*square_w]
                board_intensity[i,j] = np.mean(square)

        if prev_board is not None:
            diff = np.abs(board_intensity - prev_board)
            moves = np.argwhere(diff > threshold)
            for move in moves:
                row, col = move
                # Update board state
                board_state[row, col] = 1 if board_state[row, col]==0 else 0
                print(f"Detected move at: {row+1},{col+1}")

        prev_board = board_intensity.copy()

        # Draw board in Pygame
        draw_board(WIN, board_state)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

pygame.quit()
