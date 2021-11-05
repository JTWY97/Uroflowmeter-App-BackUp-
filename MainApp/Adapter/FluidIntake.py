from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
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

	dayID = "day 1"

	volume_day1 = []
	volume_day2 = []
	volume_day3 = []

	def GetDay(self, button):
		if button == 'DayOne':
			self.dayID = "day 1"
			self.FluidDrankLabel()
			self.ids.volumeop.text = "Volume here!"
		elif button == 'DayTwo':
			self.dayID = "day 2"
			self.FluidDrankLabel()
			self.ids.volumeop.text = "Volume here!"
		elif button == 'DayThree':
			self.dayID = "day 3"
			self.FluidDrankLabel()
			self.ids.volumeop.text = "Volume here!"

	def FluidDrankLabel(self):
		Volume = db.child("patientData").child(self.PatientID).child(self.dayID).child("total fluid intake").get()
		VolumeDrank = Volume.val()
		if VolumeDrank != None:
			self.ids.VolumeDrankOnThisDay.text = str(int(VolumeDrank)) + " ml"
			if self.dayID == "day 1":
				self.volume_day1.append(int(VolumeDrank))
			elif self.dayID == "day 2":
				self.volume_day2.append(int(VolumeDrank))
			elif self.dayID == "day 3":
				self.volume_day3.append(int(VolumeDrank))
		else:
			self.ids.VolumeDrankOnThisDay.text = "You have not logged any fluid intake"
		
	
	def callback(self, button):
		if button == 'button1':
			value = 250
			if self.dayID == "day 1":
				self.volume_day1.append(value)
				self.showvol("day 1")
				return self.volume_day1
			elif self.dayID == "day 2":
				self.volume_day2.append(value)
				self.showvol("day 2")
				return self.volume_day2
			elif self.dayID == "day 3":
				self.volume_day3.append(value)
				self.showvol("day 3")
				return self.volume_day3

		elif button == 'button2':
			value = 500
			if self.dayID == "day 1":
				self.volume_day1.append(value)
				self.showvol("day 1")
				return self.volume_day1
			elif self.dayID == "day 2":
				self.volume_day2.append(value)
				self.showvol("day 2")
				return self.volume_day2
			elif self.dayID == "day 3":
				self.volume_day3.append(value)
				self.showvol("day 3")
				return self.volume_day3

		elif button == 'button3':
			value = 1000
			if self.dayID == "day 1":
				self.volume_day1.append(value)
				self.showvol("day 1")
				return self.volume_day1
			elif self.dayID == "day 2":
				self.volume_day2.append(value)
				self.showvol("day 2")
				return self.volume_day2
			elif self.dayID == "day 3":
				self.volume_day3.append(value)
				self.showvol("day 3")
				return self.volume_day3

		elif button == 'button4':
			if self.dayID == "day 1":
				self.volume_day1 = self.volume_day1[:-1]
				self.showvol("day 1")
				return self.volume_day1
			elif self.dayID == "day 2":
				self.volume_day2 = self.volume_day2[:-1]
				self.showvol("day 2")
				return self.volume_day2
			elif self.dayID == "day 3":
				self.volume_day3 = self.volume_day3[:-1]
				self.showvol("day 3")
				return self.volume_day3

	def CustomVolume(self, CustomVol):
		if self.dayID == "day 1":
			self.volume_day1.append(int(CustomVol))
			self.ids.CustomVol.text = ""
			self.showvol("day 1")
			return self.volume_day1
		elif self.dayID == "day 2":
			self.volume_day2.append(int(CustomVol))
			self.ids.CustomVol.text = ""
			self.showvol("day 2")
			return self.volume_day2
		elif self.dayID == "day 3":
			self.volume_day3.append(int(CustomVol))
			self.ids.CustomVol.text = ""
			self.showvol("day 3")
			return self.volume_day3

	def showvol(self, day):
		if day == "day 1":
			meanvol = np.sum(self.volume_day1)
			self.ids.volumeop.text = str(int(meanvol))
			data = {"total fluid intake": str(int(meanvol))}
		elif day == "day 2":
			meanvol = np.sum(self.volume_day2)
			self.ids.volumeop.text = str(int(meanvol))
			data = {"total fluid intake": str(int(meanvol))}
		elif day == "day 3":
			meanvol = np.sum(self.volume_day3)
			self.ids.volumeop.text = str(int(meanvol))
			data = {"total fluid intake": str(int(meanvol))}

		db.child("patientData").child(self.PatientID).child(self.dayID).update(data)
		self.FluidDrankLabel()

        