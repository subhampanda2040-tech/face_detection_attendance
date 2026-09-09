from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime


from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground=cv2.imread("background.png")

COL_NAMES = ['NAME', 'TIME']

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    
    attendances_in_frame = []
    
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        attendances_in_frame.append([str(output[0]), str(timestamp)])
        
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame",imgBackground)
    k=cv2.waitKey(1)
    if k==ord('o') or k==ord('O'):
        if len(attendances_in_frame) > 0:
            try:
                if exist:
                    with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                        writer=csv.writer(csvfile)
                        writer.writerows(attendances_in_frame)
                else:
                    with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                        writer=csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        writer.writerows(attendances_in_frame)
                speak("Attendance Taken..")
                break
            except PermissionError:
                speak("Error. Please close the attendance file and press O again.")
            except Exception as e:
                print("Error saving attendance:", e)
                speak("An error occurred while saving attendance.")
        else:
            speak("No face detected. Please face the camera and press O again.")
    if k==ord('q') or k==ord('Q'):
        break
video.release()
cv2.destroyAllWindows()

