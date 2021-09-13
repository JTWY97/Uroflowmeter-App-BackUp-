# 11 Pages --
# --> Patient: Log In Page, Main Page, Sypmtoms Tracker, Bladder Diary, Fluid Intake, Quick Pee
# --> Doctor: Log In Page (Repeated), Doctor Sign Up Page, Main Page, Patient List, Patient Data Summary, Patient Sign Up Page

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class MainApp(MDApp):

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('login.kv')

	def logger(self):
		self.root.ids.WelcomeLabel.text = f'Sup {self.root.ids.User.text}!' #id: welcome_id

	def clear(self):
		self.root.ids.WelcomeLabel.text = "WELCOME"		
		self.root.ids.User.text = ""
		self.root.ids.Password.text = ""
	
MainApp().run()