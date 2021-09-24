from kivymd.app import MDApp
from kivy.lang import Builder

class MainApp(MDApp):
    user_idToken_doctor = ""
    local_id_doctor = ""
    user_idToken_patient = ""
    local_id_patient = ""
    useriD = ""

    Builder.load_file("Patient_LogIn.kv")
    Builder.load_file("Doctor_LogIn.kv")
    Builder.load_file("WelcomePage.kv")
    Builder.load_file("PatientHomePage.kv")
    Builder.load_file("DoctorHomePage.kv")
    Builder.load_file("NewUser_Doctor.kv")
    Builder.load_file("NewUser_Patient.kv")
    Builder.load_file("SymptomTracker.kv")
    Builder.load_file("FluidIntake.kv")
    Builder.load_file("BladderDiary.kv")
    Builder.load_file("PatientList.kv")

    def sign_out_doctor(self):
        self.root.ids.Doctor_LogIn.log_out()
        self.root.current = 'Doctor_LogIn'

    def sign_out_patient(self):
        self.root.ids.Patient_LogIn.log_out()
        self.root.current = 'Patient_LogIn'

    def launch_patientlist(self):
        self.root.ids.PatientList.build()
        self.root.current = 'PatientList'

MainApp().run()