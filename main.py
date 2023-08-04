import cv2
import pickle
import os
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-da701-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-da701.appspot.com"
})

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 720)

# Load the encoding file
print("Loading Encode File...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

counter = 0

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDist", faceDist)

        matchIndex = np.argmin(faceDist)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("known face detected")
            # print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = x1, y1, x2 - x1, y2 - y1
            img = cvzone.cornerRect(img, bbox, rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                counter = 1
        else:
            print("Unknown face detected")

        if counter != 0:

            if counter == 1:

                studentInfo = db.reference(f'students/{id}').get()
                print(studentInfo)

                # Update the attendance
                datetimeObject = datetime.strptime(studentInfo['Last Attendance'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                # print(secondsElapsed)
                if secondsElapsed > 3600:
                    print("Marked")
                    ref = db.reference(f'students/{id}')
                    studentInfo['Total Attendance'] += 1
                    ref.child('Total Attendance').set(studentInfo['Total Attendance'])
                    ref.child('Last Attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    print("Already Marked")

                counter += 1

    cv2.imshow("face recognition", img)
    cv2.waitKey(1)
