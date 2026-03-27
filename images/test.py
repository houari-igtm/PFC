import os
import random as ra
import cv2
import cvzone
from shapes import Shape

class Game:
    
    width=1250
    hight=700
    speed=5
    score=0
    score_pos=[50,50]
    vid=cv2.VideoCapture(0)
    shape= Shape(width,hight)

    def __init__(self):
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
        return allfood[ra.randint(0,len(allfood)-1)],[ra.randint(100,self.width-100),2] 
        
    def AddToFrame(self,frame,currentobj,position):
         frame=cvzone.overlayPNG(frame,currentobj,position)
         cv2.putText(frame,text=f"Score: {self.score}",org=self.score_pos,fontFace=cv2.FONT_HERSHEY_SIMPLEX,
         fontScale=1.25,
         color=(255, 0, 0), 
         thickness=2,
         lineType=cv2.LINE_AA
         )
         cv2.putText(frame,text="Press K to Leave",org=(50,100),fontFace=cv2.FONT_HERSHEY_SIMPLEX,
         fontScale=1.5,
          color=(255, 0, 0), 
         thickness=2,
         lineType=cv2.LINE_AA
         )

   
    def Run(self):
        currentobj,position=self.ChoiseObject()

        while True:
         
         ret ,frame=self.vid.read()
         self.AddToFrame(frame,currentobj["img"],position)
         frame_RBG=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

         if self.type.lower()=="hand":
           self.score=self.shape.TrackHands(currentobj,position,frame,frame_RBG)
         elif self.type.lower()=="face":
          self.score=self.shape.TrackFace(currentobj,position,frame,frame_RBG)

         cv2.imshow("frame",frame)
   
         position[1]+=self.speed
         if position[1]>self.hight:
           currentobj,position=self.ChoiseObject()
           
  
         if cv2.waitKey(1)==ord("k"):
           self.vid.release()
           cv2.destroyAllWindows()
  
if __name__=="__main__":
  game=Game()
  game.Run()