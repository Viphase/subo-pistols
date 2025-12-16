from mediapipe.tasks.python import vision
from mediapipe.tasks import python as mp
from mediapipe import Image, ImageFormat
from cv2 import line, circle, cvtColor, resize, COLOR_RGB2BGR, COLOR_BGR2RGB
from numpy import fliplr, hstack
from utils.geometry import Segment, Line


class MediaPipeFacade:
    def __init__(self):
        base_options_hands = mp.BaseOptions(
            model_asset_path="./models/hand_landmarker.task"
        )

        base_options_pose = mp.BaseOptions(
            model_asset_path="./models/pose_landmarker.task"
        )

        self.hands = vision.HandLandmarker.create_from_options(
            vision.HandLandmarkerOptions(
                base_options=base_options_hands,
                num_hands=4,
                min_hand_detection_confidence=0.5,
                min_hand_presence_confidence=0.5
            )
        )

        self.pose = vision.PoseLandmarker.create_from_options(
            vision.PoseLandmarkerOptions(
                base_options=base_options_pose,
                num_poses=2,
                min_pose_detection_confidence=0.5,
                min_pose_presence_confidence=0.5
            )
        )


    def process_frame(self, frame, frame_number, debug: bool = False):

        img = fliplr(frame)
        img = cvtColor(img, COLOR_BGR2RGB)
        img = resize(img, (640, 360))


        first_half = img[:, : img.shape[1] // 2, :].copy()
        second_half = img[:, img.shape[1] // 2 :, :].copy()
        mp_first_half = Image(image_format=ImageFormat.SRGB, data=first_half)
        results_hands_first = self.hands.detect(mp_first_half)
        results_pose_first = self.pose.detect(mp_first_half)

        if results_pose_first.pose_landmarks:
            n = len(results_pose_first.pose_landmarks)
            if n > 2:
                print(f"В левой части поля должен находится только один человек")
            if n < 1:
                print("Игрок должен встать в левую часть поля")

        mp_second_half = Image(image_format=ImageFormat.SRGB, data=second_half)
        results_hands_second = self.hands.detect(mp_second_half)
        results_pose_second = self.pose.detect(mp_second_half)

        if results_pose_second.pose_landmarks:
            n = len(results_pose_second.pose_landmarks)
            if n > 2:
                print(f"В левой части поля должен находится только один человек")
            if n < 1:
                print("Игрок должен встать в левую часть поля")
        # img = debugf(img, first_half.shape, results_hands_first.append(results_hands_second), results_pose_first.append(results_pose_second))
        return img, (results_hands_first,results_hands_second), (results_pose_first, results_pose_second)

# def debugf(img, half_image_shape, results_hands, results_pose):
#     if results_hands.hand_landmarks:
#         for hand in results_hands.hand_landmarks[:4]:
#             for lm in hand:
#                 px = int(lm.x * half_image_shape[1])
#                 py = int(lm.y * half_image_shape[0])
#                 circle(img, (px, py), 3, (255, 0, 0), -1)

#     if results_pose.pose_landmarks:
#         for pose in results_pose.pose_landmarks[:2]:
#             for lm in pose:
#                 px = int(lm.x * half_image_shape[1])
#                 py = int(lm.y * half_image_shape[0])
#                 circle(img, (px, py), 3, (0, 255, 0), -1)

#         line(img, (pose.collider.A.x, pose.collider.A.y), (pose.collider.B.x, pose.collider.B.y), (255,255,0), 2)
#     return cvtColor(img, COLOR_RGB2BGR)

class Human:
    def __init__(self, hands_results, pose_results, img_shape):
        self.pose = pose_results
        self.img_shape = img_shape
        self.hands_results = hands_results
        self.left_hand = hands_results
        self.right_hand = hands_results

    @property
    def left_hand(self):
        return self._left_hand
    
    @left_hand.setter
    def left_hand(self, hands_results):
        if hands_results is not None:
            for i, hand in enumerate(hands_results.hand_landmarks):
                hand_type = hands_results.handedness[i][0].category_name
                if hand_type == "Right":
                    self._left_hand = hand
        else:
            self._left_hand = None

    @property
    def right_hand(self):
        return self._right_hand
    
    @right_hand.setter
    def right_hand(self, hands_results):
        if hands_results is not None:
            for i, hand in enumerate(hands_results.hand_landmarks):
                hand_type = hands_results.handedness[i][0].category_name
                if hand_type == "Left":
                    self._right_hand = hand
        else:
            self._right_hand = None

    @property
    def collider(self):
        nose = self.pose[0]
        neck = self.pose[1]
        k1 = self.pose[31]
        k2 = self.pose[32]

        head_x = int(nose.x * self.img_shape[1])
        head_y = int(nose.y * self.img_shape[0] - 4 * (nose.y * self.img_shape[0] - neck.y * self.img_shape[0]))
        knees_x = int((k1.x + k2.x) * 0.5 * self.img_shape[1])
        knees_y = int((k1.y + k2.y) * 0.5 * self.img_shape[0])

        return Segment(head_x, head_y, knees_x, knees_y)
    
    @property
    def bullet(self):
        if self.left_hand:
            elbow = self.pose[13]
        else:
            elbow = self.pose[14]

        if self.left_hand:
            hand = self.pose[15]
        else:
            hand = self.pose[16]

        self.elbow_x = int(elbow.x * self.img_shape[1])
        self.elbow_y = int(elbow.y * self.img_shape[0])
        self.hand_x = int(hand.x * self.img_shape[1])
        self.hand_y = int(hand.y * self.img_shape[0])

        return Line(self.elbow_x, self.elbow_y, self.hand_x, self.hand_y)
