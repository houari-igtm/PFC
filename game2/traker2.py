import cv2
import mediapipe as mp


class Tracker:
 
    
    def __init__(self,width,hight):
        self. mpface=mp.solutions.face_mesh
        self.face=self.mpface.FaceMesh()
        self.mpDraw=mp.solutions.drawing_utils
        self.drawSpec=self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        self.mpHand=mp.solutions.hands
        self.hands=self.mpHand.Hands()
        self.mpDraw=mp.solutions.drawing_utils
        self.width=0
        self.hight=0
        self.score=0
        self.width=width
        self.hight=hight
        self.status=None
        self.result=None

    def TrackHands(self,currentobj,positions,frame,frame_RBG ,Name):
          self.status = ""
          result=self.hands.process(frame_RBG)
          if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
              for id ,point in enumerate(hand.landmark):
               
                if id==9:
                   px ,py=int(point.x*self.width),int(point.y*self.hight)
                   cv2.circle(frame,(px,py),8,(255,255,255),cv2.FILLED)
                   pos=[px,py]
                   for i,obj in enumerate(currentobj):
                    obj_h, obj_w, _ = obj["img"].shape
                    if (pos[0] >= positions[i][0] and
                            pos[0] <= positions[i][0] + obj_w and
                            pos[1] >= positions[i][1] and
                            pos[1] <= positions[i][1] + obj_h):
                        if obj["name"]==Name :
                            self.score=self.score+1
                            self.status="change"
                            self.result = "correct"
                            
                            break
                        elif obj["name"]!=Name:
                            self.score=0
                            self.status="change"
                            self.result = "wrong"
                            break
                    
            
            self.mpDraw.draw_landmarks(frame,hand,self.mpHand.HAND_CONNECTIONS)
          return self.score,self.status,self.result


