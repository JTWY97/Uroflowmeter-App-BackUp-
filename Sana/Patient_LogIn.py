from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager, SlideTransition

class Patient_LogIn(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "welcome_screen"
        self.parent.transition = SlideTransition(direction="left")