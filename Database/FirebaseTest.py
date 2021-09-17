#this code shld be in all the py files which will communicate with firebase
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
db = firebase.database() #connect to firebase

# users = db.child("doctorUsers").get()
# print(users)
# print(users.val()) #
# od1 = json.dumps(users.val()) #to convert ordereddict to json
# print(type(od1)) #to check type 
# print(od1) #to check output data

def doctorSignUp(firstname, lastname, specialization, hospital, phonenumber):
        data = {"firstname": firstname, "lastname": lastname, "specialization": specialization, "hospital": hospital, "phonenumber": phonenumber}
        doctorName = "Dr " + lastname
        db.child("doctorUsers").child(doctorName).set(data) 

# #db.child("doctorUsers").child("doctorID").child("basicinfo")
# data = {"basicinfo": "MoreFields", "email": "Random@email.com", "password": "sensitive"}
# db.child("doctorUsers").child("Doctor77").set(data) 
# db.child("doctorUsers").child("Doctor88").set(data)
# db.child("doctorUsers").child("Doctor88").set(data)
# db.child("doctorUsers").child("Doctor110").set(data)