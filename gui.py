from tkinter import *
from tkinter import ttk
from game1.game import Game as Game1
from game2.game2 import Game as Game2
class Gui:
    def __init__(self):
        self.app = Tk()
        
        
        self.app.title("🎮 Camera Eating Game")
        self.app.geometry("1280x720") 
        self.app.configure(bg="#2C3E50")
        self.app.resizable(False, False)

        
        self.main_frame = Frame(self.app, bg="#2C3E50")
        self.main_frame.pack(expand=True, fill=BOTH, padx=50, pady=50)

       
        self.create_header()
        self.create_game_modes()
        self.create_footer()

        self.app.mainloop()

    def create_header(self):
        
        title_frame = Frame(self.main_frame, bg="#2C3E50")
        title_frame.pack(fill=X, pady=(0, 25))

        
        Label(
            title_frame,
            text="🎮 CAMERA EATING GAME",
            font=("Segoe UI", 36, "bold"),
            fg="#F1C40F",
            bg="#2C3E50"
        ).pack()

      
        separator = Frame(title_frame, height=2, bg="#34495E")
        separator.pack(fill=X, pady=15)

      
        Label(
            title_frame,
            text="Challenge yourself! Use your facial or hand movements to play",
            font=("Tahoma", 14),
            fg="#ECF0F1",
            bg="#2C3E50"
        ).pack()
      
        Label(
            title_frame,
            text="Choose your game",
            font=("Tahoma", 16, "bold"),
            fg="#3498DB",
            bg="#2C3E50"
        ).pack(pady=(15, 10))

       
        buttons_container = Frame(title_frame, bg="#2C3E50")
        buttons_container.pack(pady=(80, 0))

        btn_style = {
            "font": ("Tahoma", 14, "bold"),
            "width": 18,
            "height": 2,
            "fg": "white",
            "relief": FLAT,
            "cursor": "hand2",
            "bd": 0
        }

       
        self.face_btn = Button(
            buttons_container,
            text="🎮 Game 1",
            bg="#2980B9",
            activebackground="#3498DB",
            command=self.start_game1,
            **btn_style
        )
        self.face_btn.pack(side=LEFT, padx=15)

      
        self.hand_btn = Button(
            buttons_container,
            text="🎮 Game 2",
            bg="#E74C3C",
            activebackground="#E55545",
            command=self.start_game2,
            **btn_style
        )
        self.hand_btn.pack(side=LEFT, padx=15)

        # Quit button container (below Game buttons, centered)
        quit_container = Frame(title_frame, bg="#2C3E50")
        quit_container.pack(pady=(10, 0))

       
        quit_btn_style = {
            "font": ("Tahoma", 14, "bold"),
            "width": 18,
            "height": 2,
            "fg": "white",
            "relief": FLAT,
            "cursor": "hand2",
            "bd": 0
        }
        self.quit_btn = Button(
            quit_container,
            text="❌ Quit",
            bg="#C0392B",
            activebackground="#B83D30",
            command=self.app.quit,
            **quit_btn_style
        )
        self.quit_btn.pack(pady=40)

    def create_game_modes(self):
      
        modes_frame = Frame(self.main_frame, bg="#2C3E50")
        modes_frame.pack(expand=True)

    def create_footer(self):
        
        footer = Frame(self.app, bg="#34495E", height=60)
        footer.pack(side=BOTTOM, fill=X)

        Label(
            footer,
            text="💡 Instructions: Make sure there is good lighting in front of the camera when you start playing.",
            font=("Tahoma", 10),
            fg="#BDC3C7",
            bg="#34495E"
        ).pack(pady=10)

    def start_game1(self):
        try:
            game = Game1()
            game.Run()
        except Exception as e:
            print(f"Error starting Game 1: {e}")

    def start_game2(self):
        try:
            game = Game2()
            game.Run()
        except Exception as e:
            print(f"Error starting Game 2: {e}")
       
if __name__== "__main__":
   gui=Gui()
