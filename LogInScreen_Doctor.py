from kivy.uix.screenmanager import Screen, SlideTransition

class LogInDoctor(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "WelcomeScreen"
        self.parent.transition = SlideTransition(direction="left")