#this code shld be in all the py files which will communicate with firebase
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

VoidIndexFetched = []
WhichDay = []

def patientSignUp(email, pfirstname, plastname, dob, weight, height, WakeUpTime, BedTime, treatmentstart, treatmentend, RaspberryID, ButtonID):
        SignUpData = {"firstname": pfirstname, "lastname": plastname, "dob": dob, "weight": weight, "height": height, "start": treatmentstart, "end": treatmentend, "sleep": BedTime, "wakeup": WakeUpTime, "raspberrypi":RaspberryID, "button":ButtonID}
        patientName = pfirstname + " " + plastname
        print(SignUpData)
        db.child("patientUsers").child(patientName).set(SignUpData)
        LogInData = {email[:-4]: patientName}
        db.child("PatientLogInID").update(LogInData)

def SendVoidType(VoidTypes, patientID, dayID):
        db.child("patientData").child(patientID).child(dayID).set(VoidTypes)

def GetVoidDetails(VoidIndex, dayID):
    VoidIndexFetched.append(VoidIndex)
    if dayID == "day 1":
        WhichDay.append(1)
    elif dayID == "day 2":
        WhichDay.append(2)
    elif dayID == "day 3":
        WhichDay.append(3)
    return VoidIndexFetched, WhichDay