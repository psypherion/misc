import cv2
from deepface import DeepFace
import numpy as np

print("""
 _______ .___  ___.   ______   .___________. __    ______   .__   __.             ___       _______  _______       .______          ___       ______  _______         _______  _______ .__   __.  _______   _______ .______         
|   ____||   \/   |  /  __  \  |           ||  |  /  __  \  |  \ |  |            /   \     /  _____||   ____|      |   _  \        /   \     /      ||   ____|       /  _____||   ____||  \ |  | |       \ |   ____||   _  \        
|  |__   |  \  /  | |  |  |  | `---|  |----`|  | |  |  |  | |   \|  |           /  ^  \   |  |  __  |  |__         |  |_)  |      /  ^  \   |  ,----'|  |__         |  |  __  |  |__   |   \|  | |  .--.  ||  |__   |  |_)  |       
|   __|  |  |\/|  | |  |  |  |     |  |     |  | |  |  |  | |  . `  |          /  /_\  \  |  | |_ | |   __|        |      /      /  /_\  \  |  |     |   __|        |  | |_ | |   __|  |  . `  | |  |  |  ||   __|  |      /        
|  |____ |  |  |  | |  `--'  |     |  |     |  | |  `--'  | |  |\   |  __     /  _____  \ |  |__| | |  |____ __    |  |\  \----./  _____  \ |  `----.|  |____ __    |  |__| | |  |____ |  |\   | |  '--'  ||  |____ |  |\  \----.   
|_______||__|  |__|  \______/      |__|     |__|  \______/  |__| \__| (_ )   /__/     \__\ \______| |_______(_ )   | _| `._____/__/     \__\ \______||_______(_ )    \______| |_______||__| \__| |_______/ |_______|| _| `._____|   
                                                                       |/                                    |/                                               |/                                                                    
 _______   _______ .___________. _______   ______ .___________. __    ______   .__   __.                                                                                                                                            
|       \ |   ____||           ||   ____| /      ||           ||  |  /  __  \  |  \ |  |                                                                                                                                            
|  .--.  ||  |__   `---|  |----`|  |__   |  ,----'`---|  |----`|  | |  |  |  | |   \|  |                                                                                                                                            
|  |  |  ||   __|      |  |     |   __|  |  |         |  |     |  | |  |  |  | |  . `  |                                                                                                                                            
|  '--'  ||  |____     |  |     |  |____ |  `----.    |  |     |  | |  `--'  | |  |\   |                                                                                                                                            
|_______/ |_______|    |__|     |_______| \______|    |__|     |__|  \______/  |__| \__|                                                                                                                                            
                                                                                                                                                                                                                                    
.______   .______        ______     _______ .______          ___      .___  ___.                                                                                                                                                    
|   _  \  |   _  \      /  __  \   /  _____||   _  \        /   \     |   \/   |                                                                                                                                                    
|  |_)  | |  |_)  |    |  |  |  | |  |  __  |  |_)  |      /  ^  \    |  \  /  |                                                                                                                                                    
|   ___/  |      /     |  |  |  | |  | |_ | |      /      /  /_\  \   |  |\/|  |                                                                                                                                                    
|  |      |  |\  \----.|  `--'  | |  |__| | |  |\  \----./  _____  \  |  |  |  |                                                                                                                                                    
| _|      | _| `._____| \______/   \______| | _| `._____/__/     \__\ |__|  |__|                                                                                                                                                    
                                                                                                                                                                                                                                    


PS : All the output/Predictions may or may not be accurate because of accuracy issues of the training model.   
      """)
face_cascade = cv2.CascadeClassifier(r"data/haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0)
while video.isOpened():
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,4)

    for x, y, w, h in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        try :
            obj = DeepFace.analyze(img_path = img , actions = ['age', 'emotion', 'race', 'gender'], enforce_detection=False)
            emotion = obj['dominant_emotion']
            age = obj['age']
            race = obj['dominant_race']
            gender = obj['gender']
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 
                f"Age:{age} ,"
                    f"Gender:{gender} ,"
                    f"Race:{race} ,"
                    f"Emotion:{emotion}", 
                (50, 50), 
                font, 0.68, 
                (255, 0, 20), 
                2, 
                cv2.LINE_4)
        except :
            print("No Face")
    cv2.imshow('Live Footage', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
