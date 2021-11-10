from kivy.event import EventDispatcher
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.label import Label
from  kivy.uix.popup import Popup
from numpy.lib.npyio import NpzFile
import pyrebase
import numpy as np
from kivy.uix.floatlayout import FloatLayout
import datetime
import matplotlib.pyplot as plt

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

import os

class PatientReportGenerator():

    Patient_Variables = "./Context/Variables_Patient.txt"
    with open(Patient_Variables, "r") as f:
        PatientID = f.read()

    def GetDay2Date(self, PatientStart):
        date_1 = datetime.datetime.strptime(PatientStart, "%d-%m-%Y")
        next_day = date_1 + datetime.timedelta(days=1)
        PatientDay2 = str(next_day.day) + '-' + str(next_day.month) + '-' + str(next_day.year)
        return PatientDay2
    
    def GetFullName(self):
        PatientName = ""
        FirstName = db.child("patientUsers").child(self.PatientID).child("firstname").get().val()
        LastName = db.child("patientUsers").child(self.PatientID).child("lastname").get().val()
        PatientName = PatientName + FirstName + LastName
        return PatientName

    def GetPatientInfo(self):
        
        PatientName = self.GetFullName()
        
        PatientDay1 = db.child("patientUsers").child(self.PatientID).child("start").get().val()
        PatientDay2 = self.GetDay2Date(PatientDay1)
        PatientDay3 = db.child("patientUsers").child(self.PatientID).child("end").get().val()
        
        WakeUpTime = db.child("patientUsers").child(self.PatientID).child("wakeup").get().val()
        BedTime = db.child("patientUsers").child(self.PatientID).child("sleep").get().val()
        
        return PatientName, PatientDay1, PatientDay2, PatientDay3, WakeUpTime, BedTime
    
    def GetVoidData(self, dayID):

        EpisodeDayID = dayID + "episode"
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child(EpisodeDayID).get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        if PatientUroflowData_VoidType != None:
            VoidType = PatientUroflowData_VoidType
        else:
            VoidType = []

        Volume = db.child("patientData").child(self.PatientID).child(dayID).child("volume").get()
        PatientUroflowData_Volume = Volume.val()
        if PatientUroflowData_Volume != None:
            VoidVolume = PatientUroflowData_Volume.split(',')
        else:
            VoidVolume = []

        VoidTimeList = []
        PatientUroflowData_Time = db.child("patientData").child(self.PatientID).child(dayID).child("time").get()
        PatientUroflowData_Time = PatientUroflowData_Time.val()
        if PatientUroflowData_Time != None:
            VoidTimeArray = PatientUroflowData_Time.split(',')
            for i in range(0, len(VoidTimeArray)):
                Time = VoidTimeArray[i]
                VoidTime = Time[0] + Time[1] + ':' + Time[2] + Time[3]
                VoidTimeList.append(VoidTime)
        else:
            pass
        
        Osmolality = db.child("patientData").child(self.PatientID).child(dayID).child("osmolality").get()
        PatientUroflowData_Osmolality = Osmolality.val()
        if PatientUroflowData_Osmolality != None:
            VoidOsmolality = PatientUroflowData_Osmolality.split(',')
        else:
            VoidOsmolality = []
            
        QMax = db.child("patientData").child(self.PatientID).child(dayID).child("qmax").get()
        PatientUroflowData_QMax = QMax.val()
        if PatientUroflowData_QMax != None:
            VoidQMax = PatientUroflowData_QMax.split(',')
        else:
            VoidQMax = []
        
        FluidIntakeDayID = dayID + "FluidIntake"
        FluidIntake = db.child("patientData").child(self.PatientID).child(FluidIntakeDayID).get().val()
        
        return VoidType, VoidVolume, VoidTimeList, VoidOsmolality, VoidQMax, FluidIntake
    
    def DailyReportData(self, FluidIntake, VoidVolume):
        TotalInput = FluidIntake
        TotalOutput = np.sum(VoidVolume)
        NocturiaNumber = 
        NPI =
        NPPresent =

    def RetrievePatientData(self):
        
        PatientName, PatientDay1, PatientDay2, PatientDay3, WakeUpTime, BedTime = self.GetPatientInfo()
        
        VoidType_Day1, VoidVolume_Day1, VoidTimeList_Day1, VoidOsmolality_Day1, VoidQMax_Day1, FluidIntake_Day1 = self.GetVoidData("day 1")
        VoidType_Day2, VoidVolume_Day2, VoidTimeList_Day2, VoidOsmolality_Day2, VoidQMax_Day2, FluidIntake_Day2 = self.GetVoidData("day 2")
        VoidType_Day3, VoidVolume_Day3, VoidTimeList_Day3, VoidOsmolality_Day3, VoidQMax_Day3, FluidIntake_Day3 = self.GetVoidData("day 3")

        SumVoidVolume1 = np.sum(VoidVolume1)
        SumVoidVolume2 = np.sum(VoidVolume2)
        SumVoidVolume3 = np.sum(VoidVolume3)

        print("Total output volume for day 1:" + " " + str(SumVoidVolume1))
        print("Total output volume for day 2:" + " " + str(SumVoidVolume2))
        print("Total output volume for day 3:" + " " + str(SumVoidVolume3))

        #No. of nocturia polyuria episode
        NocturiaEpisode = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("NoOfNocturiaEpisode").get().val()
        print("No. of nocturia episodes for day 1:" + " " + str(NocturiaEpisode))

        #Polyuria Index (Nocturia/Total episode x 100%)
        TotalEp = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("TotalEpisode").get().val()
        # print(TotalEp)
        PolyuriaIndex = (NocturiaEpisode/TotalEp)*100
        print("Polyuria Index for day 1:" + " " + str(PolyuriaIndex) + "%")

        #Presence of Polyuria (>30% = presence of polyuria)
        if PolyuriaIndex >= 30: 
            print("Presence of nocturia polyuria detected.")
        else:
            print("No presence of nocturia polyuria detected.")
        
        #Daytime Frequency Range (Normal Voids/Total daytime hours)
        NormalVoids = TotalEp = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("NoOfNormalEp").get().val()

        PatientWakeTime = db.child("patientUsers").child("patient1").child("wakeup").get().val()
        PatientSleepTime = db.child("patientUsers").child("patient1").child("sleep").get().val()

        WakeTime = datetime.strptime(str(PatientWakeTime),"%H%M")
        SleepTime = datetime.strptime(str(PatientSleepTime),"%H%M")
        time_interval = datetime.strptime(str(SleepTime - WakeTime),"%H:%M:%S")
        TotalHours = time_interval.hour
        DTFreqRange = NormalVoids/TotalHours

        print("Daytime frequency range:" + " " + str(DTFreqRange))

        #Usual Daytime Freq


        #Maximal Voided Volume (MVV)
        MaxVol1 = max(VoidVolume1)
        MaxVol2 = max(VoidVolume2)
        MaxVol3 = max(VoidVolume3)

        TotalMaxVols = [MaxVol1, MaxVol2, MaxVol3]
        MaxVoidedVol = max(TotalMaxVols)
        print("Maximal Voided Volume:" + str(MaxVoidedVol))
        