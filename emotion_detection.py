import cv2
from deepface import DeepFace
import numpy as np

face_cascade = cv2.CascadeClassifier(r"data/haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0)
while video.isOpened():
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)

    for x, y, w, h in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        try :
            obj = DeepFace.analyze(img_path = img , actions = ['emotion'], enforce_detection=False)
            emotion = obj['dominant_emotion']
            print(f"Emotion : {emotion}")
        except :
            print("No Face")
    cv2.imshow('Live Footage', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
