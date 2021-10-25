from kivymd.app import MDApp
from kivy.lang import Builder

class MainApp(MDApp):
    user_idToken_doctor = ""
    local_id_doctor = ""
    user_idToken_patient = ""
    local_id_patient = ""
    UserID_Patient = ""
    UserID_Doctor = ""


    Builder.load_file("./Pages/Patient_LogIn.kv")
    Builder.load_file("./Pages/Doctor_LogIn.kv")
    Builder.load_file("./Pages/WelcomePage.kv")
    Builder.load_file("./Pages/PatientHomePage.kv")
    Builder.load_file("./Pages/DoctorHomePage.kv")
    Builder.load_file("./Pages/NewUser_Doctor.kv")
    Builder.load_file("./Pages/NewUser_Patient.kv")
    Builder.load_file("./Pages/SymptomTracker.kv")
    Builder.load_file("./Pages/FluidIntake.kv")
    Builder.load_file("./Pages/PatientList.kv")
    Builder.load_file("./Pages/BladderDiary.kv")

    def sign_out_doctor(self):
        self.root.ids.Doctor_LogIn.log_out()
        self.root.current = 'Doctor_LogIn'

    def sign_out_patient(self):
        self.root.ids.Patient_LogIn.log_out()
        self.root.current = 'Patient_LogIn'

    def BackToHomePage(self):
        self.root.current = 'PatientHomepage'

    def Summary(self):
        self.root.current = 'BladderDiarySummary'

MainApp().run()