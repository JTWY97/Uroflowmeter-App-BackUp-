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

class BladderDiary(Screen):
    Patient_Variables = "Variables_Patient.txt"
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

    def BuildTimeline(self):
        ScreenLayout = self.ids['BladderDiaryWidgets']
        VoidType = self.GetData_VoidType()
        VoidTime = self.GetData_Time()
        VoidVolume = self.GetData_Volume()

        for i in range(0,len(VoidTime)):
            if VoidType[-i] == "First Morning Episode":
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Morning.png")
            elif VoidType[-i] == "Normal Episode":
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Normal.png")
            elif VoidType[-i] == "Nocturia Episode":
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Nocturia.png")
            else:
                Icon = IconLeftWidget(icon="human")

            ListComponents = ThreeLineAvatarListItem(text = str(VoidTime[-i]), secondary_text = "Void Type: " + VoidType[-i], tertiary_text = "Void Volume: " + VoidVolume[-i]+ "ml")

            ListComponents.add_widget(Icon)
            ScreenLayout.add_widget(ListComponents)
            i+=1

    def ShowSummary(self):
        ScreenLayout = self.ids['BladderSummary']
        VoidType = self.GetData_VoidType()
        VoidVolume = self.GetData_Volume()
        MorningVoidVolume = []
        Morning = 0
        NormalVoidVolume = []
        Normal = 0
        NightVoidVolume = []
        Night = 0
        
        NumberofVoids = (len(VoidType))

        for i in range(0, len(VoidType)):
            if VoidType[i] == "First Morning Episode":
                Morning +=1
                MorningVoidVolume.append(float(VoidVolume[i]))
                print(MorningVoidVolume)
            elif VoidType[i] == "Normal Episode":
                Normal += 1
                NormalVoidVolume.append(float(VoidVolume[i]))
            elif VoidType[i] == "Nocturia Episode":
                Night +=1
                NightVoidVolume.append(float(VoidVolume[i]))
        
        if Morning >= Night:
            if Morning >= Normal:
                MostFrequentEpisode = "First Morning Episode"
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Morning.png")
            else:
                MostFrequentEpisode = "Normal Episode"
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Normal.png")
        else:
            if Night >= Normal:
                MostFrequentEpisode = "Nocturia Episode"
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Nocturia.png")
            else:
                MostFrequentEpisode = "Normal Episode"
                Icon = IconLeftWidget(icon="Styles/BladderDiaryIcons/Normal.png")

        TotalMorningVoid = np.sum(MorningVoidVolume)
        TotalNormalVoid = np.sum(NormalVoidVolume)
        TotalNightVoid = np.sum(NightVoidVolume)

        NumberOfVoids_Entry = OneLineAvatarListItem(text = "Total Number of Voids: " + str(NumberofVoids))
        MostFrequentEpisode_Entry = OneLineAvatarListItem(text = MostFrequentEpisode)
        MostFrequentEpisode_Entry.add_widget(Icon)
        Morning_Entry = OneLineAvatarListItem(text = "Total Number of Morning Voids: " + str(Morning))
        TotalMorningVoid_Entry = OneLineAvatarListItem(text = "Total Volume of Morning Voids: " + str(TotalMorningVoid) + "ml")
        Normal_Entry = OneLineAvatarListItem(text = "Total Number of Morning Voids: " + str(Normal))
        TotalNormalVoid_Entry = OneLineAvatarListItem(text =  "Total Volume of Normal Voids: " + str(TotalNormalVoid) + "ml")
        Night_Entry = OneLineAvatarListItem(text = "Total Number of Night Voids: " + str(Night))
        TotalNightVoid_Entry = OneLineAvatarListItem(text =  "Total Volume of Nocturia Voids: " + str(TotalNightVoid) + "ml")
        
        ScreenLayout.add_widget(NumberOfVoids_Entry)
        ScreenLayout.add_widget(MostFrequentEpisode_Entry)
        ScreenLayout.add_widget(Morning_Entry)
        ScreenLayout.add_widget(TotalMorningVoid_Entry)
        ScreenLayout.add_widget(Normal_Entry)
        ScreenLayout.add_widget(TotalNormalVoid_Entry)
        ScreenLayout.add_widget(Night_Entry)
        ScreenLayout.add_widget(TotalNightVoid_Entry)