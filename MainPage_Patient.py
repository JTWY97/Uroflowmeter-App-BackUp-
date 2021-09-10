from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class WelcomePage(Screen):
	pass

class DoctorLogin(Screen):
	pass

class PatientLogin(Screen):
	pass

ScreenM = ScreenManager()

ScreenM.add_widget(WelcomePage(name='Welcome'))
ScreenM.add_widget(DoctorLogin(name='DoctorLogin'))
ScreenM.add_widget(PatientLogin(name='PatientLogin'))


class HomePagePatient(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('ScreenTest.kv')

HomePagePatient().run()