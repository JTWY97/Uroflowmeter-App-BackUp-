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

class BladderDiary(Screen, EventDispatcher):
  	# def build(self):
		# self.theme_cls.theme_style = "Dark"
		# self.theme_cls.primary_palette = "BlueGray"
		# return Builder.load_file("BladderDiary.kv")

    def showtotalvol(self):
        snapshot = db.child("patientData").child("patient1").child("day 1").child("volume").get()
        snapshotvalue = snapshot.val()
        arr = snapshotvalue.split(',')
        # arr1 = [i if i[0] is not None else (0, i[1]) for i in arr]
        an_array = np.array(arr).astype(np.float)
        # print(an_array)
        # index = [0]
        # volume = np.array(lst)
        volume = np.sum(an_array)
        print(volume)
