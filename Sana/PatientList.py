from kivy.event import EventDispatcher
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
from kivy.uix.scrollview import ScrollView

import pyrebase
import json

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database() 

class PatientList(Screen, EventDispatcher):
    def GetPatients(self):
        all_users = db.child("patientUsers").get()
        patientnames = []
        for x in all_users.each():
            patientnames.append(x.key())
        return patientnames

    def build(self):
        screen = Screen()
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        patientnames = self.GetPatients()

        for i in range(0,len(patientnames)):
            icon = IconLeftWidget(icon="human")
            name = patientnames[i]
            
            startdate = []
            startdate.append(db.child("patientUsers").child(name).child("start").get().val())
            start = startdate[0]

            enddate = []
            enddate.append(db.child("patientUsers").child(name).child("end").get().val())
            end = enddate[0]

            items = ThreeLineAvatarListItem(
                text = name,
                secondary_text = "Start: " + start,
                tertiary_text = "End: " + end
                )
            items.add_widget(icon)
            list_view.add_widget(items)
            i+=1

        screen.add_widget(scroll)