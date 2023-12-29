import time
from typing import Any
import calendar
import firebase_admin
from firebase_admin import auth, credentials, db
from datetime import datetime, timedelta

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

device = "esp32-dev-1"
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://esp32-dd238-default-rtdb.europe-west1.firebasedatabase.app/'
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

# Format the date and time

# User ID
user_id = "cUgRiGk3v1Yfi59j0eOlNrK7gnn1"

def continuously_check_time(user_id, db):
    """

    :type db: object
    :type user_id: object
    :param user_id: 
    :param db: 
    """
    while True:
        # Get the current time
        now = datetime.now()
        minutes = int(now.strftime("%M"))
        hours = int(now.strftime("%H"))
        days = int(now.strftime("%d"))
        month = int(now.strftime("%m"))
        year = int(now.strftime("%Y"))
        formatted_now = str(days).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + " - " + str(
            hours).zfill(2) + "-" + str(minutes).zfill(2)
        print(formatted_now)
        if month == 1:
            process_data_year(year, user_id, db)
        if days == 1:
            process_data_month(user_id, db)
        if hours == 0:
            process_data_days(hours, user_id, db, month, year)
        if minutes == 0:
            process_data_hours(minutes, hours, user_id, device, db, days, month, year)

        # Sleep for 60 seconds
        time.sleep(60)


def process_data_year(year, user_id, db):
    """

    :type db: object
    :type user_id: object
    :param year: 
    :param user_id: 
    :param db: 
    """
    data_temp = []
    data_hum = []
    year -= 1
    for month in range(1, 13):
        formatted_now = str(month).zfill(2) + "-" + str(year)
        path_temp = user_id + "/Average per month/Living Room/" + formatted_now + "/temperature"
        path_hum = user_id + "/Average per month/Living Room/" + formatted_now + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())

    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    processed_data_temp_average = round(raw_data_temp_average, 1)
    processed_data_hum_average = round(raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    path_temp_average = user_id + "/Average per year" + "/Living Room/" + str(year) + "/temperature"
    path_hum_average = user_id + "/Average per year" + "/Living Room/" + str(year) + "/humidity"

    db.reference(path_temp_average).set(processed_data_temp_average)
    db.reference(path_hum_average).set(processed_data_hum_average)
    print("processed_data_temp_average per year: ", processed_data_temp_average)
    print("processed_data_hum_average per year: ", processed_data_hum_average)


def process_data_month(user_id, db):
    """

    :type db: object
    :type user_id: object
    :param user_id:
    :param db:
    """
    data_temp = []
    data_hum = []
    # Get the date 4 weeks ago
    date_four_weeks_ago = datetime.today() - timedelta(weeks=5)

    # Get the year and month of the date 5 weeks ago
    year, month = date_four_weeks_ago.year, date_four_weeks_ago.month

    # Get the last day of that month
    _, last_day = calendar.monthrange(year, month)
    for day in range(1, last_day + 1):
        formatted_now = str(day).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year)
        path_temp = user_id + "/Average per day/Living Room/" + formatted_now + "/temperature"
        path_hum = user_id + "/Average per day/Living Room/" + formatted_now + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        print("data_temp: ", path_temp)
        data_hum.append(db.reference(path_hum).get())

    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    processed_data_temp_average = round(raw_data_temp_average, 1)
    processed_data_hum_average = round(raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    formatted_now = str(month).zfill(2) + "-" + str(year)
    path_temp_average = user_id + "/Average per month" + "/Living Room/" + formatted_now + "/temperature"
    path_hum_average = user_id + "/Average per month" + "/Living Room/" + formatted_now + "/humidity"
    db.reference(path_temp_average).set(processed_data_temp_average)
    db.reference(path_hum_average).set(processed_data_hum_average)

    print("processed_data_temp_average per month: ", processed_data_temp_average)
    print("processed_data_hum_average per month: ", processed_data_hum_average)


def process_data_days(hours, user_id, db, month, year):
    """

    :type db: object
    :type user_id: object
    :param hours:
    :param user_id:
    :param db:
    :param month:
    :param year:
    """

   #day-1
    days = datetime.today() - timedelta(days=1)

    data_temp = []
    data_hum = []

    while hours < 24:
        formatted_now = "-" + str(month).zfill(2) + "-" + str(year)
        path_temp = user_id + "/Average per hour/Living Room/" + str(days).zfill(2) + formatted_now + " - " + str(
            hours).zfill(
            2) + "/temperature"
        path_hum = user_id + "/Average per hour/Living Room/" + str(days).zfill(2) + formatted_now + " - " + str(
            hours).zfill(
            2) + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())

        hours += 1
    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    processed_data_temp_average = round(raw_data_temp_average, 1)
    processed_data_hum_average = round(raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    formatted_now = str(days).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year)
    path_temp_average = user_id + "/Average per day" + "/Living Room/" + formatted_now + "/temperature"
    path_hum_average = user_id + "/Average per day" + "/Living Room/" + formatted_now + "/humidity"
    db.reference(path_temp_average).set(processed_data_temp_average)
    db.reference(path_hum_average).set(processed_data_hum_average)

    print("processed_data_temp_average per day: ", processed_data_temp_average)
    print("processed_data_hum_average per day: ", processed_data_hum_average)


def process_data_hours(minutes, hours, user_id, device, db, days, month, year):
    """

    :type db: object
    :type device: object
    :type user_id: object
    :param minutes:
    :param hours:
    :param user_id:
    :param device:
    :param db:
    :param days:
    :param month:
    :param year:
    """
    if hours > 0:
        hours -= 1
    elif hours == 00:
        hours = 23
    data_temp = []
    data_hum = []
    while minutes < 60:
        formatted_now = str(days).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + " - " + str(
            hours).zfill(2) + "-" + str(minutes).zfill(2)
        path_temp = user_id + "/Living Room/" + formatted_now + "/" + device + "/temperature"
        path_hum = user_id + "/Living Room/" + formatted_now + "/" + device + "/humidity"
        data_temp.append(db.reference(path_temp).get())
        data_hum.append(db.reference(path_hum).get())

        minutes += 1
    # Calculate the sum while ignoring None values
    raw_data_temp_average = sum(x for x in data_temp if x is not None) / len(data_temp)
    raw_data_hum_average = sum(x for x in data_hum if x is not None) / len(data_hum)
    processed_data_temp_average = round(raw_data_temp_average, 1)
    processed_data_hum_average = round(raw_data_hum_average, 1)
    # Save the average temperature to Firebase
    formatted_now = str(days).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + " - " + str(
        hours).zfill(2)
    path_temp_average = user_id + "/Average per hour" + "/Living Room/" + formatted_now + "/temperature"
    path_hum_average = user_id + "/Average per hour" + "/Living Room/" + formatted_now + "/humidity"
    db.reference(path_temp_average).set(processed_data_temp_average)
    db.reference(path_hum_average).set(processed_data_hum_average)

    print("processed_data_temp_average per hour: ", processed_data_temp_average)
    print("processed_data_hum_average per hour: ", processed_data_hum_average)


if __name__ == "__main__":
    continuously_check_time(user_id, db)
