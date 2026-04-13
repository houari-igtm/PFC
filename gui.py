from tkinter import *
from tkinter import ttk
from game1.game import Game as Game1
from game2.game2 import Game as Game2
class Gui:
    def __init__(self):
        self.app = Tk()
        
        # إعدادات النافذة الرئيسية
        self.app.title("🎮 Camera Eating Game")
        self.app.geometry("1280x720") # تم تقليل الارتفاع ليتناسب مع غياب المعاينة
        self.app.configure(bg="#2C3E50")
        self.app.resizable(False, False)

        # الإطار الرئيسي
        self.main_frame = Frame(self.app, bg="#2C3E50")
        self.main_frame.pack(expand=True, fill=BOTH, padx=50, pady=50)

        # إنشاء المكونات
        self.create_header()
        self.create_game_modes()
        self.create_footer()

        self.app.mainloop()

    def create_header(self):
        """إنشاء رأس الصفحة المطور"""
        title_frame = Frame(self.main_frame, bg="#2C3E50")
        title_frame.pack(fill=X, pady=(0, 40))

        # العنوان الرئيسي
        Label(
            title_frame,
            text="🎮 CAMERA EATING GAME",
            font=("Segoe UI", 36, "bold"),
            fg="#F1C40F",
            bg="#2C3E50"
        ).pack()

        # خط فاصل أنيق
        separator = Frame(title_frame, height=2, bg="#34495E")
        separator.pack(fill=X, pady=15)

        # وصف اللعبة
        Label(
            title_frame,
            text="تحدَّ نفسك! استخدم حركات وجهك أو يدك للعب",
            font=("Tahoma", 14),
            fg="#ECF0F1",
            bg="#2C3E50"
        ).pack()

    def create_game_modes(self):
        """إنشاء منطقة اختيار أوضاع اللعب بشكل مركزي"""
        modes_frame = Frame(self.main_frame, bg="#2C3E50")
        modes_frame.pack(expand=True)

        Label(
            modes_frame,
            text="Choose your game",
            font=("Tahoma", 16, "bold"),
            fg="#3498DB",
            bg="#2C3E50"
        ).pack(pady=(0, 30))

        buttons_container = Frame(modes_frame, bg="#2C3E50")
        buttons_container.pack()

        # إعدادات الأزرار المشتركة
        btn_style = {
            "font": ("Tahoma", 14, "bold"),
            "width": 18,
            "height": 2,
            "fg": "white",
            "relief": FLAT,
            "cursor": "hand2",
            "bd": 0
        }

        # زر وضع الوجه
        self.face_btn = Button(
            buttons_container,
            text="🎮 Game 1",
            bg="#2980B9",
            activebackground="#3498DB",
            command=self.start_game1,
            **btn_style
        )
        self.face_btn.pack(side=LEFT, padx=15)

        # زر وضع اليد
        self.hand_btn = Button(
            buttons_container,
            text="🎮 Game 2",
            bg="#C0392B",
            activebackground="#E74C3C",
            command=self.start_game2,
            **btn_style
        )
        self.hand_btn.pack(side=LEFT, padx=15)

    def create_footer(self):
        """تذييل الصفحة"""
        footer = Frame(self.app, bg="#34495E", height=60)
        footer.pack(side=BOTTOM, fill=X)

        Label(
            footer,
            text="💡 تعليمات: تأكد من وجود إضاءة جيدة أمام الكاميرا عند بدء اللعب",
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
