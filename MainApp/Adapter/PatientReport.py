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
    
    def GetAllDayData(self, dayID):
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
            
        NoOfNocturiaEp = 0
        NoOfNormalEp = 0
        NoOfMorningEp = 0
        TotalVoidEp = 0

        NocturiaVoidVol = []
        MorningVoidVol = []
        NormalVoidVol = []
        print(len(VoidVolume))
        print(len(VoidType))
        for i in range(0, len(VoidType)):
            if VoidType[i] == "First Morning Episode":
                MorningVoidVol.append(VoidVolume[i])
                NoOfMorningEp += 1
                TotalVoidEp += 1
            elif VoidType[i] == "Normal Episode":
                NormalVoidVol.append(VoidVolume[i])
                NoOfNormalEp += 1
                TotalVoidEp += 1
            elif VoidType[i] == "Nocturia Episode":
                NocturiaVoidVol.append(VoidVolume[i])
                NoOfNocturiaEp += 1
                TotalVoidEp += 1
        DayTimeFrequencyRange = len(NormalVoidVol)
        UsualDayTimeFrequency = len(NormalVoidVol)
        MaximalVoidedVolume = max(VoidVolume)
        NormalVoidVol = np.array(NormalVoidVol).astype(float)
        DayTimeVoidedVolumerange = max(NormalVoidVol) - min(NormalVoidVol)

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
        
        VoidQMax = np.array(VoidQMax).astype(float)
        if len(VoidQMax) != 0:
            QmaxRange = max(VoidQMax) - min(VoidQMax)
        else:
            QmaxRange = 0
        
        return DayTimeFrequencyRange, UsualDayTimeFrequency, MaximalVoidedVolume, DayTimeVoidedVolumerange, DayTimeVoidedVolumerange, QmaxRange
        
    
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
        TotalVoidEp = 0

        NocturiaVoidVol = []
        MorningVoidVol = []
        NormalVoidVol = []
        print(len(VoidVolume))
        print(len(VoidType))
        for i in range(0, len(VoidType)):
            if VoidType[i] == "First Morning Episode":
                MorningVoidVol.append(VoidVolume[i])
                NoOfMorningEp += 1
                TotalVoidEp += 1
            elif VoidType[i] == "Normal Episode":
                NormalVoidVol.append(VoidVolume[i])
                NoOfNormalEp += 1
                TotalVoidEp += 1
            elif VoidType[i] == "Nocturia Episode":
                NocturiaVoidVol.append(VoidVolume[i])
                NoOfNocturiaEp += 1
                TotalVoidEp += 1
        
        TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent= self.DailyReportData(FluidIntake, VoidVolume, NoOfNocturiaEp, NocturiaVoidVol, MorningVoidVol, TotalVoidEp)
        return TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent
    
    def DailyReportData(self, FluidIntake, VoidVolume, NoOfNocturiaEp, NocturiaVoidVol, MorningVoidVol, TotalVoidEp):
        
        TotalInput = FluidIntake
        VoidVolume = np.array(VoidVolume).astype(float)
        TotalOutput = np.sum(VoidVolume)
        NocturiaNumber = NoOfNocturiaEp
        TotalVoidNumber = TotalVoidEp
        NocturiaVoidVol = np.array(NocturiaVoidVol).astype(float)
        MorningVoidVol = np.array(MorningVoidVol).astype(float)
        NocturiaVoidVol = np.sum(NocturiaVoidVol) + np.sum(MorningVoidVol)

        if TotalVoidNumber != 0:
            NPI = (NocturiaNumber/TotalVoidNumber)*100
        else:
            NPI = "Not logged yet."

        if NocturiaNumber != 0:
            NcoturiaPresent = "Yes"
        else:
            NcoturiaPresent = "No"
        
        return TotalInput, TotalOutput, NocturiaNumber, NPI, NcoturiaPresent
    
        
    def CollData(self):
        DayTimeFrequencyRange1, UsualDayTimeFrequency1, MaximalVoidedVolume1, DayTimeVoidedVolumerange1, DayTimeVoidedVolumerange1, QmaxRange1 = self.GetAllDayData("day 1")
        DayTimeFrequencyRange2, UsualDayTimeFrequency2, MaximalVoidedVolume2, DayTimeVoidedVolumerange2, DayTimeVoidedVolumerange2, QmaxRange2 = self.GetAllDayData("day 2")
        DayTimeFrequencyRange3, UsualDayTimeFrequency3, MaximalVoidedVolume3, DayTimeVoidedVolumerange3, DayTimeVoidedVolumerange3, QmaxRange3 = self.GetAllDayData("day 3")
        x = []
        x.append(UsualDayTimeFrequency1)
        x.append(UsualDayTimeFrequency2)
        x.append(UsualDayTimeFrequency3)
        DayTimeFrequencyRange = (int(DayTimeFrequencyRange1) + int(DayTimeFrequencyRange2)+ int(DayTimeFrequencyRange3))/3
        UsualDayTimeFrequency = np.std(x)
        MaximalVoidedVolume = (float(MaximalVoidedVolume1) + float(MaximalVoidedVolume2) + float(MaximalVoidedVolume3))/3
        DayTimeVoidedVolumerange = (DayTimeVoidedVolumerange1 + DayTimeVoidedVolumerange2 + DayTimeVoidedVolumerange3)/3
        QmaxRange = (QmaxRange1+ QmaxRange2+QmaxRange3)
        Summarydata = []
        a1 = []
        a2 = []
        a3 = []
        a4 = []
        a5 = []
        a1.append(str(DayTimeFrequencyRange)[:5])
        a2.append(str(UsualDayTimeFrequency)[:5])
        a3.append(str(MaximalVoidedVolume)[:5])
        a4.append(str(DayTimeVoidedVolumerange)[:5])
        a5.append(str(QmaxRange)[:5])
        Summarydata.append(a1)
        Summarydata.append(a2)
        Summarydata.append(a3)
        Summarydata.append(a4)
        Summarydata.append(a5)
        
        return Summarydata
        
        
    
    def CollectingData(self):
        
        TotalInput_Day1, TotalOutput_Day1, NocturiaNumber_Day1, NPI_Day1, NocturiaPresent_Day1 = self.GetVoidData("day 1", "DailyTable")
        TotalInput_Day2, TotalOutput_Day2, NocturiaNumber_Day2, NPI_Day2, NocturiaPresent_Day2 = self.GetVoidData("day 2", "DailyTable")
        TotalInput_Day3, TotalOutput_Day3, NocturiaNumber_Day3, NPI_Day3, NocturiaPresent_Day3 = self.GetVoidData("day 3", "DailyTable")
        
        TotalInput = []
        TotalInput.append(TotalInput_Day1)
        if TotalInput_Day2 != None:
            TotalInput.append(TotalInput_Day2)
        else:
            TotalInput.append(0)
        if TotalInput_Day3 != None:
            TotalInput.append(TotalInput_Day3)
        else:
            TotalInput.append(0)

        TotalOutput = []
        TotalOutput.append(TotalOutput_Day1)
        TotalOutput.append(TotalOutput_Day2)
        TotalOutput.append(TotalOutput_Day3)
        
        NocNum = []
        NocNum.append(NocturiaNumber_Day1)
        NocNum.append(NocturiaNumber_Day2)
        NocNum.append(NocturiaNumber_Day3)
        
        NPI = []
        NPI.append(str(NPI_Day1)[:4])
        NPI.append(str(NPI_Day2)[:4])
        NPI.append(str(NPI_Day3)[:4])
        
        Noc = []
        Noc.append(NocturiaPresent_Day1)
        Noc.append(NocturiaPresent_Day2)
        Noc.append(NocturiaPresent_Day3)

        AllDays = []
        AllDays.append(TotalInput)
        AllDays.append(TotalOutput)
        AllDays.append(NocNum)
        AllDays.append(NPI)
        AllDays.append(Noc)
        

        #Daily Graph Data
        
        VoidVolume_Day1, VoidTimeList_Day1 = self.GetVoidData("day 1", "DailyGraph")
        VoidVolume_Day1 = np.array(VoidVolume_Day1).astype(float)
        VoidVolume_Day2, VoidTimeList_Day2 = self.GetVoidData("day 2", "DailyGraph")
        VoidVolume_Day2 = np.array(VoidVolume_Day2).astype(float)
        VoidVolume_Day3, VoidTimeList_Day3 = self.GetVoidData("day 3", "DailyGraph")
        VoidVolume_Day3 = np.array(VoidVolume_Day3).astype(float)
        
        
        
        return AllDays, VoidVolume_Day1, VoidTimeList_Day1, VoidVolume_Day2, VoidTimeList_Day2, VoidVolume_Day3, VoidTimeList_Day3
        
    def GenerateFigure(self):
        AllDays, VoidVolume_Day1, VoidTimeList_Day1, VoidVolume_Day2, VoidTimeList_Day2, VoidVolume_Day3, VoidTimeList_Day3 = self.CollectingData()
        FVCSummaryData= self.CollData()

        fig3 = plt.figure(constrained_layout=True, figsize= [10,8])
        gs = fig3.add_gridspec(4, 4)
        
        ax1 = fig3.add_subplot(gs[0, :])
        ax1.set_axis_off()

        ax2 = fig3.add_subplot(gs[1, :])
        ax2.set_axis_off()

        ax3 = fig3.add_subplot(gs[2, :])
        ax3.set_title('Usual Daytime Freq', fontweight= "bold")

        ax4 = fig3.add_subplot(gs[3, :])
        ax4.set_title('Voided Volume/Day', fontweight= "bold")
        
        #Daily FVC Table
        Columns1 = ('Day 1', 'Day 2', 'Day 3')
        Rows1 = ('Total Input (ml)', 'Total Output (ml)', 'Nocturia Episode Count', 'NPI (%)', 'Nocturnal Polyuria')
        ccolors = plt.cm.BuPu(np.full(len(Columns1), 0.1))
        rcolors = plt.cm.BuPu(np.full(len(Rows1), 0.1))
        DailySummaryTable = ax1.table(cellText=AllDays, colLabels=Columns1, rowLabels = Rows1, loc='center', colColours = ccolors, rowColours = rcolors)
        ax1.set_title('Daily FVC Data', fontweight = "bold")

        #Overall Stats Table 
        Rows1 = ('Day Time Frequency Range', 'Usual Daytime Frequency', 'Maximal Voided Volume (MVV) (ml)', 'Usual Daytime Voided Volume (ml)', 'Q Max Range')
        rcolors = plt.cm.BuPu(np.full(len(Rows1), 0.1))
        OverallFVCTable = ax2.table(cellText=FVCSummaryData, rowLabels = Rows1, loc='center', colColours = ccolors, rowColours = rcolors)
        ax2.set_title('Summary FVC Data', fontweight = "bold")

        #Usual Daytime Freq scatterplot


        fig3.tight_layout()
        plt.show()
        # plt.savefig('./Styles/Patient.png')

# class PatientReport(Screen):
PatientReportGenerator().GenerateFigure()
    # pass