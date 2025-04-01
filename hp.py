import cv2
import numpy as np
import time

def cap_background(cap, num_frames=30):
    print("Capturing background...please move away from the camera")
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print("Error capturing frame")

        time.sleep(0.1)
    if backgrounds:
        return np.median(np.array(backgrounds), axis=0).astype(np.uint8)
    else:
        raise Exception("Error capturing background")

def create_mask(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

def apply_cloak(frame, mask, background):
    mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    bg = cv2.bitwise_and(background, background, mask=mask)
    return cv2.add(fg, bg)

def main():
    print("open cv version:", cv2.__version__)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening video capture")
        return
    try:
        background = cap_background(cap)
    except Exception as e:
        print(str(e))
        cap.release()
        return
    
    lower_black = np.array([0, 0, 0])       # Lower bound for black
    upper_black = np.array([180, 255, 50]) # Upper bound for black



    print("starting main loop")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            time.sleep(1)
            continue

        mask = create_mask(frame, lower_black, upper_black)
        cloak = apply_cloak(frame, mask, background)
        cv2.imshow("Harry Potter Cloak", cloak)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


