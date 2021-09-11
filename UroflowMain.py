from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.picker import MDDatePicker

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

    #Click OK
    def on_save(self,instance,value,date_range):
        print(instance,value,date_range)

    #Click Cancel
    def on_cancel(self,instance,value):
        self.root.ids.date_label.text = "You Clicked Cancel"
    
	def show_date_picker(self):
		date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
		date_dialog.open()

	def got_date(self, the_date):
		print(the_date)

#MainApp().run()
HomePagePatient().run()