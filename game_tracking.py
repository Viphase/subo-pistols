# from numpy import array, int32
# from cv2 import minEnclosingCircle
from math import acos, degrees
from utils.geometry import Vector, crossRS

def finger_dist(first, second, results) -> float:
    if results is None or not results.hand_landmarks:
        return 0  

    lm = results.hand_landmarks[0]
    x1, y1 = lm[first].x, lm[first].y
    x2, y2 = lm[second].x, lm[second].y
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5


def is_pistol(hand, shape) -> bool:
    open = 0
    closed = 0

    for i in [1, 5, 9, 13, 17]:
        prev = None
        for j in range(i, i+3):
            if j + 1 > 20:
                break
            current = Vector(
                hand[j+1].x - hand[j].x,
                hand[j+1].y - hand[j].y
            )
            if prev is not None:
                angle = degrees(acos((current * prev) / (current.dist() * prev.dist())))
                if 0 <= angle <= 20:
                    open += 1
                else:
                    closed += 1
            prev = current

    x_l = shape[1]
    y_l = shape[0]
    
    v1  = finger_dist(0, 20)
    v2 = finger_dist(0, 18)
    v3 = finger_dist(0, 12)
    v4 = finger_dist(0, 10)
    v5 = finger_dist(0, 16)
    v6 = finger_dist(0, 14)
    v7 = finger_dist(12, 8)
    v8 = finger_dist(10, 8)
    v9 = finger_dist(4, 5)
    v10 = finger_dist(4, 9)

    return (v1.dist() - v2.dist() < 0 
            and v3.dist() - v4.dist() < 0 
            and v5.dist() - v6.dist() < 0 
            and v7.dist() - v8.dist() > 0 
            and v10.dist() - v9.dist() > 0)

def shot(human1, human2):
    cross1 = crossRS(human1.bullet, human2.collider)
    cross2 = crossRS(human2.bullet, human1.collider)
    if cross1 is not None:
        return (human1, cross1.x, cross1.y)
    elif cross2 is not None:
        return (human2, cross2.x, cross2.y)
    else:
        return None

def is_shield(hands, shape) -> bool:
    if hands is None or not hands.hand_landmarks:
        return False

    lm = hands.hand_landmarks[0]
    points = []

    for mark in lm:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    points = array(points, dtype=int32)

    x1, y1 = lm[0].x * shape[1], lm[0].y * shape[0]
    x2, y2 = lm[5].x * shape[1], lm[5].y * shape[0]

    ws = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5
    _, r = minEnclosingCircle(points)
    return (2 * r / ws) > 1.6