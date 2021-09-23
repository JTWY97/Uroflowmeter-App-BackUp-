from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.picker import MDDatePicker
import numpy as np

#Connect to firebase 
import pyrebase
import json
  
config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com",
  ##"serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


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
	date = []
	def on_save(self, instance, value, date_range):
		self.date.append(str(value))
		self.root.ids.date_label.text = str(self.date[-1])

	print(date)


#Click Cancel
	def on_cancel(self, instance, value):
		self.root.ids.date_label.text = "You Clicked Cancel"

	def show_date_picker(self):
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
		date_dialog.open()



	volume = []
	def callback(self,button):
		if button == 'button1':
			value = 70
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button2':
			value = 90
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button3':
			value = 100
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button4':
			self.volume = self.volume[:-1]
			self.showvol()
			return self.volume

	
	def showvol(self):
		print(self.volume)
		meanvol = np.sum(self.volume)
		self.root.ids.volumeop.text = str(int(meanvol))
		
		data = {"total fluid intake": str(int(meanvol))}
		db.child("patientUsers").child("jane doe").update(data) #to update to a dynamic variable

#MainApp().run()
HomePagePatient().run()