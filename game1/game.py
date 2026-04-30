import os
import random as ra
import cv2
import cvzone
from game1.traker import Tracker
from base.base_games import Base

class Game(Base):
    
    def __init__(self):
      super().__init__()
      self.score_pos=[50,50]
      self.vid=cv2.VideoCapture(0)
      self.track= Tracker(self.width,self.hight)   
      self.vid.set(3,self.width)
      self.vid.set(4,self.hight)
      self.type="face"
      self.lost=False
      
  
    def Load_eatable(self):
        eatables=[]
        folderEatable='images/eatable'
        listeEatable=os.listdir(folderEatable)
        for obj in listeEatable:
         eatables.append({
            "img":cv2.imread(f'{folderEatable}/{obj}',cv2.IMREAD_UNCHANGED),
            "is_eatable":True
          })
        return eatables
        
    def Load_NoNEatable(self):
        NonEatable=[]
        foldeNONEatable='images/non_eatable'
        listeNONEatable=os.listdir(foldeNONEatable)
        for obj in listeNONEatable:
         NonEatable.append({
            "img":cv2.imread(f'{foldeNONEatable}/{obj}',cv2.IMREAD_UNCHANGED),
            "is_eatable":False
          })
        return NonEatable
    

    def ChoiseObject(self): 
        allfood=[]
        allfood=self.Load_eatable()+self.Load_NoNEatable()
        half=self.width/2
        # Use proportional offset (20% of width) instead of hardcoded 120
        offset = int(self.width * 0.1)
        return allfood[ra.randint(0,len(allfood)-1)],[ra.randint(int(half-offset),int(half+offset)),2] 
        
    def AddToFrame(self,frame,currentobj,position):
         frame = cvzone.overlayPNG(frame, currentobj, position)
         h, w, _ = frame.shape
         bar_height = int(h*0.15)
         cv2.rectangle(frame, (0, 0), (w, bar_height), (0, 0, 0), -1)
         font = cv2.FONT_HERSHEY_SIMPLEX
         
         y_text = int(bar_height *0.60)
         score_offset = int(w * 0.08)  # 8% of width
         button_offset = int(w * 0.2)  # 20% of width
        
         cv2.putText(frame, text=f"Score: {self.score}",
                    org=(int(w/2)-score_offset, y_text),
                    fontFace=font,
                    fontScale=1.4,
                    color=(255, 255, 255),
                    thickness=3,
                    lineType=cv2.LINE_AA)

      
         cv2.putText(frame, text="Press K to Leave",
                    org=(w-button_offset, y_text),
                    fontFace=font,
                    fontScale=0.8,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA)

         cv2.putText(frame, text="Press C to Switch",
                    org=(int(w*0.02), y_text),
                    fontFace=font,
                    fontScale=0.8,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA)
            

    def Run(self):
        currentobj,position=self.ChoiseObject()

        while True:
         ret ,frame=self.vid.read()
         frame = cv2.flip(frame, 1)
         if self.lost==False:
          self.AddToFrame(frame,currentobj["img"],position)
          frame_RBG=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        

          if self.type=="hand":
                self.score,self.lost=self.track.TrackHands(currentobj,position,frame,frame_RBG)
          elif self.type == "face":
              self.score, self.lost = self.track.TrackFace(currentobj, position, frame, frame_RBG)
              if  position[1] > self.hight:   
                  currentobj, position = self.ChoiseObject()

          cv2.imshow("frame",frame)
          
          position[1]+=self.speed
          if position[1]>self.hight:
            currentobj,position=self.ChoiseObject()
         else:
             
             
             x = 365
             y = self.hight - 100
             cv2.putText(frame, "Game Over Press R to Restart", (x, y), cv2.FONT_HERSHEY_SIMPLEX,2, (0, 0, 255), 3)
             cv2.imshow("frame", frame)
             
         
         key = cv2.waitKey(1)

         if key == ord("c"):
              if self.type == "hand":
                  self.type = "face"
              else:
                  self.type = "hand"
         if key == ord("r") and self.lost:
              self.lost = False
              self.score = 0
              currentobj, position = self.ChoiseObject()
         if key == ord("k"):
              self.vid.release() 
              cv2.destroyAllWindows()

    
  
if __name__=="__main__":
  game=Game()
  game.Run()