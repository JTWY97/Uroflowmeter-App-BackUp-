from kivy.uix.screenmanager import Screen
import pyrebase
from ExternalConnections.FirebaseTest import VoidIndexFetched, WhichDay

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

    SymptomList = []
    EpiDay = ''
    VoidNo = ''

    def GetSetupData(self):
        if len(VoidIndexFetched) != 0:
            VoidNumber = VoidIndexFetched[-1]
        else:
            VoidNumber = 0
        if len(WhichDay) != 0:
            if WhichDay[-1] == 1:
                DayID = "day 1"
            elif WhichDay[-1] == 2:
                DayID = "day 2"
            elif WhichDay[-1] == 3:
                DayID = "day 3"
            else:
                DayID = "day 1"
                print("ERROR IN FETCHING DAY ID")
        else:
            DayID = "day 1"
        self.SymptomList.append(VoidNumber)
        self.ShowVoid(VoidNumber, DayID)

    def GetData_VoidType(self, dayID, VoidNumber):
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child(dayID).child(VoidNumber).get()
        VoidType = PatientUroflowData_VoidType.val()
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

    def ShowVoid(self, VoidNumber, dayID):
        
        EpisodeDayID = dayID + 'episode'
        self.EpiDay = EpisodeDayID
        self.VoidNo = VoidNumber
        
        VoidType = self.GetData_VoidType(EpisodeDayID, VoidNumber)
        VoidTime, VoidTimeRaw = self.GetData_Time(dayID)
        VoidVolume = self.GetData_Volume(dayID)

        self.ids.VoidInfo.text = "VoidTime: " + VoidTime[int(VoidNumber)]
        self.ids.VoidInfo.secondary_text = "Void Type: " + VoidType
        self.ids.VoidInfo.tertiary_text = "Void Volume: " + VoidVolume[int(VoidNumber)]+ "ml"
        if VoidType == "First Morning Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Morning.png"
        elif VoidType == "Normal Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Normal.png"
        elif VoidType == "Nocturia Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Nocturia.png"

    def ChangeVoidType(self, button):
        if button == 'Morning':
            db.child("patientData").child(self.PatientID).child(str(self.EpiDay)).update({str(self.VoidNo):"First Morning Episode"})
            self.UpdateVoidDisplayed("First Morning Episode")
        elif button == 'Normal':
            db.child("patientData").child(self.PatientID).child(str(self.EpiDay)).update({str(self.VoidNo):"Normal Episode"})
            self.UpdateVoidDisplayed("Normal Episode")
        elif button == 'Nocturia':
            db.child("patientData").child(self.PatientID).child(str(self.EpiDay)).update({str(self.VoidNo):"Nocturia Episode"})
            self.UpdateVoidDisplayed("Nocturia Episode")

    def UpdateVoidDisplayed(self, VoidType):
        self.ids.VoidInfo.secondary_text = "Void Type: " + VoidType
        if VoidType == "First Morning Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Morning.png"
        elif VoidType == "Normal Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Normal.png"
        elif VoidType == "Nocturia Episode":
            self.ids.VoidInfoIcon.icon = "./Styles/BladderDiaryIcons/Nocturia.png"

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

        elif button == 'button7':
            Symptom = "Foul Smelly Urine"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button8':
            Symptom = "Pain in Pelvic Area"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button9':
            Symptom = "Hesitancy to Urinate"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button10':
            Symptom = "Cramp on Side"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

        elif button == 'button11':
            Symptom = "Cloudy Urine"
            self.SymptomList.append(Symptom)
            self.SendSymptomToFirebase()
            return self.SymptomList

    def SendSymptomToFirebase(self):
        SymptomTrackerChild = "Symptoms" + self.EpiDay
        Label = self.EpiDay + self.VoidNo
        data = {Label: str(self.SymptomList)}
        db.child("patientData").child(self.PatientID).child(SymptomTrackerChild).update(data)