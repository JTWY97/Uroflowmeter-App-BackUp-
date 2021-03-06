from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
import certifi

# KivyMD imports
from kivymd.toast import toast

# Python imports
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
import os.path

# Load the kv files
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/LogInScreen_Doctor.kv")
Builder.load_file(folder + "/LogInScreen_Patient.kv")
Builder.load_file(folder + "/Welcome_Screen.kv")
Builder.load_file(folder + "/LogInCombined.kv")
Builder.load_file(folder + "/loadingpopup.kv")

# Import the screens used to log the user in
from Welcome_Screen import WelcomeScreen
from LogInScreen_Doctor import LogIn_Doctor
from LogInScreen_Patient import LogIn_Patient

class FirebaseLoginScreen(Screen, EventDispatcher):
    """Use this widget as a complete module to incorporate Firebase user
    authentication in your app. To use this module, instantiate the login screen
    in the KV language like so:
    FirebaseLoginScreen:
        web_api_key: "your_firebase_web_api_key"
        debug: True # Not necessary, but will print out debug information
        on_login_success:
            # do something here
    NOTES:
    1) You MUST set the web api key or it is impossible for the login screen to
    function properly.
    2) You probably want to wrap the firebaseloginscreen in a ScreenManager.
    3) You probably want to switch screens to a Screen in your project once the
    user has logged in (write that code in the on_login_success function shown
    in the example above).
    """

    # Firebase Project meta info - MUST BE CONFIGURED BY DEVELOPER
    web_api_key = StringProperty()  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    refresh_token = ""
    localId = ""
    idToken = ""

    # Properties used to send events to update some parts of the UI
    login_success = BooleanProperty(False)  # Called upon successful sign in
    login_state = StringProperty("")
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)
    remember_user = BooleanProperty(True)

    debug = False
    # popup = Factory.LoadingPopup()
    # popup.background = folder + "/transparent_image.png"

    # def log_out(self):
    #     '''Clear the user's refresh token, marked them as not signed in, and
    #     go back to the welcome screen.
    #     '''
    #     with open(self.refresh_token_file, 'w') as f:
    #         f.write('')
    #     self.login_state = 'out'
    #     self.login_success = False
    #     self.refresh_token = ''
    #     self.ids.screen_manager.current = 'Welcome_Screen'
    #     # Clear text fields
    #     self.ids.sign_in_screen.ids.email.text = '' #
    #     self.ids.sign_in_screen.ids.password.text = '' #
    #     self.ids.sign_up_screen.ids.email.text = '' #
    #     self.ids.sign_up_screen.ids.password.text = '' #


    def on_login_success(self, screen_name, login_success_boolean):
        """Overwrite this method to switch to your app's home screen.
        """
        print("Testing", self.login_success, self.login_state)
        print("self.login_success=", login_success_boolean)

    def on_web_api_key(self, *args):
        """When the web api key is set, look for an existing account in local
        memory.
        """
        # Try to load the users info if they've already created an account
        self.refresh_token_file = App.get_running_app().user_data_dir + "/refresh_token.txt"
        if self.debug:
            print("Looking for a refresh token in:", self.refresh_token_file)
        if self.remember_user:
            print("REMEMBER USER IS TRUE")
            if os.path.exists(self.refresh_token_file):
                self.load_saved_account()

    def sign_in_success(self, urlrequest, log_in_data):
        """Collects info from Firebase upon successfully registering a new user.
        """
        if self.debug:
            print("Successfully signed in a user: ", log_in_data)
        # User's email/password exist, but are they verified?
        # self.hide_loading_screen()
        self.refresh_token = log_in_data['refreshToken']
        self.localId = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        self.save_refresh_token(self.refresh_token)

        self.login_state = 'in'
        self.login_success = True

    def sign_in(self, email, password):
        """Called when the "Log in" button is pressed.
        Sends the user's email and password in an HTTP request to the Firebase
        Authentication service.
        """
        if self.debug:
            print("Attempting to sign user in: ", email, password)
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.sign_in_success,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def sign_in_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to create an
        account was invalid.
        """
        self.hide_loading_screen()
        # self.email_not_found = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        toast(msg)
        if msg == "Email not found":
            self.email_not_found = True
        if self.debug:
            print("Couldn't sign the user in: ", failure_data)

    def sign_in_error(self, *args):
        # self.hide_loading_screen()
        if self.debug:
            print("Sign in error", args)

    def save_refresh_token(self, refresh_token):
        """Saves the refresh token in a local file to enable automatic sign in
        next time the app is opened.
        """
        if self.debug:
            print("Saving the refresh token to file: ", self.refresh_token_file)
        with open(self.refresh_token_file, "w") as f:
            f.write(refresh_token)

    def load_refresh_token(self):
        """Reads the refresh token from local storage.
        """
        if self.debug:
            print("Loading refresh token from file: ", self.refresh_token_file)
        with open(self.refresh_token_file, "r") as f:
            self.refresh_token = f.read()

    def load_saved_account(self):
        """Uses the refresh token to get the user's idToken and localId by
        sending it as a request to Google/Firebase's REST API.
        Called immediately when a web_api_key is set and if the refresh token
        file exists.
        """
        if self.debug:
            print("Attempting to log in a user automatically using a refresh token.")
        self.load_refresh_token()
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.web_api_key
        refresh_payload = dumps({"grant_type": "refresh_token", "refresh_token": self.refresh_token})
        UrlRequest(refresh_url, req_body=refresh_payload,
                   on_success=self.successful_account_load,
                   on_failure=self.failed_account_load,
                   on_error=self.failed_account_load, ca_file=certifi.where())

    def successful_account_load(self, urlrequest, loaded_data):
        """Sets the idToken and localId variables upon successfully loading an
        account using the refresh token.
        """
        # self.hide_loading_screen()
        if self.debug:
            print("Successfully logged a user in automatically using the refresh token")
        self.idToken = loaded_data['id_token']
        self.localId = loaded_data['user_id']
        self.login_state = 'in'
        self.login_success = True

    def failed_account_load(self, *args):
        # self.hide_loading_screen()
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

