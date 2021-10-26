from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import Screen
import pyrebase
import numpy as np


config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class BladderDiary(Screen):
    Patient_Variables = "./Context/Variables_Patient.txt"
    with open(Patient_Variables, "r") as f:
        PatientID = f.read()

    def GetData_Volume(self):
        Volume = db.child("patientData").child(self.PatientID).child("day 1").child("volume").get()
        PatientUroflowData_Volume = Volume.val()
        VoidVolume = PatientUroflowData_Volume.split(',')
        return VoidVolume

    def GetData_Time(self):
        VoidTimeList = []
        PatientUroflowData_Time = db.child("patientData").child(self.PatientID).child("day 1").child("time").get()
        PatientUroflowData_Time = PatientUroflowData_Time.val()
        VoidTimeArray = PatientUroflowData_Time.split(',')
        VoidTimeArray = np.array(VoidTimeArray).astype(np.float)
        print(VoidTimeArray)
        for i in range(0, len(VoidTimeArray)):
            VoidTime = self.GetTime_Text(VoidTimeArray[i])
            VoidTimeList.append(VoidTime)
        return VoidTimeList

    def GetTime_Text(self,VoidTimeArray):
        TimeOfLastVoid = VoidTimeArray
        b = 10
        n = np.ceil(np.max(np.log(TimeOfLastVoid) / np.log(b))).astype(int)
        d = np.arange(n)
        d.shape = d.shape + (1,) * (TimeOfLastVoid.ndim)
        out = TimeOfLastVoid // b ** d % b
        VoidTime = str(int(out[3])) + str(int(out[2])) + ":" + str(int(out[1]))+ str(int(out[0]))
        return VoidTime

    def GetData_VoidType(self):
        print("PatientID:" + self.PatientID)
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child("day 1").child("episode").get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        VoidType = PatientUroflowData_VoidType.split(',')
        return VoidType

    def ShowSummary(self):
        ScreenLayout = self.ids['BladderSummary']
        
        VoidType = self.GetData_VoidType()
        VoidVolume = self.GetData_Volume()
        TotalVoidVolume = []
        
        NumberofVoids = (len(VoidType))

        for i in range(0, len(VoidType)):
            TotalVoidVolume.append(float(VoidVolume[i]))

        TotalVoid = np.sum(TotalVoidVolume)

        NumberOfVoids_Entry = OneLineAvatarListItem(text = "Total Number of Voids Logged Today: " + str(NumberofVoids))
        TotalVoidVolume_Entry = OneLineAvatarListItem(text = "Total Volume Voided Today: " + str(TotalVoid))
        BackButton = MDRaisedButton(text="Back")
        MoreButton = MDRaisedButton(text="Show Detailed Timeline")

        ScreenLayout.add_widget(MoreButton)
        ScreenLayout.add_widget(NumberOfVoids_Entry)
        ScreenLayout.add_widget(TotalVoidVolume_Entry)
        ScreenLayout.add_widget(BackButton)