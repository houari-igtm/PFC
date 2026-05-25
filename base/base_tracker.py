import cv2
import mediapipe as mp
class Base_Tracker:
    def __init__(self,width,hight):
        self.mpDraw=mp.solutions.drawing_utils
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.mpHand=mp.solutions.hands
        self.hands=self.mpHand.Hands( max_num_hands=1, min_detection_confidence=0.5,min_tracking_confidence=0.3)
        self.score=0
        self.width=width
        self.hight=hight
        self.status=None
        self.result=None

    def is_hand_closed(self, hand):
        tip_y = hand.landmark[12].y
        base_y = hand.landmark[9].y
        return tip_y > base_y