import cv2 as cv

#deep learning face detector
modelFile = "res10_300x300_ssd_iter_140000.caffemodel" # Pre-trained model weights
configFile = "deploy.prototxt" # Model architecture
net = cv.dnn.readNetFromCaffe(configFile, modelFile)


# webcam
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read() # Read a frame from the webcam  (ret is True if the frame was captured successfully)
    (h, w) = frame.shape[:2] # Get frame dimensions

    #convert img to blob (preprocess for deep learning)
    blob = cv.dnn.blobFromImage(frame, scalefactor=1.0, size=(300,300), mean=(104.0, 177.9, 123.9))

    #detect face
    net.setInput(blob)
    detections = net.forward() # Perform forward pass (face detection)

    #draw rectangle around detected faces
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] # Extract confidence score

        if confidence > 0.5: # Confidence + 50%? if yes then,
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x, y, x2, y2) = box.astype("int")
            cv.rectangle(frame, (x,y), (x2, y2), (0,255,0), 2)
            text = f"{confidence*100:.2f}%"
            cv.putText(frame, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv.imshow("Deep Learning Face Detection", frame)

    # Press 'q' to exit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()