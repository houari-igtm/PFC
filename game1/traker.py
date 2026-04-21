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

    def TrackFace(self, currentobj, position, frame, frame_RBG):
        result = self.face.process(frame_RBG)
        if not result.multi_face_landmarks:
            return self.score, False

        for face in result.multi_face_landmarks:
            self.mpDraw.draw_landmarks(
                frame,
                face,
                self.mpface.FACEMESH_LIPS,
                self.drawSpec,
                self.drawSpec
            )

            h, w, _ = frame.shape
            lm = face.landmark

            TOP_LIP    = [13, 312, 311, 310, 415, 308]
            BOTTOM_LIP = [14, 317, 402, 318, 324, 308]

            def avg_y(ids):
                return sum(lm[i].y for i in ids) / len(ids)

            top_y    = avg_y(TOP_LIP)    * h
            bottom_y = avg_y(BOTTOM_LIP) * h

            left_x  = lm[61].x * w
            right_x = lm[291].x * w
            mouth_width = abs(right_x - left_x)

            center_x = int((left_x + right_x) / 2)
            center_y = int((top_y + bottom_y) / 2)
            center   = [center_x, center_y]

            mouth_gap   = bottom_y - top_y
            mouth_ratio = mouth_gap / mouth_width if mouth_width > 0 else 0
            mouth_open  = mouth_ratio > 0.20

            for pt in [(center_x, int(top_y)), (center_x, int(bottom_y)),
                    (int(left_x), center_y), (int(right_x), center_y)]:
                cv2.circle(frame, pt, 4, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, center, 8, (0, 0, 255), cv2.FILLED)

            cv2.putText(frame, f"ratio:{mouth_ratio:.2f} ({'OPEN' if mouth_open else 'closed'})",
                        (center_x - 40, center_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0) if mouth_open else (0, 100, 255), 1, cv2.LINE_AA)

            obj_h, obj_w, _ = currentobj["img"].shape
            in_box = (position[0] <= center[0] <= position[0] + obj_w and
                    position[1] <= center[1] <= position[1] + obj_h)

            if in_box and mouth_open:
                if currentobj["is_eatable"]:
                    self.score += 1
                else:
                    self.score = 0
                return self.score, True

        return self.score, False