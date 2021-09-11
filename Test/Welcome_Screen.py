from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class WelcomeScreen(MDApp):

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('Welcome_Screen.kv')
	
WelcomeScreen().run()

# from kivy.uix.screenmanager import Screen

# class WelcomeScreen(Screen):
#     pass