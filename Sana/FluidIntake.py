from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
import numpy as np
import pyrebase

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com",
  ##"serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class FluidIntake(Screen, EventDispatcher):
	volume = []
	def callback(self, button):
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
		self.parent.ids.volumeop.text = str(int(meanvol))
 		
		data = {"total fluid intake": str(int(meanvol))}
		db.child("patientUsers").child("jane doe").update(data)

        