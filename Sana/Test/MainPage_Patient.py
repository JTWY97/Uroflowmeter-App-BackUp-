from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class WelcomePage(Screen):
	pass

class Doctor_LogIn(Screen):
	pass

class Patient_LogIn(Screen):
	pass

ScreenM = ScreenManager()

ScreenM.add_widget(WelcomePage(name='Welcome'))
ScreenM.add_widget(Doctor_LogIn(name='DoctorLogin'))
ScreenM.add_widget(Patient_LogIn(name='PatientLogin'))


class HomePagePatient(MDApp):
	# def build(self):
	# 	self.theme_cls.theme_style = "Dark"
	# 	self.theme_cls.primary_palette = "BlueGray"
	# 	return Builder.load_file('ScreenTest.kv')

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		screen = Builder.load_file('ScreenTest.kv')
		return screen

HomePagePatient().run()