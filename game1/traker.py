import cv2
import mediapipe as mp
from base.base_tracker import Base_Tracker

class Tracker(Base_Tracker):
 
    
    def __init__(self,width,hight):
        super().__init__(width,hight)
        self. mpface=mp.solutions.face_mesh
        self.face=self.mpface.FaceMesh()
        self.lost=False

    def TrackHands(self,currentobj,position,frame,frame_RBG):
        self.lost = False
          
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
                                self.score += 100
                            else:
                                self.score = 0
                                self.lost = True
                                

                            position[1] = self.hight + 1

                self.mpDraw.draw_landmarks(frame, hand, self.mpHand.HAND_CONNECTIONS)

        return self.score,self.lost

    def TrackFace(self, currentobj, position, frame, frame_RBG):
        self.lost = False
        result = self.face.process(frame_RBG)

        if not result.multi_face_landmarks:
            return self.score, False

        h, w, _ = frame.shape

        for face in result.multi_face_landmarks:
            self.mpDraw.draw_landmarks(
                frame, face, self.mpface.FACEMESH_LIPS, self.drawSpec, self.drawSpec
            )

            lm = face.landmark

            top_ids    = [13, 312, 311, 310, 415, 308]
            bottom_ids = [14, 317, 402, 318, 324, 308]

            avg = lambda ids: sum(lm[i].y for i in ids) / len(ids)

            top_y, bottom_y = avg(top_ids) * h, avg(bottom_ids) * h
            left_x, right_x = lm[61].x * w, lm[291].x * w

            center = [int((left_x + right_x) / 2), int((top_y + bottom_y) / 2)]

            mouth_width = abs(right_x - left_x)
            mouth_ratio = (bottom_y - top_y) / mouth_width if mouth_width else 0
            mouth_open = mouth_ratio > 0.20

            # Draw points
            for pt in [(center[0], int(top_y)), (center[0], int(bottom_y)),
                    (int(left_x), center[1]), (int(right_x), center[1])]:
                cv2.circle(frame, pt, 4, (255, 0, 0), cv2.FILLED)

            cv2.circle(frame, center, 8, (0, 0, 255), cv2.FILLED)

            cv2.putText(
                frame,
                f"{mouth_ratio:.2f} ({'OPEN' if mouth_open else 'closed'})",
                (center[0] - 40, center[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0) if mouth_open else (0, 100, 255),
                1,
                cv2.LINE_AA,
            )

            obj_h, obj_w, _ = currentobj["img"].shape
            in_box = (position[0] <= center[0] <= position[0] + obj_w and
                    position[1] <= center[1] <= position[1] + obj_h)

            if in_box and mouth_open:
                self.score = self.score + 100 if currentobj["is_eatable"] else 0
                self.lost = not currentobj["is_eatable"]
                position[1] = self.hight + 1
                return self.score, self.lost

        return self.score, self.lost