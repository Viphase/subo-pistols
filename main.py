from cv2 import VideoCapture, CAP_PROP_BUFFERSIZE, imshow, waitKey, flip
from utils.tracking import MediaPipeFacade, split_players
from game_tracking import *


def main():
    cap = VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 360)
    cap.set(CAP_PROP_BUFFERSIZE, 1)

    mp_facade = MediaPipeFacade()

    first_player = Human(None, None, (640, 360)) # hands_results pose_results image_shape
    second_player = Human(None, None, (640, 360))# hands_results pose_results image_shape

    frame_number = 0
    while True:
        cap.grab()
        ret, frame = cap.retrieve()
        frame = flip(frame, 1)
        if not ret:
            break
        
        if frame_number % 3 == 0:
            frame, hands_results, pose_results = mp_facade.process_frame(frame, debug=True)
        
        frame_number += 1

        left_pose, right_pose, left_hands, right_hands = split_players(
            pose_results,
            hands_results,
            frame.shape
        )

        first_player.pose = left_pose
        first_player.left_hand = left_hands[0]
        first_player.right_hand = left_hands[1]
        first_player.img_shape = frame.shape

        second_player.pose = right_pose
        second_player.left_hand = right_hands[0]
        second_player.right_hand = right_hands[1]
        second_player.img_shape = frame.shape

        first_player.update_state(frame.shape)
        second_player.update_state(frame.shape)

        debugf(frame, first_player, second_player)

        imshow("Cowboy Shootout", frame)
        if waitKey(1) == ord('q'):
            break

if __name__ == "__main__":
    main()
