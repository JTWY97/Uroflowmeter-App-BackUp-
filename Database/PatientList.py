from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineAvatarListItem
from kivymd.uix.list import IconLeftWidget
from kivy.uix.scrollview import ScrollView
from collections import OrderedDict

import pyrebase
import json

config = {
  "apiKey": "AIzaSyBE439nHksT0x_MZ7gaD7rx3GwJh8VIBTM",
  "authDomain": "bg4102app.firebaseapp.com",
  "databaseURL": "https://bg4102app-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "bg4102app.appspot.com",
  ##"serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database() 


class PatientList(MDApp):

    def build(self):
        screen = Screen()

        #define scrollview function
        scroll = ScrollView() 
        
        #define the list
        list_view = MDList()

        #add scroll view into list
        scroll.add_widget(list_view)

        #defining items to be added into the list
        for i in range(0,len(patientnames)):
            icon = IconLeftWidget(icon="human")
            name = patientnames[i]
            
            startdate = []
            startdate.append(db.child("patientUsers").child(name).child("start").get().val())
            start = startdate[0]

            enddate = []
            enddate.append(db.child("patientUsers").child(name).child("end").get().val())
            end = enddate[0]

            items = ThreeLineAvatarListItem(
                text = name,
                secondary_text = "Start: " + start,
                tertiary_text = "End: " + end
                )

            items.add_widget(icon)


        
             #adding items into the list
            list_view.add_widget(items)
            i+=1

        #add scroll onto the screen
        screen.add_widget(scroll)
       
        return screen

#returns a list of objects under "patientUsers"
all_users = db.child("patientUsers").get()
patientnames = []
for x in all_users.each():
    print(x.key())
    patientnames.append(x.key())

od1 = json.dumps((all_users.key())) #to convert ordereddict to json
print(od1)

PatientList().run()