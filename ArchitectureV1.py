# from kivy.app import App
# from kivy.uix.label import Label

#Every Kivy application needs to subclass App and override build(). This is where you’ll put your UI code or make calls to other functions that define your UI code.
# 11 Pages --
# --> Patient: Log In Page, Main Page, Sypmtoms Tracker, Bladder Diary, Fluid Intake, Quick Pee
# --> Doctor: Log In Page (Repeated), Doctor Sign Up Page, Main Page, Patient List, Patient Data Summary, Patient Sign Up Page

# class MainApp(App):
#     def build(self):
#         label = Label(text='Hello from Kivy',
#                       size_hint=(.5, .5),
#                       pos_hint={'center_x': .5, 'center_y': .5})

#         return label

# if __name__ == '__main__':
#     app = MainApp()
#     app.run()

from kivy.lang import Builder
from kivymd.app import MDApp


class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file('login.kv')
	def logger(self):
		self.root.ids.welcome_label.text = f'Sup {self.root.ids.user.text}!' #id: welcome_id

	def clear(self):
		self.root.ids.welcome_label.text = "WELCOME"		
		self.root.ids.user.text = ""
		self.root.ids.password.text = ""
	
MainApp().run()