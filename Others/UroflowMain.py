from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.picker import MDDatePicker

class MainPage(Screen):
    pass

class SymptomTracker(Screen):
    pass

class BladderDiary(Screen):
    pass

class FluidIntake(Screen):
    pass

#class MainApp(MDApp):
class HomePagePatient(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"
		return Builder.load_file("UroflowMain.kv")


    #Click OK
	date = []
	def on_save(self, instance, value, date_range):
		self.date.append(str(value))
		self.root.ids.date_label.text = str(self.date[-1])

# syptom tracker
# array1 = [1, 2, 1, 3] #dates
# arraya = [[1, 2, 3], [4, 5], [2, 2, 3], [4]]

# arrayday1 = [array1[0] + arraya[0] + arraya[2]]
# arrayday2 = [array1[1] + arraya[1]]
# arrayday3 = [array1[3] + arraya[3]]

# symptomLegend = {'PainWhileUrinating': 1, 'Dizziness': 2}

# syp = []
# 	def Choose_Color():
# 		for Symptom,Index in symptomLegend.items():
# 			for i in len(arrayday1):
# 				if Index == arrayday1[i]:
# 					syp.append(Index)
# 					i +=1 
# 				else:
# 					syp.append(arrayday1[i])
# 					i +=1

#fluid
# array1 = [1, 2, 1, 3] #dates
# arraya = [[1, 2, 3], [4, 5], [2, 2, 3], [4]]

# arrayday1 = [array1[0] + arraya[0] + arraya[2]]
# arrayday2 = [array1[1] + arraya[1]]
# arrayday3 = [array1[3] + arraya[3]]

	# def TotalFluid():
	# 	i = 1
	# 	for i in len(arrayday1):
	# 		totalvol = arrayday1[1:].sum
	# 		return totalvol


	#Click Cancel
	def on_cancel(self, instance, value):
		self.root.ids.date_label.text = "You Clicked Cancel"

	def show_date_picker(self):
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
		date_dialog.open()

HomePagePatient().run()