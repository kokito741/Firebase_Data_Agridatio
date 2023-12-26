import datetime
import firebase_admin
from firebase_admin import auth, credentials, db

# Firebase configuration
config = {
    "apiKey": "AIzaSyBU7Tn2EOD03z5eOseQ2rbKoBzbS3waS9w",
    "authDomain": "esp32-dd238.firebaseapp.com",
    "databaseURL": "https://esp32-dd238-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "esp32-dd238",
    "appId": "1:368211157112:web:95523c257dbb917f43cd8d",
    "storageBucket": "esp32-dd238.appspot.com",
    "measurementId": "G-W1GWQN28P6"
}

device="esp32-dev-1"
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://esp32-dd238-default-rtdb.europe-west1.firebasedatabase.app/'
})

# uid should be the id of the user you want to grant admin privileges to
uid = "vN8iEemQ50UZ8SA6RR7I3FFdgfp2"

# Add custom claims for additional privileges.
# This will set the `admin` claim to `True` for this user.
auth.set_custom_user_claims(uid, {'admin': True})

# Log the user in
email = "kokito741@gmail.com"  # replace with the user's email
password = "987456321kK"  # replace with the user's password
user = auth.get_user_by_email(email)
print(user)

# Get a reference to the database service
db = firebase_admin.db

# Get the current date and time
now = datetime.datetime.now()
minutes = int(now.strftime("%M"))
hours = int(now.strftime("%H"))
print(minutes)
data_temp=[]
data_hum=[]

# Format the date and time
formatted_now = now.strftime("%d-%m-%Y - ")
print(f"Current date and time: {formatted_now}")

# User ID
user_id = "cUgRiGk3v1Yfi59j0eOlNrK7gnn1"
print(user_id)
print(type(formatted_now))


# Get temperature date
minutes=00
# Check if data exists
if minutes == 0:
    print("minutes: ", minutes)
    if(hours>0):
        hours = hours - 1
    print("hours: ", hours)

    while(minutes<60):
        print(minutes)
        path_temp = user_id + "/Living Room/" + formatted_now + str(hours).zfill(2) + "-"+ str(minutes).zfill(2) + "/" + device + "/temperature"
        path_hum = user_id + "/Living Room/" + formatted_now + str(hours).zfill(2) + "-"+ str(minutes).zfill(2) + "/" + device + "/humidity"
        print(path_temp)
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())

        minutes=minutes+1
    print(data_temp)
    raw_data_temp_average=sum(data_temp)/len(data_temp)
    raw_data_hum_average=sum(data_hum)/len(data_hum)
    proccesd_data_temp_average=round(raw_data_temp_average,1)
    proccesd_data_hum_average=round(raw_data_hum_average,1)
    # Save the average temperature to Firebase
    path_temp_average = user_id +"/Average per hour"+"/Living Room/" + formatted_now + str (hours).zfill (2)  + "/temperature"
    path_hum_average = user_id +"/Average per hour"+ "/Living Room/" + formatted_now + str (hours).zfill (2)  + "/humidity"
    db.reference(path_temp_average).set(proccesd_data_temp_average)
    db.reference(path_hum_average).set(proccesd_data_hum_average)
#todo add for hours,days,mounts,years and make it continuesly check the time
