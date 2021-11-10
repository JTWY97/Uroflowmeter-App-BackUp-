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
db = firebase.database() #connect to firebase

def listToString(s): 
    str1 = ""  
    for ele in s: 
        str1 += ele   
    return str1 

def doctorSignUp(firstname, lastname, specialization, hospital, phonenumber, email):
        SignUpData = {"firstname": firstname, "lastname": lastname, "specialization": specialization, "hospital": hospital, "phonenumber": phonenumber, "email": email}
        doctorName = "Dr " + lastname
        db.child("doctorUsers").child(doctorName).set(SignUpData)
        LogInData = {email[-4]: doctorName}
        db.child("DoctorLogInID").set(LogInData)
        

def patientSignUp(pfirstname, plastname, dob, weight, height, WakeUpTime, BedTime, treatmentstart, treatmentend, email):
        SignUpData = {"firstname": pfirstname, "lastname": plastname, "dob": dob, "weight": weight, "height": height, "start": treatmentstart, "end": treatmentend, "sleep": BedTime, "wakeup": WakeUpTime, "email":email}
        patientName = pfirstname + " " + plastname
        db.child("patientUsers").child(patientName).set(SignUpData)
        LogInData = {email[-4]: patientName}
        db.child("PatientLogInID").set(LogInData)

def SendVoidType(VoidTypes, patientID, dayID):
        db.child("patientData").child(patientID).child(dayID).set(VoidTypes)

VoidIndexFetched = []
WhichDay = []

def GetVoidDetails(VoidIndex, dayID):
    VoidIndexFetched.append(VoidIndex)
    if dayID == "day 1":
        WhichDay.append(1)
    elif dayID == "day 2":
        WhichDay.append(2)
    elif dayID == "day 3":
        WhichDay.append(3)
    return VoidIndexFetched, WhichDay