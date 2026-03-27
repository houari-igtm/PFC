from tkinter import Tk
from tkinter import *
from game import Game


class Gui:

    app=Tk()
    game=Game()

    def __init__(self):
    
        self.app.title("PFC")
        self.app.geometry("800x600")
        self.app.configure(bg="gold")
        title=Label(self.app,text="welcome to our game",font=("jersey 25", 50, "bold"),pady="50",fg="#1C3F81",bg="gold" )
        title.pack()
        self.buttons()
        self.app.mainloop()

    def buttons(self):
        btn1 = Button(self.app, text="face",font=("jersey 25", 18, "bold") ,width=20,
            height=2,
            padx=10,
            pady=5,
            bd=0,
            bg="#1C3F81",
            fg="gold",
            command=self.face)
        btn1.pack()


        btn2 = Button(self.app, text="hands",font=("jersey 25", 18, "bold"),   width=20,
            height=2,
            padx=10,
            pady=5,
            bd=0,
            bg="#1C3F81",
            fg="gold",
            command=self.hands)
        btn2.pack(pady=40) 


    def hands(self):
        self.game.type="hand"
        self.game.Run()
        self.Quit()
        
    def face(self):
        self.game.type="face"
        self.game.Run()
        self.Quit()

if __name__=="__main__":
        gui=Gui()