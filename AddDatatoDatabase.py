import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-da701-default-rtdb.firebaseio.com/"
})

ref = db.reference('students')

data = {
    "60003210191":
        {
            'Name': "Bhavya Poddar",
            'University': "Mumbai University",
            'Work': 'Student',
            'Total Attendance': 0,
            'Last Attendance': "2023-08-01 00:54:34"
        },
    "328941":
        {
            'Name': "Mark Zuckerberg",
            'University': "Harvard University",
            'Work': 'Founder (META)',
            'Total Attendance': 0,
            'Last Attendance': "2023-08-01 00:54:34"
        },
    "348490":
        {
            'Name': "Ratan Tata",
            'University': "Harvard University",
            'Work': 'Chairman (TATA)',
            'Total Attendance': 0,
            'Last Attendance': "2023-08-01 00:54:34"
        },
    "965256":
        {
            'Name': "Amitabh Bachchan",
            'University': "University of Delhi",
            'Work': 'Actor',
            'Total Attendance': 0,
            'Last Attendance': "2023-08-01 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)