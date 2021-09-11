# from kivy.uix.screenmanager import Screen, SlideTransition

# class LogInDoctor(Screen):
#     def go_back(self):
#         self.parent.transition = SlideTransition(direction="right")
#         self.parent.current = self.parent.current = "WelcomeScreen"
#         self.parent.transition = SlideTransition(direction="left")

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class LogIn_Doctor(MDApp):

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('LogInScreen_Doctor.kv')
	
LogIn_Doctor().run()