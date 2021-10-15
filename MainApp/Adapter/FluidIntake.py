from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
from kivymd.uix.textfield import MDTextField
import numpy as np
import pyrebase

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class FluidIntake(Screen, EventDispatcher):

	Patient_Variables = "./Context/Variables_Patient.txt"
	with open(Patient_Variables, "r") as f:
		PatientID = f.read()

	volume = []
	def callback(self, button):
		if button == 'button1':
			value = 250
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button2':
			value = 500
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button3':
			value = 1000
			self.volume.append(value)
			self.showvol()
			return self.volume

		elif button == 'button4':
			self.volume = self.volume[:-1]
			self.showvol()
			return self.volume

	#def button(self,button):
		#CustomField = MDTextField(text='Enter Fluid in ml',
		#pos_hint = {'center_x': 0.5, 'center_y': 0.5}, 
		#size_hint_x=None,width=300)
	
	def showvol(self):
		print(self.volume)
		meanvol = np.sum(self.volume)
		self.ids.volumeop.text = str(int(meanvol))
 		
		data = {"total fluid intake": str(int(meanvol))}
		db.child("patientUsers").child(self.PatientID).update(data)

        