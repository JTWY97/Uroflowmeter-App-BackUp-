from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.picker import MDDatePicker
<<<<<<< HEAD
<<<<<<< HEAD
import pyrebase
import os
  
config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

path = os.getcwd()
path = path + "/Sana/"
=======
>>>>>>> parent of 6c92e76 (fixed main app)
=======
>>>>>>> parent of 6c92e76 (fixed main app)

class SymptomTracker(Screen):
    date = []
    def on_save(self, instance, value, date_range):
        self.date.append(str(value))
        self.ids.date_label.text = str(self.date[-1])
        
    def on_cancel(self, instance, value):
        self.ids.date_label.text = "You Clicked Cancel"
    
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()