from kivymd.uix.list import MDList, ThreeLineAvatarListItem, OneLineAvatarListItem
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
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

class DiaryEntry(MDList):
    pass

class DiarySummary(MDList):
    pass

class DynamicBladderDiary(Screen):

    def GetData_Volume(self):
        Volume = db.child("patientData").child("patient1").child("day 1").child("volume").get()
        PatientUroflowData_Volume = Volume.val()
        VoidVolume = PatientUroflowData_Volume.split(',')
        return VoidVolume

    def GetData_Time(self):
        VoidTimeList = []
        PatientUroflowData_Time = db.child("patientData").child("patient1").child("day 1").child("time").get()
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
        PatientUroflowData_VoidType = db.child("patientData").child("patient1").child("day 1").child("episode").get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        VoidType = PatientUroflowData_VoidType.split(',')
        return VoidType

    def BuildTimeline(self):
        ScreenLayout = self.ids['BladderDiary']
        VoidType = self.GetData_VoidType()
        VoidTime = self.GetData_Time()
        VoidVolume = self.GetData_Volume()

        for i in range(0,len(VoidTime)):
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

    def ShowSummary(self):
        ScreenLayout = self.ids['BladderSummary']
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

            ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[i]), secondary_text = "Void Type: " + VoidType[-i], tertiary_text = "Void Volume: " + VoidVolume[-i]+ "ml")

            ListComponents.add_widget(Icon)
            ScreenLayout.add_widget(ListComponents)
            i+=1