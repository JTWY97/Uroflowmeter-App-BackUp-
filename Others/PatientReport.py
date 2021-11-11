from sys import float_info
from kivy.event import EventDispatcher
import matplotlib
import pyrebase
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
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

  def RetrievePatientData(self, RasberryPiID,  ButtonID, PatientStart, PatientDay2, PatientEnd, PatientID, dayID):

      ## DAILY STATS ##

      #--> 1. Total Fluid Intake
      TotalFluidIntake = db.child("patientData").child(PatientID).child(dayID).child("day 1Fluidintake").get().val()
      if TotalFluidIntake == None:
        print("Fluid intake has not been logged.")
      
      else:
        print("Total Fluid Intake: " + str(TotalFluidIntake) + "ml")
        
      
      #--> 2. Total ouput volume(void volume)
      #day 1
      result = db.child("patientData").child(PatientID).child(dayID).child("volume").get().val()
      result = result.split(",") 
      VoidVolume1 = np.array(result).astype(float)
      SumVoidVolume1 = np.sum(VoidVolume1)
    
      print("Total output volume for day 1: " + str(SumVoidVolume1) + "ml")

      #day 2
      result = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("volume").get().val()
      result = result.split(",") 
      VoidVolume2 = np.array(result).astype(float)
      SumVoidVolume2 = np.sum(VoidVolume2)
    
      print("Total output volume for day 2: " + str(SumVoidVolume2) + "ml")

      #day 3
      result = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("volume").get().val()
      result = result.split(",") 
      VoidVolume3 = np.array(result).astype(float)
      SumVoidVolume3 = np.sum(VoidVolume3)
    
      print("Total output volume for day 3: " + str(SumVoidVolume3) + "ml")
      
  

      #--> 3. No. of nocturia polyuria episode
      TotalEpList = db.child("patientData").child(PatientID).child(dayID).child("day 1episode").get().val()
      print(TotalEpList)
      
      NocturiaEpisode = db.child("patientData").child(PatientID).child(dayID).child("NoOfNocturiaEpisode").get().val()
      print("No. of nocturia episodes for day 1: " + str(NocturiaEpisode))

      #--> 4. Polyuria Index (Nocturia/Total episode x 100%)
      TotalEp = db.child("patientData").child(PatientID).child(dayID).child("TotalEpisode").get().val()

      PolyuriaIndex = (NocturiaEpisode/TotalEp)*100
      print("Polyuria Index: " + str(PolyuriaIndex) + "%")

      #--> 5. Presence of Polyuria (>30% = presence of polyuria)
      if PolyuriaIndex >= 30: 
        print("Presence of nocturia polyuria detected.")
      else:
        print("No presence of nocturia polyuria detected.")

      #plot graph for daily stats

      plt.plot([1, 2, 3], [1, 4, 9, 16])
      plt.xlabel('x values')
      plt.ylabel('y values')


      plt.show()

      ## OVERALL STATS ##
    
      #-->Daytime Frequency Range (Normal Voids/Total daytime hours)

      # NormalVoids1 = db.child("patientData").child(PatientID).child(dayID).child("NoOfNormalEp").get().val()
      # NormalVoids2 = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientDay2).child("NoOfNormalEp").get().val()
      # NormalVoids3 = db.child("raspberrypi").child(RasberryPiID).child(ButtonID).child(PatientEnd).child("NoOfNormalEp").get().val()


      # PatientWakeTime = db.child("patientUsers").child("patient1").child("wakeup").get().val()
      # PatientSleepTime = db.child("patientUsers").child("patient1").child("sleep").get().val()

      # WakeTime = datetime.strptime(str(PatientWakeTime),"%H%M")
      # SleepTime = datetime.strptime(str(PatientSleepTime),"%H%M")
      # time_interval = datetime.strptime(str(SleepTime - WakeTime),"%H:%M:%S")
      # TotalHours = time_interval.hour
      
      # if NormalVoids1 == None:
      #   NormalVoids1 = 0
      #   print("Normal voids for day 1 have not been logged yet.")
      # else:
      #   DTFreq1= NormalVoids1/TotalHours

      # if NormalVoids2 == None:
      #   NormalVoids2 = 0
      #   print("Normal voids for day 2 have not been logged yet.")
      # else:
      #   DTFreq2= NormalVoids2/TotalHours

      # if NormalVoids3 == None:
      #   NormalVoids3 = 0
      #   print("Normal voids for day 3 have not been logged yet.")
      # else:
      #   DTFreq3= NormalVoids3/TotalHours

      # DTFreqList = [DTFreq1, DTFreq2, DTFreq3]
      # MaxDTFreq = max(DTFreqList)
      # MinDTFreq = min(DTFreqList)

      # print("Daytime frequency range:" + " " + str(MinDTFreq) + " - " + str(MaxDTFreq))

      #-->Usual Daytime Freq (count all the normal episodes) - line plot day timefreq vs. day # represent in a graph
      
      NoOfNormalEp = db.child("patientData").child(PatientID).child(dayID).child("NoOfNormalEp").get().val()
  
      print(NoOfNormalEp)


      #-->Maximal Voided Volume (MVV)
      MaxVol1 = max(VoidVolume1)
      MaxVol2 = max(VoidVolume2)
      MaxVol3 = max(VoidVolume3)

      TotalMaxVols = [MaxVol1, MaxVol2, MaxVol3]
      MaxVoidedVol = max(TotalMaxVols)
      print("Maximal Voided Volume:" + str(MaxVoidedVol))

      #-->Daytime Voided Volume Range




      #-->make a string of void types -> count normal void + append index of normal void positions -> only call those positions from fluid data



      #-->Usual Daytime Voided Volume (average)



      #-->Qmax Range
      
      QmaxListFirebase = db.child("patientData").child(PatientID).child(dayID).child("qmax").get().val()
      QmaxListFirebase = QmaxListFirebase.split(",") 
      QmaxList = np.array(QmaxListFirebase).astype(int)
      MaxQmax = max(QmaxList)
      MinQmax = min(QmaxList)
      print ("Qmax range: " + str(MinQmax) + "-" + str(MaxQmax))

    

      



PatientReport().RetrievePatientData("raspberry1", "button1", "03-11-2021", "04-11-2021", "05-11-2021", "patient1", "day 1")

   

    
