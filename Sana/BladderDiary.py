from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
import numpy as np
import pyrebase


config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class BladderDiary(Screen, EventDispatcher):

    def ShowLastVol(self):
        snapshot = db.child("patientData").child("patient1").child("day 1").child("volume").get()
        snapshotvalue = snapshot.val()
        arr = snapshotvalue.split(',')
        an_array = np.array(arr).astype(np.float)
        volume = an_array[-1]
        self.ids.LastVoid.text = str(int(volume)) + "ml"

    def ShowTotalVol(self):
        snapshot = db.child("patientData").child("patient1").child("day 1").child("volume").get()
        snapshotvalue = snapshot.val()
        arr = snapshotvalue.split(',')
        an_array = np.array(arr).astype(np.float)
        volume = np.sum(an_array)
        self.ids.TotalVoid.text = str(int(volume)) + "ml"

    def ShowVoidTime(self):
      VoidTimes = db.child("patientData").child("patient1").child("day 1").child("time").get()
      VoidTimesValues = VoidTimes.val()
      VoidTimesArr = VoidTimesValues.split(',')
      VoidTimeArray = np.array(VoidTimesArr).astype(np.float)
      TimeOfLastVoid = VoidTimeArray[-1]
      b = 10
      n = np.ceil(np.max(np.log(TimeOfLastVoid) / np.log(b))).astype(int)
      d = np.arange(n)
      d.shape = d.shape + (1,) * (TimeOfLastVoid.ndim)
      out = TimeOfLastVoid // b ** d % b
      self.ids.VoidTime.text = str(int(out[3])) + str(int(out[2])) + ":" + str(int(out[1]))+ str(int(out[0]))

    def GetVoidType(self, VoidEpisodes):
        VoidTypes = []
        for Episode in VoidEpisodes:
            VoidTypes.append(Episode)
        return VoidTypes

    def ShowVoidType(self):
        FireBase_VoidType = db.child("patientData").child("patient1").child("day 1").child("episode").get()
        FireBase_VoidType = FireBase_VoidType.val()
        FireBase_VoidType = FireBase_VoidType.split(',')
        VoidTypeList = self.GetVoidType(FireBase_VoidType)
        LatestVoidEpisodeType = VoidTypeList[-1]
        self.ids.VoidType.text = LatestVoidEpisodeType
