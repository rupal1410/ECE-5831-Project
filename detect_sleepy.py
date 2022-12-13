import cv2
import numpy as np
from playsound import playsound
from PIL import Image, ImageDraw
import face_recognition
from tensorflow import keras
model = keras.models.load_model('E:/School/DDDSystem/CNN_drozyDATA.h5')

def eye_cropper(frame):

    # create a variable for the facial feature coordinates
    facial = face_recognition.face_landmarks(frame)
    try:
        eye = facial[0]['left_eye']
    except:
        try:
            eye = facial[0]['right_eye']
        except:
            return

    # establish the max x and y coordinates of the eye
    x_max = max([c[0] for c in eye])
    x_min = min([c[0] for c in eye])
    y_max = max([c[1] for c in eye])
    y_min = min([c[1] for c in eye])


    # establish the range of x and y coordinates
    x_range = x_max - x_min
    y_range = y_max - y_min


    if x_range > y_range:
        right = round(.5*x_range) + x_max
        left = x_min - round(.5*x_range)
        bottom = round((((right-left) - y_range))/2) + y_max
        top = y_min - round((((right-left) - y_range))/2)
    else:
        bottom = round(.5*y_range) + y_max
        top = y_min - round(.5*y_range)
        right = round((((bottom-top) - x_range))/2) + x_max
        left = x_min - round((((bottom-top) - x_range))/2)


    # crop the image according to the coordinates determined above
    cropped = frame[top:(bottom + 1), left:(right + 1)]

    # resize the image
    cropped = cv2.resize(cropped, (80,80))
    image = cropped.reshape(-1, 80, 80, 3)


    return image 


# initiate webcam
cap = cv2.VideoCapture(0)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(cap.get(cv2.CAP_PROP_FPS))


if not cap.isOpened():
    raise IOError('Cannot open webcam')

# set a counter
counter = 0

# create a while loop that runs while webcam is in use

while True:

    ret, frame = cap.read()

    frame_count = 0
    if frame_count == 0:
        frame_count += 1
        pass
    else:
        count = 0
        continue

    image = eye_cropper(frame)
    try:
        image = image/255.0
    except:
        continue

    # get prediction from model

    prediction = model.predict(image)

    # Based on prediction, display either "Open Eyes" or "Closed Eyes"

    if prediction < 0.5:
        counter = 0
        status = 'Open'
        print(prediction)
        cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)
        cv2.putText(frame, status, (round(w/2)-70,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_4)
        x1, y1,w1,h1 = 0,0,175,75
    else:
        counter = counter + 1
        status = 'Closed'
        print(prediction)
        cv2.rectangle(frame, (round(w/2) - 110,20), (round(w/2) + 110, 80), (38,38,38), -1)
        cv2.putText(frame, status, (round(w/2)-70,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2, cv2.LINE_4)
        x1, y1,w1,h1 = 0,0,175,75
     
        if counter > 5:

            x1, y1, w1, h1 = 400,400,400,100
            cv2.rectangle(frame, (round(w/2) - 160, round(h) - 200), (round(w/2) + 160, round(h) - 120), (0,0,255), -1)

            cv2.putText(frame, 'DRIVER SLEEPING', (round(w/2)-100,round(h) - 146), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_4)

            cv2.imshow('Drowsiness Detected', frame)
            k = cv2.waitKey(1)
            counter = 1
            continue
        
    # Draw boxes around face and eyes on the live footage
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
    cv2.imshow('Drowsiness Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()