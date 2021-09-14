from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


class MenuScreen(Screen):
	pass


class ProfileScreen(Screen):
	pass


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))


class DemoApp(MDApp):

	def build(self):
		screen = Builder.load_file('screenhelper.kv')
		return screen


DemoApp().run()
