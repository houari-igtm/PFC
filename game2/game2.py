import os
import random as ra
import cv2
import cvzone
from .traker2 import Tracker
import time

class Game:
    
    def __init__(self):
      
      self.width=1280
      self.hight=720
      self.speed=5
      self.score=0
      self.middle_width=int(self.width/2)
      self.middle_height=int(self.hight/2)
      self.score_pos=[50,50]
      self.vid=cv2.VideoCapture(0)
      self.track= Tracker(self.width,self.hight)
      self.vid.set(3,self.width)
      self.vid.set(4,self.hight)
      self.waiting = False
      self.wait_st = 0
      
  
    def Load_eatable(self):
        eatables=[]
        folderEatable='images/eatable'
        listeEatable=os.listdir(folderEatable)
        for obj in listeEatable:
         eatables.append({
            "img":cv2.imread(f'{folderEatable}/{obj}',cv2.IMREAD_UNCHANGED),
            "is_eatable":True,
            "name":obj.split(".")[0]
          })
        return eatables
        
    def Load_NoNEatable(self):
        NonEatable=[]
        foldeNONEatable='images/non_eatable'
        listeNONEatable=os.listdir(foldeNONEatable)
        for obj in listeNONEatable:
         NonEatable.append({
            "img":cv2.imread(f'{foldeNONEatable}/{obj}',cv2.IMREAD_UNCHANGED),
            "is_eatable":False,
            "name":obj.split(".")[0]
          })
        return NonEatable
    

    def ChoiseObject(self): 
        allfood=[]
        positions=[]
        offset=0
        allfood=self.Load_eatable()+self.Load_NoNEatable()
        ra.shuffle(allfood)
        selected_obj=allfood[0:3]
        Name=ra.choice(selected_obj)["name"]
        for i in range(3):
          x = self.middle_width - 250 +offset
          y = self.middle_height
          positions.append([x, y])
          offset+=250
        return allfood[0:3], positions, Name
          
        
    def AddToFrame(self,frame,currentobj,position,Name):
         
         frame = cvzone.overlayPNG(frame, currentobj, position)
         h, w, _ = frame.shape
         bar_height = int(self.hight*0.15)
         cv2.rectangle(frame, (0, 0), (w, bar_height), (0, 0, 0), -1)
         font = cv2.FONT_HERSHEY_SIMPLEX
         
         y_text = int(bar_height *0.60) 

        
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

         
         
         cv2.putText(frame,text=f"Click : {Name}",org=(self.middle_width-150,self.middle_height-180),fontFace=cv2.FONT_HERSHEY_SIMPLEX,
         fontScale=2,
          color=(0, 0, 0), 
         thickness=2,
         lineType=cv2.LINE_AA
         )
   
   
   
        

    def Run(self):
        currentobj,positions,Name=self.ChoiseObject()

        while True:
         
         ret ,frame=self.vid.read()
         for i, obj in enumerate(currentobj):
                self.AddToFrame(frame,obj["img"],positions[i],Name)   
       
         frame_RBG=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
         

         if  not self.waiting:
                self.score, status,result = self.track.TrackHands(currentobj, positions, frame, frame_RBG, Name)
         else:
             status = ""

         if status == "change" and not self.waiting:
                  self.waiting = True
                  self.wait_st = time.time()

         if self.waiting:
                  cv2.putText(frame,f"{result} - WAIT...",(500, self.hight-100),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                  if time.time() - self.wait_st > 2:
                      currentobj, positions, Name = self.ChoiseObject()
                      self.waiting = False
                  
         
         cv2.imshow("frame",frame)
         key = cv2.waitKey(1)

       
         if key == ord("k"):
                self.vid.release() 
                cv2.destroyAllWindows()

    
  
if __name__=="__main__":
  game=Game()
  game.Run()