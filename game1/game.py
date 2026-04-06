import os
import random as ra
import cv2
import cvzone
from traker import Tracker

class Game:
    
    def __init__(self):
      
      self.width=1280
      self.hight=720
      self.speed=5
      self.score=0
      self.score_pos=[50,50]
      self.vid=cv2.VideoCapture(0)
      self.track= Tracker(self.width,self.hight)
      self.vid.set(3,self.width)
      self.vid.set(4,self.hight)
      self.type="face"
      
  
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
        return allfood[ra.randint(0,len(allfood)-1)],[ra.randint(half-120,half+120),2] 
        
    def AddToFrame(self,frame,currentobj,position):
         frame = cvzone.overlayPNG(frame, currentobj, position)
         h, w, _ = frame.shape
         bar_height = int(self.hight*0.15)
         cv2.rectangle(frame, (0, 0), (w, bar_height), (0, 0, 0), -1)
         font = cv2.FONT_HERSHEY_SIMPLEX
         
         y_text = int(bar_height *0.60)  # vertical alignment inside bar

        
         cv2.putText(frame, text=f"Score: {self.score}",
                    org=(int(w/2)-100, y_text),
                    fontFace=font,
                    fontScale=1.4,
                    color=(255, 255, 255),
                    thickness=3,
                    lineType=cv2.LINE_AA)

      
         cv2.putText(frame, text="Press K to Leave",
                    org=(w-260, y_text),
                    fontFace=font,
                    fontScale=0.8,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA)

         cv2.putText(frame, text="Press C to Switch",
                    org=(20, y_text),
                    fontFace=font,
                    fontScale=0.8,
                    color=(255, 255, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA)
            

    def Run(self):
        currentobj,position=self.ChoiseObject()

        while True:
         
         ret ,frame=self.vid.read()
         print(frame.shape)
         self.AddToFrame(frame,currentobj["img"],position)
         frame_RBG=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
       

         if self.type=="hand":
              self.score=self.track.TrackHands(currentobj,position,frame,frame_RBG)
         elif self.type=="face":
            self.score=self.track.TrackFace(currentobj,position,frame,frame_RBG)
     
         cv2.imshow("frame",frame)
        
         position[1]+=self.speed
         if position[1]>self.hight:
           currentobj,position=self.ChoiseObject()
           
         key = cv2.waitKey(1)

         if key == ord("c"):
              if self.type == "hand":
                  self.type = "face"
              else:
                  self.type = "hand"

         if key == ord("k"):
              self.vid.release() 
              cv2.destroyAllWindows()

    
  
if __name__=="__main__":
  game=Game()
  game.Run()