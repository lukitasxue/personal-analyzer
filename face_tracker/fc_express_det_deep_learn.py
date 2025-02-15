import cv2 as cv
from deepface import DeepFace

#deep learning face detector
modelFile = "res10_300x300_ssd_iter_140000.caffemodel" # Pre-trained model weights
configFile = "deploy.prototxt" # Model architecture
net = cv.dnn.readNetFromCaffe(configFile, modelFile)


# webcam
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() # Read a frame from the webcam  (ret is True if the frame was captured successfully)
    if not ret:
        break

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        

        cv.putText(frame, dominant_emotion, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    except:
        pass # if no face detected, continue

    cv.imshow("Deep Learning Face Exrepssion Detection", frame)


    # Press 'q' to exit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()