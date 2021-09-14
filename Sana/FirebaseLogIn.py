from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
import certifi

# KivyMD imports
from kivymd.toast import toast

# Python imports
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
import os.path

folder = os.path.dirname(os.path.realpath(__file__))

Builder.load_file("Patient_LogIn.kv")
Builder.load_file("Doctor_LogIn.kv")
Builder.load_file("WelcomePage.kv")
Builder.load_file("PatientHomePage.kv")
Builder.load_file("DoctorHomePage.kv")
Builder.load_file("FirebaseLogIn.kv")

# Import the screens used to log the user in
from WelcomePage import Welcome_Page
from Patient_LogIn import Patient_LogIn
from Doctor_LogIn import Doctor_LogIn
from PatientHomePage import PatientHomePage
from DoctorHomePage import DoctorHomePage

class Firebase_LoginScreen_Patient(Patient_LogIn, EventDispatcher):
	web_api_key = StringProperty("")
	refresh_token = ""
	localId = ""
	idToken = ""
	
	login_success = BooleanProperty(False)
	login_state = StringProperty("")
	email_exists = BooleanProperty(False)
	email_not_found = BooleanProperty(False)
	remember_user = BooleanProperty(True)
	debug = False
	
	def log_out(self):
		'''Clear the user's refresh token, marked them as not signed in, and
        go back to the welcome screen.
        '''
		with open(self.refresh_token_file, 'w') as f:
			f.write('')
		self.login_state = 'out'
		self.login_success = False
		self.refresh_token = ''
		self.ids.User_Patient.text = '' 
		self.ids.Password_Patient.text = ''

	def on_web_api_key(self, *args):
		self.refresh_token_file = MDApp.get_running_app().user_data_dir + "/refresh_token.txt"
		if self.debug:
			print("Looking for a refresh token in:", self.refresh_token_file)
		if self.remember_user:
			print("REMEMBER USER IS TRUE")
			if os.path.exists(self.refresh_token_file):
				self.load_saved_account()
				
	def sign_in_success(self, urlrequest, log_in_data):
		if self.debug:
			print("Successfully signed in a user: ", log_in_data)
			
		self.refresh_token = log_in_data['refreshToken']
		self.localId = log_in_data['localId']
		self.idToken = log_in_data['idToken']
		self.save_refresh_token(self.refresh_token)
		
		self.login_state = 'in'
		self.login_success = True
	
	def sign_in(self, email, password):
		if self.debug:
			print("Attempting to sign user in: ", email, password)
		sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
		sign_in_payload = dumps({"email": email, "password": password, "returnSecureToken": True})
		UrlRequest(sign_in_url, req_body=sign_in_payload,on_success=self.sign_in_success,on_failure=self.sign_in_failure,on_error=self.sign_in_error, ca_file=certifi.where())
		
	def sign_in_failure(self, urlrequest, failure_data):
		self.email_not_found = False  # Triggers hiding the sign in button
		msg = failure_data['error']['message'].replace("_", " ").capitalize()
		toast(msg)
		if msg == "Email not found":
			self.email_not_found = True
		if self.debug:
			print("Couldn't sign the user in: ", failure_data)
			
	def sign_in_error(self, *args):
		if self.debug:
			print("Sign in error", args)

	def save_refresh_token(self, refresh_token):
		if self.debug:
			print("Saving the refresh token to file: ", self.refresh_token_file)
		with open(self.refresh_token_file, "w") as f:
			f.write(refresh_token)
			
	def load_refresh_token(self):
		if self.debug:
			print("Loading refresh token from file: ", self.refresh_token_file)
		with open(self.refresh_token_file, "r") as f:
			self.refresh_token = f.read()
			
	def load_saved_account(self):
		if self.debug:
			print("Attempting to log in a user automatically using a refresh token.")
		self.load_refresh_token()
		refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
		refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
		UrlRequest(refresh_url, req_body=refresh_payload,on_success=self.successful_account_load,on_failure=self.failed_account_load,on_error=self.failed_account_load, ca_file=certifi.where())
		
	def successful_account_load(self, urlrequest, loaded_data):
		if self.debug:
			print("Successfully logged a user in automatically using the refresh token")
		self.idToken = loaded_data['id_token']
		self.localId = loaded_data['user_id']
		self.login_state = 'in'
		self.login_success = True
	
	def failed_account_load(self, *args):
		if self.debug:
			print("Failed to load an account.", args)

	def sign_out(self):
		self.localId = ''
		self.idToken = ''
		self.clear_refresh_token_file()
		self.ids.screen_manager.current = 'Welcome_Screen'
		toast("Signed out")
		
	def clear_refresh_token_file(self):
		with open(self.refresh_token_file, 'w') as f:
			f.write('')

	pass

class Firebase_LoginScreen_Doctor(Doctor_LogIn, EventDispatcher):
	web_api_key = StringProperty("")
	refresh_token = ""
	localId = ""
	idToken = ""
	
	login_success = BooleanProperty(False)
	login_state = StringProperty("")
	email_exists = BooleanProperty(False)
	email_not_found = BooleanProperty(False)
	remember_user = BooleanProperty(True)
	debug = False
	
	def log_out(self):
		'''Clear the user's refresh token, marked them as not signed in, and
        go back to the welcome screen.
        '''
		with open(self.refresh_token_file, 'w') as f:
			f.write('')
		self.login_state = 'out'
		self.login_success = False
		self.refresh_token = ''
		self.ids.User_Doctor.text = '' 
		self.ids.Password_Doctor.text = ''
		
	def on_login_success(self,  DoctorHomePage, login_success_boolean):
		print("Testing", self.login_success, self.login_state)
		print("self.login_success=", login_success_boolean)

	def on_web_api_key(self, *args):
		self.refresh_token_file = MDApp.get_running_app().user_data_dir + "/refresh_token.txt"
		if self.debug:
			print("Looking for a refresh token in:", self.refresh_token_file)
		if self.remember_user:
			print("REMEMBER USER IS TRUE")
			if os.path.exists(self.refresh_token_file):
				self.load_saved_account()
				
	def sign_in_success(self, urlrequest, log_in_data):
		if self.debug:
			print("Successfully signed in a user: ", log_in_data)
			
		self.refresh_token = log_in_data['refreshToken']
		self.localId = log_in_data['localId']
		self.idToken = log_in_data['idToken']
		self.save_refresh_token(self.refresh_token)
		
		self.login_state = 'in'
		self.login_success = True
	
	def sign_in(self, email, password):
		if self.debug:
			print("Attempting to sign user in: ", email, password)
		sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
		sign_in_payload = dumps({"email": email, "password": password, "returnSecureToken": True})
		UrlRequest(sign_in_url, req_body=sign_in_payload,on_success=self.sign_in_success,on_failure=self.sign_in_failure,on_error=self.sign_in_error, ca_file=certifi.where())
		
	def sign_in_failure(self, urlrequest, failure_data):
		self.email_not_found = False  # Triggers hiding the sign in button
		msg = failure_data['error']['message'].replace("_", " ").capitalize()
		toast(msg)
		if msg == "Email not found":
			self.email_not_found = True
		if self.debug:
			print("Couldn't sign the user in: ", failure_data)
			
	def sign_in_error(self, *args):
		if self.debug:
			print("Sign in error", args)

	def save_refresh_token(self, refresh_token):
		if self.debug:
			print("Saving the refresh token to file: ", self.refresh_token_file)
		with open(self.refresh_token_file, "w") as f:
			f.write(refresh_token)
			
	def load_refresh_token(self):
		if self.debug:
			print("Loading refresh token from file: ", self.refresh_token_file)
		with open(self.refresh_token_file, "r") as f:
			self.refresh_token = f.read()
			
	def load_saved_account(self):
		if self.debug:
			print("Attempting to log in a user automatically using a refresh token.")
		self.load_refresh_token()
		refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
		refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
		UrlRequest(refresh_url, req_body=refresh_payload,on_success=self.successful_account_load,on_failure=self.failed_account_load,on_error=self.failed_account_load, ca_file=certifi.where())
		
	def successful_account_load(self, urlrequest, loaded_data):
		if self.debug:
			print("Successfully logged a user in automatically using the refresh token")
		self.idToken = loaded_data['id_token']
		self.localId = loaded_data['user_id']
		self.login_state = 'in'
		self.login_success = True
	
	def failed_account_load(self, *args):
		if self.debug:
			print("Failed to load an account.", args)

	def sign_out(self):
		self.localId = ''
		self.idToken = ''
		self.clear_refresh_token_file()
		self.ids.screen_manager.current = 'Welcome_Screen'
		toast("Signed out")
		
	def clear_refresh_token_file(self):
		with open(self.refresh_token_file, 'w') as f:
			f.write('')

	pass

