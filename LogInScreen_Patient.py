from kivy.uix.screenmanager import Screen, SlideTransition

class LogInPatient(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "WelcomeScreen"
        self.parent.transition = SlideTransition(direction="left")