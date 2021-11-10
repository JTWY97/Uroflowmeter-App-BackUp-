from kivy.event import EventDispatcher
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.label import Label
from  kivy.uix.popup import Popup
import pyrebase
import numpy as np
from ExternalConnections.FirebaseTest import SendVoidType, GetVoidDetails
from kivy.uix.floatlayout import FloatLayout
import datetime

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

import os

class P(FloatLayout):
    pass

class BladderDiary(Screen, EventDispatcher):
    DayID = ''
    Patient_Variables = "./Context/Variables_Patient.txt"
    with open(Patient_Variables, "r") as f:
        PatientID = f.read()

    IconList = []
    
    def GetDaysAndRaspberryPiID(self):
        PatientStart = db.child("patientUsers").child(self.PatientID).child("start").get().val()
        PatientEnd = db.child("patientUsers").child(self.PatientID).child("end").get().val()

        date_1 = datetime.datetime.strptime(PatientStart, "%d-%m-%Y")
        next_day = date_1 + datetime.timedelta(days=1)
        PatientDay2 = str(next_day.day) + '-' + str(next_day.month) + '-' + str(next_day.year)

        RasberryPiID = db.child("patientUsers").child(self.PatientID).child("raspberrypi").get().val()
        ButtonID = db.child("patientUsers").child(self.PatientID).child("button").get().val()
        self.SetUpPatientData(RasberryPiID,  ButtonID, PatientStart, PatientDay2, PatientEnd)
        return RasberryPiID,  ButtonID, PatientStart, PatientDay2, PatientEnd

    def SetUpPatientData(self, RasberryPiID,  ButtonID, PatientStart, PatientDay2, PatientEnd):
        #day1
        VoidTime = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("time").get().val()
        VoidVolumes = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("volume").get().val()
        VoidColors = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("color").get().val()
        VoidQMax = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("qmax").get().val()

        VoidData = {"time":VoidTime, "volume":VoidVolumes, "color":VoidColors, "qmax":VoidQMax}

        db.child("patientData").child(self.PatientID).child("day 1").set(VoidData)
        
        # day2
        VoidTime = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("time").get().val()
        VoidVolumes = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("volume").get().val()
        VoidColors = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("color").get().val()
        VoidQMax = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("qmax").get().val()
        
        VoidData2 = {"time":VoidTime, "volume":VoidVolumes, "color":VoidColors, "qmax":VoidQMax}

        db.child("patientData").child(self.PatientID).child("day 2").set(VoidData2)
        
        #day3
        VoidTime = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("time").get().val()
        VoidVolumes = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("volume").get().val()
        VoidColors = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("color").get().val()
        VoidQMax = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("qmax").get().val()
        
        VoidData3 = {"time":VoidTime, "volume":VoidVolumes, "color":VoidColors, "qmax":VoidQMax}
        db.child("patientData").child(self.PatientID).child("day 3").set(VoidData3)

        self.ShowSummary("day 1")
        self.BuildTimeline("day 1")

    def GetData_VoidType(self, dayID):
        self.ids.BladderDiary.clear_widgets()
        self.ids.BladderSummary.clear_widgets()
        EpisodeDayID = dayID + 'episode'
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child(EpisodeDayID).get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        if PatientUroflowData_VoidType != None:
            VoidType = PatientUroflowData_VoidType
        else:
            VoidType = []
        return VoidType

    def GetData_Volume(self, dayID):
        Volume = db.child("patientData").child(self.PatientID).child(dayID).child("volume").get()
        PatientUroflowData_Volume = Volume.val()
        if PatientUroflowData_Volume != None:
            VoidVolume = PatientUroflowData_Volume.split(',')
        else:
            VoidVolume = []
        return VoidVolume

    def GetData_Time(self, dayID):
        VoidTimeList = []
        PatientUroflowData_Time = db.child("patientData").child(self.PatientID).child(dayID).child("time").get()
        PatientUroflowData_Time = PatientUroflowData_Time.val()
        if PatientUroflowData_Time != None:
            VoidTimeArray = PatientUroflowData_Time.split(',')
            print(VoidTimeArray)
            for i in range(0, len(VoidTimeArray)):
                Time = VoidTimeArray[i]
                VoidTime = Time[0] + Time[1] + ':' + Time[2] + Time[3]
                VoidTimeList.append(VoidTime)
        else:
            VoidTimeList = []
            VoidTimeArray = []
            
        return VoidTimeList, VoidTimeArray

    def GetSleepPattern(self):
        PatientBedTime = db.child("patientUsers").child(self.PatientID).child("sleep").get().val()
        PatientWakeTime = db.child("patientUsers").child(self.PatientID).child("wakeup").get().val()
        return PatientBedTime, PatientWakeTime

    def WarningMessage(self):
        popupWarning = Popup(title='Uh Oh!', content=Label(text='You have no recorded data for this day.'), size_hint=(None, None), size=(400, 400))
        popupWarning.open()

    def EditVoidData(self, VoidIndex):
        show = P()
        print("testets" + str(VoidIndex))
        GetVoidDetails(str(VoidIndex), str(self.DayID))
        popupVoid = Popup(title = 'Would you like to edit this void?', content=show, size_hint=(None, None), size=(1000, 1000))
        popupVoid.open()

    def ShowSummary(self, dayID):
        VoidVolume = self.GetData_Volume(dayID)
        TotalVoidVolume = []
        if len(VoidVolume) != 0:
            ScreenLayout = self.ids['BladderSummary']
            NumberofVoids = (len(VoidVolume))
            for i in range(0, len(VoidVolume)):
                TotalVoidVolume.append(float(VoidVolume[i]))
            TotalVoid = np.sum(TotalVoidVolume)

            NumberOfVoids_Entry = OneLineAvatarListItem(text = "Total Number of Voids Logged Today: " + str(NumberofVoids))
            TotalVoidVolume_Entry = OneLineAvatarListItem(text = "Total Volume Voided Today: " + str(TotalVoid))

            ScreenLayout.add_widget(NumberOfVoids_Entry)
            ScreenLayout.add_widget(TotalVoidVolume_Entry)
        else:
            pass

    def edit_void_callback(self, instance):
        print(instance)
        print(len(self.IconList))
        Index = self.IconList.index(instance)
        self.EditVoidData(Index)

    def BuildTimeline(self, dayID):
        self.DayID = dayID
        print("BuildTimeLine:", self.DayID)
        VoidType = self.GetData_VoidType(dayID)
        VoidTime, VoidTimeRaw = self.GetData_Time(dayID)
        VoidVolume = self.GetData_Volume(dayID)
        self.IconList.clear()
        
        SleepTime, WakeTime = self.GetSleepPattern()

        if len(VoidVolume) != 0:

            ScreenLayout = self.ids['BladderDiary']

            MorningEpisode = VoidType.count("First Morning Episode")
            
            if len(VoidType) != len(VoidTime):
                if len(VoidType) != 0:
                    for k in range(len(VoidType), len(VoidTime)):
                        if int(VoidTimeRaw[k]) <= int(WakeTime):
                            VoidType.append("Nocturia Episode")
                        elif int(VoidTimeRaw[k]) >= int(SleepTime):
                            VoidType.append("Nocturia Episode")
                        elif int(VoidTimeRaw[k]) >= int(WakeTime):
                            if MorningEpisode == 0:
                                VoidType.append("First Morning Episode")
                                MorningEpisode += 1
                            else:
                                VoidType.append("Normal Episode")

                else:
                    for k in range(0, len(VoidTime)):
                        if int(VoidTimeRaw[k]) <= int(WakeTime):
                            VoidType.append("Nocturia Episode")
                        elif int(VoidTimeRaw[k]) >= int(SleepTime):
                            VoidType.append("Nocturia Episode")
                        elif int(VoidTimeRaw[k]) >= int(WakeTime):
                            if MorningEpisode != 1:
                                VoidType.append("First Morning Episode")
                                MorningEpisode += 1
                            else:
                                VoidType.append("Normal Episode")
                    
                    

                EpisodeDayID = dayID + 'episode'

                SendVoidType(VoidType, self.PatientID, EpisodeDayID)
                for i in range(0, len(VoidTime)):
                    if VoidType[i] == "First Morning Episode":
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Morning.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    elif VoidType[i] == "Normal Episode":
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Normal.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    elif VoidType[i] == "Nocturia Episode":
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Nocturia.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    else:
                        Icon = IconLeftWidget(icon="human")

                    ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[i]), secondary_text = "Void Type: " + VoidType[i], tertiary_text = "Voud Volume: " + VoidVolume[i] + "ml")
                    ListComponents.add_widget(Icon)
                    
                    ScreenLayout.add_widget(ListComponents)
            else:
                print("IMPORTANT" , VoidType)
                NoOfNocturiaEp = 0
                NoOfNormalEp = 0

                for i in range(0, len(VoidTime)):
                    if VoidType[i] == "First Morning Episode":
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Morning.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    elif VoidType[i] == "Normal Episode":
                        NoOfNormalEp += 1
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Normal.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    elif VoidType[i] == "Nocturia Episode":
                        NoOfNocturiaEp += 1
                        Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Nocturia.png", on_press = self.edit_void_callback)
                        self.IconList.append(Icon)
                    else:
                        Icon = IconLeftWidget(icon="human")

                    ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[i]), secondary_text = "Void Type: " + VoidType[i], tertiary_text = "Voud Volume: " + VoidVolume[i] + "ml")
                    ListComponents.add_widget(Icon)
                    
                    ScreenLayout.add_widget(ListComponents)
            
                #Add Total Ep count & Nocturia Ep count on to google firebase
                EpisodeCount = {"NoOfNocturiaEpisode": NoOfNocturiaEp, "NoOfNormalEp": NoOfNormalEp, "TotalEpisode": len(VoidType)}
                db.child("raspberrypi").child("raspberry1").child("button1").child("03-11-2021").update(EpisodeCount) #how dayID is being defined, instead of hardcoding what should be the variable? 
            
        else:
            self.WarningMessage()
    
