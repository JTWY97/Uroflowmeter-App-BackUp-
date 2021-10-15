from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.picker import MDDatePicker
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

class SymptomTracker(Screen):

    Patient_Variables = "./Context/Variables_Patient.txt"
    with open(Patient_Variables, "r") as f:
        PatientID = f.read()


    date = []
    SymptomList = []
    def on_save(self, instance, Symptom, date_range):
        self.date.append(str(Symptom))
        self.ids.date_label.text = str(self.date[-1])
        
    def on_cancel(self, instance, Symptom):
        self.ids.date_label.text = "You Clicked Cancel"
    
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def SendSymptom(self, button):
        if button == 'button1':
            Symptom = "Fatigue"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList
            
        elif button == 'button2':
            Symptom = "Leg Swelling"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList
            
        elif button == 'button3':
            Symptom = "Fever"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList
            
        elif button == 'button4':
            Symptom = "Nausea and/or vomiting"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button5':
            Symptom = "Headache"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button6':
            Symptom = "Leaks"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList
            
    def SendSymptomToFirebase(self):
        Label = "Symptoms Experienced" + str(self.date)
        data = {Label: self.SymptomList}
        db.child("patientData").child(self.PatientID).update(data)