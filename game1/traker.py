import cv2
import mediapipe as mp
from base.base_tracker import Base_Tracker

class Tracker(Base_Tracker):
 
    
    def __init__(self,width,hight):
        super().__init__(width,hight)
        self. mpface=mp.solutions.face_mesh
        self.face=self.mpface.FaceMesh()

    def TrackHands(self,currentobj,position,frame,frame_RBG):
          
        result = self.hands.process(frame_RBG)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:

                h, w, _ = frame.shape
                lm = hand.landmark

                # 4 purple points on palm
                palm_ids = [0, 5, 9, 13]
                palm_points = []

                for pid in palm_ids:
                    px, py = int(lm[pid].x * w), int(lm[pid].y * h)
                    palm_points.append([px, py])
                    cv2.circle(frame, (px, py), 8, (255, 0, 255), cv2.FILLED)

                # Detect open hand
                palm_center = palm_points[2]
                finger_tip = lm[12]  # middle finger tip

                fx, fy = int(finger_tip.x * w), int(finger_tip.y * h)
                cv2.circle(frame, (fx, fy), 8, (0, 255, 0), cv2.FILLED)

                distance = ((fx - palm_center[0])**2 + (fy - palm_center[1])**2) ** 0.5
                hand_open = distance > 40

                obj_h, obj_w, _ = currentobj["img"].shape

                if hand_open:
                    for pos in palm_points:
                        if (pos[0] >= position[0] and
                            pos[0] <= position[0] + obj_w and
                            pos[1] >= position[1] and
                            pos[1] <= position[1] + obj_h):

                            if currentobj["is_eatable"]:
                                self.score += 1
                            else:
                                self.score = 0

                            position[1] = self.hight + 1

                self.mpDraw.draw_landmarks(frame, hand, self.mpHand.HAND_CONNECTIONS)

        return self.score

    def TrackFace(self,currentobj,position,frame,frame_RBG):
          result=self.face.process(frame_RBG)
          if result.multi_face_landmarks:
            for face in result.multi_face_landmarks:   
             self.mpDraw.draw_landmarks(
              frame,
              face,
              self.mpface.FACEMESH_LIPS,
              self.drawSpec,
              self.drawSpec
          )           
            top = face.landmark[0]
            bottom = face.landmark[17]
            left = face.landmark[61]
            right = face.landmark[291]

          
            h, w, _ = frame.shape

            top_pt = [int(top.x * w), int(top.y * h)]
            bottom_pt = [int(bottom.x * w), int(bottom.y * h)]
            left_pt = [int(left.x * w), int(left.y * h)]
            right_pt = [int(right.x * w), int(right.y * h)]

           
            center_x = int((left_pt[0] + right_pt[0]) / 2)
            center_y = int((top_pt[1] + bottom_pt[1]) / 2)

            center = [center_x, center_y]
            Mouth_Open=bottom_pt[1]-top_pt[1]
         
            cv2.circle(frame, top_pt, 4, (255,0,0), cv2.FILLED)
            cv2.circle(frame, bottom_pt, 4, (255,0,0), cv2.FILLED)
            cv2.circle(frame, left_pt, 4, (255,0,0), cv2.FILLED)
            cv2.circle(frame, right_pt, 4, (255,0,0), cv2.FILLED)
            cv2.circle(frame, center, 8, (0,0,255), cv2.FILLED)
            obj_h, obj_w, _ = currentobj["img"].shape
            if (center[0] >= position[0] and
                        center[0] <= position[0] + obj_w and
                        center[1] >= position[1] and
                        center[1] <= position[1] + obj_h):
                 
                if Mouth_Open>82:
                 if currentobj["is_eatable"] :
                        self.score=self.score+1
                        position[1]=self.hight+1
               
                 elif currentobj["is_eatable"]==False:
                          self.score=0
                          position[1]=self.hight+1
                
               
           
            return self.score