from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
import pyrebase

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Patient(MDList):
    pass

class PatientList(Screen):
    def BuildButton(self):

        ScreenLayout = self.ids['PatientName']
        patientnames = []
        startdate = []
        enddate = []

        AllDoctorsPatients = db.child("patientUsers").get()
        for Patient in AllDoctorsPatients.each():
            patientnames.append(Patient.key())
            print(patientnames)

        for i in range(0,len(patientnames)):
            Icon = IconLeftWidget(icon="human")
            PatientID = patientnames[i]
            startdate.append(db.child("patientUsers").child(PatientID).child("start").get().val())
            start = startdate[i]
            enddate.append(db.child("patientUsers").child(PatientID).child("end").get().val())
            end = enddate[i]

            ListComponents = ThreeLineAvatarListItem(text = PatientID, secondary_text = "Start: " + start, tertiary_text = "End: " + end)

            ListComponents.add_widget(Icon)
            ScreenLayout.add_widget(ListComponents)
            i+=1