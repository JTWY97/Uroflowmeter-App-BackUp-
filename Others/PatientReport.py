from kivymd.app import MDApp
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
from datetime import datetime, date
# from ExternalConnections.FirebaseTest import SendVoidType, GetVoidDetails
from kivy.uix.floatlayout import FloatLayout

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class PatientReport():

  def RetrievePatientData(self, RasberryPiID,  ButtonID, PatientStart, PatientDay2, PatientEnd):

      #Total Fluid Intake
      #will the fluid intake be updated in firebase? take from patientData
      
      
      #Total ouput (void volume)
      result = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientStart).child("volume").get().val()
      result = result.split(",") 
      VoidVolume1 = np.array(result).astype(float)

      result = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("volume").get().val()
      result = result.split(",") 
      VoidVolume2 = np.array(result).astype(float)

      result = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("volume").get().val()
      result = result.split(",") 
      VoidVolume3 = np.array(result).astype(float)

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

      #Daytime Voided Volume Range


      #Usual Daytime Voided Volume (average)


      #Qmax Range

      



PatientReport().RetrievePatientData("raspberry1", "button1", "03-11-2021", "04-11-2021", "05-11-2021")

   

    
