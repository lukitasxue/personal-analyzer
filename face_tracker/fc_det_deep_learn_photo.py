import cv2 as cv

#deep learning face detector
modelFile = "res10_300x300_ssd_iter_140000.caffemodel"  # Pre-trained model weights
configFile = "deploy.prototxt"  # Model architecture
net = cv.dnn.readNetFromCaffe(configFile, modelFile)


# load image
img =  cv.imread("images/my_photo.jpeg")
(h, w) = img.shape[:2]

#convert image to blob (preprocess for deep learning)
blob = cv.dnn.blobFromImage(img, scalefactor=1.0, size=(300,300), mean=(104.0, 177.9, 123.9))

#detect face
net.setInput(blob)
detections = net.forward()

#draw rectangle
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    if confidence > 0.5:
        box = detections[0, 0, i, 3:7] * [w, h, w, h]
        (x, y, x2, y2) = box.astype("int")
        cv.rectangle(img, (x,y), (x2, y2), (0,255,0), 2)
        text = f"{confidence*100:.2f}%"
        cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


#show img
cv.imshow("deep learn face det", img)
cv.waitKey()
cv.destroyAllWindows()