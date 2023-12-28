import datetime
import time

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

data_temp=[]
data_hum=[]

# Format the date and time

# User ID
user_id = "cUgRiGk3v1Yfi59j0eOlNrK7gnn1"
print(user_id)


def continuously_check_time(user_id, db):
    while True:
        # Get the current time
        now = datetime.datetime.now()
        minutes = int(now.strftime("%M"))
        hours = int(now.strftime("%H"))
        days = int(now.strftime("%d"))
        month  = int(now.strftime("%m"))
        year = int(now.strftime("%Y"))
        if month == 1:
            process_data_year (year, user_id, db)
        if days == 0:
            process_data_month (month, year, user_id, db)
        if hours == 0:
            process_data_days (days, hours, user_id, db,month,year)
        if minutes == 0:
            process_data_hours (minutes, hours, user_id, device, db,days,month,year)
        formatted_now = str (days).zfill (2) + "-" + str (month).zfill (2) + "-" + str (year) + " - " + str (
            hours).zfill (2) + "-" + str (minutes).zfill (2)
        print(formatted_now)
        # Sleep for 60 seconds
        time.sleep(60)

def process_data_year( year, user_id, db):
    data_temp = []
    data_hum = []
    print ("year: ", year)
    if (year > 0):
        year = year - 1
    year=2023
    print ("year: ", year)
    for month in range(1, 13):
        formatted_now = str(month).zfill(2) + "-" + str(year)
        path_temp = user_id + "/Average per month/Living Room/" + formatted_now + "/temperature"
        path_hum = user_id + "/Average per month/Living Room/" + formatted_now + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())
        print (month,data_temp)

    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    proccesd_data_temp_average = round(raw_data_temp_average, 1)
    proccesd_data_hum_average = round(raw_data_hum_average, 1)
    print(proccesd_data_temp_average)
    # Save the average temperature to Firebase
    path_temp_average = user_id + "/Average per year" + "/Living Room/" + str(year) + "/temperature"
    path_hum_average = user_id + "/Average per year" + "/Living Room/" + str(year) + "/humidity"
    print(path_hum_average)

    db.reference(path_temp_average).set(proccesd_data_temp_average)
    db.reference(path_hum_average).set(proccesd_data_hum_average)
    print("proccesd_data_temp_average per year: ", proccesd_data_temp_average)
    print("proccesd_data_hum_average per year: ", proccesd_data_hum_average)


def process_data_month(month, year, user_id, db):
    data_temp = []
    data_hum = []
    print ("month: ", month)
    if (month > 0):
        month = month - 1
    elif (month == 12):
        month = 1
    print ("year: ", year)
    month = 12
    # Assuming each month has 30 days
    for day in range(1, 31):
        formatted_now = str(day).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year)
        path_temp = user_id + "/Average per day/Living Room/" + formatted_now + "/temperature"
        path_hum = user_id + "/Average per day/Living Room/" + formatted_now + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())
        print (day,data_temp)

    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    proccesd_data_temp_average = round(raw_data_temp_average, 1)
    proccesd_data_hum_average = round(raw_data_hum_average, 1)
    print(proccesd_data_temp_average)
    # Save the average temperature to Firebase
    formatted_now = str(month).zfill(2) + "-" + str(year)
    path_temp_average = user_id + "/Average per month" + "/Living Room/" + formatted_now + "/temperature"
    path_hum_average = user_id + "/Average per month" + "/Living Room/" + formatted_now + "/humidity"
    db.reference(path_temp_average).set(proccesd_data_temp_average)
    db.reference(path_hum_average).set(proccesd_data_hum_average)

    print("proccesd_data_temp_average per month: ", proccesd_data_temp_average)
    print("proccesd_data_hum_average per month: ", proccesd_data_hum_average)


def process_data_days(days, hours, user_id, db,month,year):
    print ("hours: ", hours)
    if (days > 0):
        days = days - 1
    print ("days: ", days)

    data_temp = []
    data_hum = []

    while (hours < 24):
        print (hours)
        formatted_now =  "-" +str (month).zfill (2) + "-" + str (year)
        path_temp = user_id + "/Average per hour/Living Room/" + str (days).zfill (2)+formatted_now + " - " + str (hours).zfill (
            2)  + "/temperature"
        path_hum = user_id + "/Average per hour/Living Room/" + str (days).zfill (2)+formatted_now + " - " + str (hours).zfill (
            2)  + "/humidity"
        print (path_temp)
        data_temp.append (db.reference (path_temp).get ())
        data_hum.append (db.reference (path_hum).get ())

        hours = hours + 1
    print (data_temp)
    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum (x for x in data_temp if x is not None) / len (data_temp)
    raw_data_hum_average = sum (x for x in data_hum if x is not None) / len (data_hum)
    proccesd_data_temp_average = round (raw_data_temp_average, 1)
    proccesd_data_hum_average = round (raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    formatted_now = str (days).zfill (2) + "-" + str (month).zfill (2) + "-" + str (year)
    path_temp_average = user_id + "/Average per day" + "/Living Room/" + formatted_now + "/temperature"
    path_hum_average = user_id + "/Average per day" + "/Living Room/" + formatted_now  + "/humidity"
    db.reference (path_temp_average).set (proccesd_data_temp_average)
    db.reference (path_hum_average).set (proccesd_data_hum_average)

    print("proccesd_data_temp_average per day: ",proccesd_data_temp_average)
    print("proccesd_data_hum_average per day: ",proccesd_data_hum_average)

def process_data_hours(minutes, hours, user_id, device, db,days,month,year):
    print ("minutes: ", minutes)
    if (hours > 0):
        hours = hours - 1
    print ("hours: ", hours)

    data_temp = []
    data_hum = []
    while (minutes < 60):
        print (minutes)
        formatted_now = str (days).zfill (2) + "-" + str (month).zfill (2) + "-" + str (year) + " - " + str (
            hours).zfill (2) + "-" + str (minutes).zfill (2)
        path_temp = user_id + "/Living Room/" + formatted_now + "/" + device + "/temperature"
        path_hum = user_id + "/Living Room/" + formatted_now + "/" + device + "/humidity"
        print (path_temp)
        data_temp.append (db.reference (path_temp).get ())
        data_hum.append (db.reference (path_hum).get ())

        minutes = minutes + 1
    print (data_temp)
    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum (x for x in data_temp if x is not None) / len (data_temp)
    raw_data_hum_average = sum (x for x in data_hum if x is not None) / len (data_hum)
    proccesd_data_temp_average = round (raw_data_temp_average, 1)
    proccesd_data_hum_average = round (raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    formatted_now = str (days).zfill (2) + "-" + str (month).zfill (2) + "-" + str (year) + " - " + str (
        hours).zfill (2)
    path_temp_average = user_id + "/Average per hour" + "/Living Room/" + formatted_now +"/temperature"
    path_hum_average = user_id + "/Average per hour" + "/Living Room/" + formatted_now + "/humidity"
    db.reference (path_temp_average).set (proccesd_data_temp_average)
    db.reference (path_hum_average).set (proccesd_data_hum_average)

    print("proccesd_data_temp_average per hour: ",proccesd_data_temp_average)
    print("proccesd_data_hum_average per hour: ",proccesd_data_hum_average)

continuously_check_time(user_id, db)
