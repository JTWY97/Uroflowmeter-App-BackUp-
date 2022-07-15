from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton,MDIconButton


class MainApp(MDApp):
    def build(self):
        return Builder.load_file('main.kv')


MainApp().run()