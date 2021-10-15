from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
import pyrebase
import numpy as np
import os

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()



class DiaryEntry(MDList):
    pass

class BladderDiarySummary(Screen):
    path = os.getcwd()
    path = path + "/Sana/"
    
    Patient_Variables = path + "Context/Variables_Patient.txt"
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
        for i in range(0, len(VoidTimeArray)):
            VoidTime = self.GetTime_Text(VoidTimeArray[i])
            VoidTimeList.append(VoidTime)
        return VoidTimeList

    def GetTime_Text(self,VoidTimeArray):
        VoidTime = str(int(VoidTimeArray[0])) + str(int(VoidTimeArray[1])) + ":" + str(int(VoidTimeArray[2]))+ str(int(VoidTimeArray[3]))
        return VoidTime

    def GetData_VoidType(self):
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child("day 1").child("episode").get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        VoidType = PatientUroflowData_VoidType.split(',')
        return VoidType

    def BuildTimeline(self):
        ScreenLayout = self.ids['BladderDiaryWidgets']
        VoidType = self.GetData_VoidType()
        VoidTime = self.GetData_Time()
        VoidVolume = self.GetData_Volume()

        for i in range(0,len(VoidType)):
            if VoidType[-i] == "First Morning Episode":
                Icon = IconLeftWidget(icon="BladderDiaryIcons/Morning.png")
            elif VoidType[-i] == "Normal Episode":
                Icon = IconLeftWidget(icon="BladderDiaryIcons/Normal.png")
            elif VoidType[-i] == "Nocturia Episode":
                Icon = IconLeftWidget(icon="BladderDiaryIcons/Nocturia.png")
            else:
                Icon = IconLeftWidget(icon="human")

            ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[-i]), secondary_text = "Void Type: " + VoidType[-i], tertiary_text = "Void Volume: " + VoidVolume[-i]+ "ml")

            ListComponents.add_widget(Icon)
            ScreenLayout.add_widget(ListComponents)
            i+=1