from kivymd.app import MDApp

class MainApp(MDApp):
    user_idToken = ""
    local_id = ""
	
    def sign_out_doctor(self):
        self.root.ids.firebase_login_screen_doctor.log_out()
        self.root.current = 'firebase_login_screen_doctor'

    def sign_out_patient(self):
        self.root.ids.firebase_login_screen_patient.log_out()
        self.root.current = 'firebase_login_screen_patient'
		
MainApp().run()