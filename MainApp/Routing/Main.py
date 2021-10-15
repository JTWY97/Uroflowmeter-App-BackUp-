from kivymd.app import MDApp
from kivy.lang import Builder
import os

class MainApp(MDApp):
    user_idToken_doctor = ""
    local_id_doctor = ""
    user_idToken_patient = ""
    local_id_patient = ""
    UserID_Patient = ""
    UserID_Doctor = ""

    path = os.getcwd()
    path = path + "/MobileApplicationForUroflowometer/MainApp/"

    Builder.load_file(path + "Pages/Patient_LogIn.kv")
    Builder.load_file(path + "Pages/Doctor_LogIn.kv")
    Builder.load_file(path + "Pages/WelcomePage.kv")
    Builder.load_file(path + "Pages/PatientHomePage.kv")
    Builder.load_file(path + "Pages/DoctorHomePage.kv")
    Builder.load_file(path + "Pages/NewUser_Doctor.kv")
    Builder.load_file(path + "Pages/NewUser_Patient.kv")
    Builder.load_file(path + "Pages/SymptomTracker.kv")
    Builder.load_file(path + "Pages/FluidIntake.kv")
    Builder.load_file(path + "Pages/PatientList.kv")
    Builder.load_file(path + "Pages/BladderDiary.kv")

    def sign_out_doctor(self):
        self.root.ids.Doctor_LogIn.log_out()
        self.root.current = 'Doctor_LogIn'

    def sign_out_patient(self):
        self.root.ids.Patient_LogIn.log_out()
        self.root.current = 'Patient_LogIn'

MainApp().run()