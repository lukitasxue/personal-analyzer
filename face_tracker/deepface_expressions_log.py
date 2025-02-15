import cv2 as cv
from deepface import DeepFace
import pandas as pd
import time
import os

csv_file = "emotion_log.csv"

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Timestamp", "Emotion", "Confidence"])
    df.to_csv(csv_file, index=False)


# webcam
cap = cv.VideoCapture(0)
last_emotion = None

while True:
    ret, frame = cap.read() # Read a frame from the webcam  (ret is True if the frame was captured successfully)
    if not ret:
        break

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        confidence = max(analysis[0]['emotion'].values())

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S") 

        if dominant_emotion == "fear":
            dominant_emotion = "neutral"  # Convert fear to neutral


        if dominant_emotion != last_emotion and confidence >= 60:
            df = pd.DataFrame([[timestamp, dominant_emotion, confidence]], columns=["Timestamp", "Emotion", "Confidence"])
            df.to_csv(csv_file, mode='a', header=False, index=False)

            last_emotion = dominant_emotion
        

        cv.putText(frame, dominant_emotion, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    except:
        pass # if no face detected, continue

    cv.imshow("Emotion Logging", frame)


    # Press 'q' to exit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()