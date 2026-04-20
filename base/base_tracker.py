import cv2
import mediapipe as mp
class Base_Tracker:
    def __init__(self,width,hight):
        self.mpDraw=mp.solutions.drawing_utils
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.mpHand=mp.solutions.hands
        self.hands=self.mpHand.Hands()
        self.score=0
        self.width=width
        self.hight=hight
        self.status=None
        self.result=None