from kivy.uix.screenmanager import Screen
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, StringProperty
from kivy.network.urlrequest import UrlRequest
import certifi
from json import dumps

# KivyMD imports
from kivymd.toast import toast

from Database.FirebaseTest import doctorSignUp

class NewDoctor_SignUp(Screen, EventDispatcher):
    web_api_key = StringProperty()

    refresh_token = ""
    localId = ""
    idToken = ""

    login_success = BooleanProperty(False)
    login_state = StringProperty("")
    sign_up_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)
    remember_user = BooleanProperty(True)
    require_email_verification = BooleanProperty(False)

    debug = False

    def sign_up(self, email, password, firstname, lastname, specialization, hospital, phonenumber): 
        if self.debug:
            print("Attempting to create a new account: ", email, password)
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = dumps({"email": email, "password": password, "returnSecureToken": "true"})
        UrlRequest(signup_url, req_body=signup_payload,
                   on_success=self.successful_sign_up,
                   on_failure=self.sign_up_failure,
                   on_error=self.sign_up_error, ca_file=certifi.where())
        doctorSignUp(firstname, lastname, specialization, hospital, phonenumber, email) #call the firebase function

    def successful_sign_up(self, request, result):
        if self.debug:
            print("Successfully signed up a user: ", result)
        self.refresh_token = result['refreshToken']
        self.localId = result['localId']
        self.idToken = result['idToken']

        if self.require_email_verification:
            self.send_verification_email(result['email'])
            self.ids.screen_manager.current = 'sign_in_screen'

        else:
            self.login_state = 'in'
            self.login_success = True

    def sign_up_failure(self, urlrequest, failure_data):
        self.email_exists = False
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        toast(msg)
        if msg == "Email exists":
            self.email_exists = True
        if self.debug:
            print("Couldn't sign the user up: ", failure_data)

    def sign_up_error(self, *args):
        if self.debug:
            print("Sign up Error: ", args)
    pass