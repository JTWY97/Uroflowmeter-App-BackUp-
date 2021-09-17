from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.picker import MDDatePicker

class SymptomTracker(Screen):
    date = []
    def on_save(self, instance, value, date_range):
        self.date.append(str(value))
        self.ids.date_label.text = str(self.date[-1])
        
    def on_cancel(self, instance, value):
        self.ids.date_label.text = "You Clicked Cancel"
    
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()