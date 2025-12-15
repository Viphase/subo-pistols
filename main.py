from cv2 import (VideoCapture, putText, imshow,
waitKey, destroyAllWindows, FONT_HERSHEY_SIMPLEX, LINE_AA)
from utils.tracking import MediaPipeFacade
from game_tracking import *

def main():
    cap = VideoCapture(0)
    mp_facade = MediaPipeFacade()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, tracked = mp_facade.process_frame(frame, debug=True)
        labels = []

        for i, human in enumerate(tracked[:2]):
            if human.right_hand is not None and is_pistol(human.right_hand, frame.shape):
                text = f"Player {i+1} Right Hand: GUN"
                color = (0, 255, 0)
            else:
                text = f"Player {i+1} Right Hand: NO GUN"
                color = (0, 0, 255)
            labels.append((text, color))

        y = 50
        for text, color in labels:
            putText(frame, text, (50, y), FONT_HERSHEY_SIMPLEX, 0.8, color, 2, LINE_AA)
            y += 40
        imshow("kartinka", frame)
        key = waitKey(1)
        if key == ord('q'):
            cap.release()
            destroyAllWindows()
            break


if __name__ == "__main__":
    main()
