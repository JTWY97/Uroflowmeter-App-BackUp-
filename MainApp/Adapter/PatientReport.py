import pyrebase
import numpy as np
from kivy.uix.screenmanager import Screen
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

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
    
    def GetVoidData(self, dayID, WhichCollection):

        EpisodeDayID = dayID + "episode"
        PatientUroflowData_VoidType = db.child("patientData").child(self.PatientID).child(EpisodeDayID).get()
        PatientUroflowData_VoidType = PatientUroflowData_VoidType.val()
        if PatientUroflowData_VoidType != None:
            VoidType = PatientUroflowData_VoidType
            print(VoidType)
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
        FluidIntake = db.child("patientData").child(self.PatientID).child(FluidIntakeDayID).child("total fluid intake").get().val()
        
        TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent = self.VoidTypeInfo(VoidType, VoidVolume, FluidIntake)
        if WhichCollection == "DailyTable":
            return TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent
        elif WhichCollection == "DailyGraph":
            return VoidVolume, VoidTimeList
    
    def VoidTypeInfo(self, VoidType, VoidVolume, FluidIntake):
        NoOfNocturiaEp = 0
        NoOfNormalEp = 0
        NoOfMorningEp = 0

        NocturiaVoidVol = []
        MorningVoidVol = []
        NormalVoidVol = []
        print(len(VoidVolume))
        print(len(VoidType))
        for i in range(0, len(VoidType)):
            if VoidType[i] == "First Morning Episode":
                MorningVoidVol.append(VoidVolume[i])
                NoOfMorningEp += 1
            elif VoidType[i] == "Normal Episode":
                NormalVoidVol.append(VoidVolume[i])
                NoOfNormalEp += 1
            elif VoidType[i] == "Nocturia Episode":
                NocturiaVoidVol.append(VoidVolume[i])
                NoOfNocturiaEp += 1
        
        TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent= self.DailyReportData(FluidIntake, VoidVolume, NoOfNocturiaEp, NocturiaVoidVol, MorningVoidVol)
        return TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent
    
    def DailyReportData(self, FluidIntake, VoidVolume, NoOfNocturiaEp, NocturiaVoidVol, MorningVoidVol):
        
        TotalInput = FluidIntake
        VoidVolume = np.array(VoidVolume).astype(float)
        TotalOutput = np.sum(VoidVolume)
        NocturiaNumber = NoOfNocturiaEp
        NocturiaVoidVol = np.array(NocturiaVoidVol).astype(float)
        MorningVoidVol = np.array(MorningVoidVol).astype(float)
        NocturiaVoidVol = np.sum(NocturiaVoidVol) + np.sum(MorningVoidVol)
        NPI = (NocturiaVoidVol/TotalOutput)*100
        if NocturiaNumber != 0:
            NcoturiaPresent = "Yes"
        else:
            NcoturiaPresent = "No"
        
        return TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent

    def CollectingData(self):
        
        #Data for Day Report
        TotalInput_Day1, TotalOutput_Day1, NocturiaNumber_Day1, NPI_Day1, NocturiaPresent_Day1 = self.GetVoidData("day 1", "DailyTable")
        TotalInput_Day2, TotalOutput_Day2, NocturiaNumber_Day2, NPI_Day2, NocturiaPresent_Day2 = self.GetVoidData("day 2", "DailyTable")
        TotalInput_Day3, TotalOutput_Day3, NocturiaNumber_Day3, NPI_Day3, NocturiaPresent_Day3 = self.GetVoidData("day 3", "DailyTable")
        
        Day1 = {'Total Input (ml)': TotalInput_Day1, 'Total Output (ml)': TotalOutput_Day1, 'Nocturia Episodes':  NocturiaNumber_Day1, 'NPI (%)': NPI_Day1, 'Nocturnal Polyuria': NocturiaPresent_Day1}
        print(Day1)
        Day1DF = pd.DataFrame(data=Day1,index=[0])
        print(Day1DF)
        Day2 = {'Total Input (ml)': TotalInput_Day2, 'Total Output (ml)': TotalOutput_Day2, 'Nocturia Episodes':  NocturiaNumber_Day2, 'NPI (%)': NPI_Day2, 'Nocturnal Polyuria': NocturiaPresent_Day2}
        Day2DF = pd.DataFrame(data=Day2,index=[0])
        Day3 = {'Total Input (ml)': TotalInput_Day3, 'Total Output (ml)': TotalOutput_Day3, 'Nocturia Episodes':  NocturiaNumber_Day3, 'NPI (%)': NPI_Day3, 'Nocturnal Polyuria': NocturiaPresent_Day3}
        Day3DF = pd.DataFrame(data=Day3,index=[0])
        
        
        #Daily Graph Data
        
        VoidVolume_Day1, VoidTimeList_Day1 = self.GetVoidData("day 1", "DailyGraph")
        VoidVolume_Day2, VoidTimeList_Day2 = self.GetVoidData("day 2", "DailyGraph")
        VoidVolume_Day3, VoidTimeList_Day3 = self.GetVoidData("day 3", "DailyGraph")
        
        return Day1DF, VoidVolume_Day1, VoidTimeList_Day1, Day2DF, VoidVolume_Day2, VoidTimeList_Day2, Day3DF, VoidVolume_Day3, VoidTimeList_Day3
        
    def GenerateFigure(self):
        Day1DF, VoidVolume_Day1, VoidTimeList_Day1, Day2DF, VoidVolume_Day2, VoidTimeList_Day2, Day3DF, VoidVolume_Day3, VoidTimeList_Day3 = self.CollectingData()
        
        fig3 = plt.figure(constrained_layout=True, figsize= [10,8])
        gs = fig3.add_gridspec(4, 4)
        
        f3_ax1 = fig3.add_subplot(gs[0, -1])
        f3_ax2 = fig3.add_subplot(gs[0, -2])
        f3_ax3 = fig3.add_subplot(gs[0, :-2])
        f3_ax3.set_axis_off()

        f3_ax4 = fig3.add_subplot(gs[1, -1])
        f3_ax5 = fig3.add_subplot(gs[1, -2])
        f3_ax6 = fig3.add_subplot(gs[1, :-2])
        f3_ax6.set_axis_off()

        f3_ax7 = fig3.add_subplot(gs[2, -1])
        f3_ax8 = fig3.add_subplot(gs[2, -2])
        f3_ax9 = fig3.add_subplot(gs[2, :-2])
        f3_ax9.set_axis_off()

        f3_ax10 = fig3.add_subplot(gs[3, :])

        
        
        f3_ax1.scatter(VoidTimeList_Day1, VoidVolume_Day1)
        Day1Table = f3_ax3.table(cellText=Day1DF.values, colLabels=Day1DF.columns, loc='center')
        Day1Table.scale(1, 4)
        Day1Table.auto_set_font_size(False)
        Day1Table.set_fontsize(5)
        
        f3_ax4.scatter(VoidTimeList_Day2, VoidVolume_Day2)
        Day2Table = f3_ax6.table(cellText=Day2DF.values, colLabels=Day2DF.columns, loc='center')
        Day2Table.scale(1, 4)
        Day2Table.auto_set_font_size(False)
        Day2Table.set_fontsize(5)
        
        f3_ax7.scatter(VoidTimeList_Day3, VoidVolume_Day3)
        Day3Table = f3_ax9.table(cellText=Day3DF.values, colLabels=Day3DF.columns, loc='center')
        Day3Table.scale(1, 4)
        Day3Table.auto_set_font_size(False)
        Day3Table.set_fontsize(5)
        
        fig3.tight_layout()

        plt.savefig('./Styles/Patient.png')

class PatientReport(Screen):
    PatientReportGenerator().GenerateFigure()
    pass
        