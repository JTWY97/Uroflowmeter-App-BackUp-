from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
import pyrebase
import numpy as np
from ExternalConnections.FirebaseTest import SendVoidType

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

    def GetData_Volume(self, dayID):
        print(dayID)
        Volume = db.child("patientData").child(self.PatientID).child(dayID).child("volume").get()
        PatientUroflowData_Volume = Volume.val()
        VoidVolume = PatientUroflowData_Volume.split(',')
        return VoidVolume

    def GetData_Time(self, dayID):
        VoidTimeList = []
        PatientUroflowData_Time = db.child("patientData").child(self.PatientID).child(dayID).child("time").get()
        PatientUroflowData_Time = PatientUroflowData_Time.val()
        VoidTimeArray = PatientUroflowData_Time.split(',')
        VoidTimeArray = np.array(VoidTimeArray).astype(np.float)
        print(VoidTimeArray)
        for i in range(0, len(VoidTimeArray)):
            VoidTime = self.GetTime_Text(VoidTimeArray[i])
            VoidTimeList.append(VoidTime)
        return VoidTimeList, VoidTimeArray

    def GetTime_Text(self,VoidTimeArray):
        TimeOfLastVoid = VoidTimeArray
        b = 10
        n = np.ceil(np.max(np.log(TimeOfLastVoid) / np.log(b))).astype(int)
        d = np.arange(n)
        d.shape = d.shape + (1,) * (TimeOfLastVoid.ndim)
        out = TimeOfLastVoid // b ** d % b
        VoidTime = str(int(out[3])) + str(int(out[2])) + ":" + str(int(out[1]))+ str(int(out[0]))
        return VoidTime

    def GetData_VoidType(self, dayID):
        print("PatientID:" + self.PatientID)
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child(dayID).child("episode").get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        print(PatientUroflowData_VoidType)
        if PatientUroflowData_VoidType != None:
            VoidType = PatientUroflowData_VoidType.split(',')
        else:
            VoidType = []
        return VoidType

    def GetSleepPattern(self):
        PatientBedTime = db.child("patientUsers").child(self.PatientID).child("sleep").get().val()
        PatientWakeTime = db.child("patientUsers").child(self.PatientID).child("wakeup").get().val()
        return PatientBedTime, PatientWakeTime

    def ShowSummary(self, dayID):
        ScreenLayout = self.ids['BladderSummary']

        VoidVolume = self.GetData_Volume(dayID)
        TotalVoidVolume = []
        
        NumberofVoids = (len(VoidVolume))
        for i in range(0, len(VoidVolume)):
            TotalVoidVolume.append(float(VoidVolume[i]))
        TotalVoid = np.sum(TotalVoidVolume)

        NumberOfVoids_Entry = OneLineAvatarListItem(text = "Total Number of Voids Logged Today: " + str(NumberofVoids))
        TotalVoidVolume_Entry = OneLineAvatarListItem(text = "Total Volume Voided Today: " + str(TotalVoid))

        ScreenLayout.add_widget(NumberOfVoids_Entry)
        ScreenLayout.add_widget(TotalVoidVolume_Entry)

    def BuildTimeline(self, dayID):
        print(dayID)
        ScreenLayout = self.ids['BladderDiary']
        VoidType = self.GetData_VoidType(dayID)
        VoidTime, VoidTimeRaw = self.GetData_Time(dayID)
        VoidVolume = self.GetData_Volume(dayID)

        SleepTime, WakeTime = self.GetSleepPattern()
        AutomatedVoidType = []

        MorningEpisode = VoidType.count("First Morning Episode")
        if len(VoidType) != len(VoidTime):
            if len(VoidType) != 0:
                Difference = len(VoidTime) - len(VoidType)
                for k in range(Difference, len(VoidTime)):
                    if int(VoidTimeRaw[k]) <= int(WakeTime):
                        AutomatedVoidType.append("Nocturia Episode")
                    elif int(VoidTimeRaw[k]) >= int(SleepTime):
                        AutomatedVoidType.append("Nocturia Episode")
                    elif int(VoidTimeRaw[k]) >= int(WakeTime):
                        if MorningEpisode == 0:
                            AutomatedVoidType.append("First Morning Episode")
                            MorningEpisode += 1
                        else:
                            AutomatedVoidType.append("Normal Episode")
            else:
                for k in range(0, len(VoidTime)):
                    if int(VoidTimeRaw[k]) <= int(WakeTime):
                        AutomatedVoidType.append("Nocturia Episode")
                    elif int(VoidTimeRaw[k]) >= int(SleepTime):
                        AutomatedVoidType.append("Nocturia Episode")
                    elif int(VoidTimeRaw[k]) >= int(WakeTime):
                        if MorningEpisode != 1:
                            AutomatedVoidType.append("First Morning Episode")
                            MorningEpisode += 1
                        else:
                            AutomatedVoidType.append("Normal Episode")
                            
        SendVoidType(str(AutomatedVoidType), self.PatientID)

        for i in range(0, len(VoidTime)):
            if AutomatedVoidType[i] == "First Morning Episode":
                Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Morning.png")
            elif AutomatedVoidType[i] == "Normal Episode":
                Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Normal.png")
            elif AutomatedVoidType[i] == "Nocturia Episode":
                Icon = IconLeftWidget(icon="./Styles/BladderDiaryIcons/Nocturia.png")
            else:
                Icon = IconLeftWidget(icon="human")

            ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[i]), secondary_text = "Void Type: " + AutomatedVoidType[i], tertiary_text = "Void Volume: " + VoidVolume[i]+ "ml")

            ListComponents.add_widget(Icon)
            ScreenLayout.add_widget(ListComponents)
            i+=1