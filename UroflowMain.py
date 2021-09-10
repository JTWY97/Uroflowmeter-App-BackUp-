from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

class MainPage(Screen):
    pass

class SymptomTracker(Screen):
    pass

class BladderDiary(Screen):
    pass

class FluidIntake(Screen):
    pass

#class MainApp(MDApp):
class HomePagePatient(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file("UroflowMain.kv")

#MainApp().run()
HomePagePatient().run()