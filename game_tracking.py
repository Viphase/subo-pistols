from numpy import array, int32
from cv2 import minEnclosingCircle
from math import acos, degrees
from utils.line import crossRS as cross_ray_segment



def finger_dist(first, second, hand, shape) -> float:
    if hand is None:
        return 0  

    lm = hand
    x1, y1 = lm[first].x * shape[1], lm[first].y * shape[0]
    x2, y2 = lm[second].x * shape[1], lm[second].y * shape[0]
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

def is_pistol(hand, shape) -> bool:

    v1  = finger_dist(0, 20, hand, shape)
    v2 = finger_dist(0, 18, hand, shape)
    v3 = finger_dist(0, 12, hand, shape)
    v4 = finger_dist(0, 10, hand, shape)
    v5 = finger_dist(0, 16, hand, shape)
    v6 = finger_dist(0, 14, hand, shape)
    v7 = finger_dist(12, 8, hand, shape)
    v8 = finger_dist(10, 8, hand, shape)
    v9 = finger_dist(4, 5, hand, shape)
    v10 = finger_dist(4, 9, hand, shape)

    return (v1 - v2 < 0 
            and v3 - v4 < 0 
            and v5 - v6 < 0 
            and v7 - v8 > 0 
            and v10 - v9 > 0)

def is_shield(hands, shape) -> bool:
    if hands is None:
        return False

    lm = hands
    points = []

    for mark in lm:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    points = array(points, dtype=int32)

    x1, y1 = lm[0].x * shape[1], lm[0].y * shape[0]
    x2, y2 = lm[5].x * shape[1], lm[5].y * shape[0]

    ws = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5
    _, r = minEnclosingCircle(points)
    return (2 * r / ws) < 1.6

def round(first_player, second_player, shape):

    if first_player.right_hand is not None and is_pistol(first_player.right_hand, shape):
        first_player.state = "Gun"
    elif first_player.left_hand is not None and is_shield(first_player.left_hand, shape):
        first_player.state = "Shield"
    else:
        first_player.state = "Nothing"

    if second_player.right_hand is not None and is_pistol(second_player.right_hand, shape):
        second_player.state = "Gun"
    elif second_player.left_hand is not None and is_shield(second_player.left_hand, shape):
        second_player.state = "Shield"
    else:
        second_player.state = "Nothing"

    if  first_player.state == "Gun" and cross_ray_segment(first_player.bullet, second_player.collider):
        if second_player.state == "Shield" and not cross_ray_segment(first_player.bullet, second_player.shield):
            first_player.shoot(second_player)
            return "First", f"FIrst: {first_player.state}", f"Second {second_player.state}"
        else:
            return "Same", f"FIrst: {first_player.state}", f"Second {second_player.state}"
        
    elif  second_player.state == "Gun" and cross_ray_segment(second_player.bullet, first_player.collider):
        if first_player.state == "Shield" and not cross_ray_segment(second_player.bullet, first_player.shield):
            second_player.shoot(first_player)
            return "Second", f"FIrst: {first_player.state}", f"Second {second_player.state}"
        else:
            return "Same", f"FIrst: {first_player.state}", f"Second {second_player.state}"
    
    else:
        return "Same", f"FIrst: {first_player.state}", f"Second {second_player.state}"
        