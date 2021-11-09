from kivymd.app import MDApp
from kivy.lang import Builder

class MainApp(MDApp):

    local_id_doctor = ""
    user_idToken_patient = ""
    local_id_patient = ""
    UserID_Patient = ""
    
    Builder.load_file("./Pages/WelcomePage.kv")
    Builder.load_file("./Pages/Patient_LogIn.kv")
    Builder.load_file("./Pages/NewUser_Patient.kv")
    Builder.load_file("./Pages/PatientHomePage.kv")
    Builder.load_file("./Pages/SymptomTracker.kv")
    Builder.load_file("./Pages/FluidIntake.kv")
    Builder.load_file("./Pages/BladderDiary.kv")

    def sign_out_patient(self):
        self.root.ids.Patient_LogIn.log_out()
        self.root.current = 'Patient_LogIn'

MainApp().run()