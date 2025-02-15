import cv2 as cv


def rescaleFrame(frame, scale=0.75): 
    #rescale video, image and live video
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)

    dimensions=(width,height)
    
    return cv.resize(frame,dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height):
    #only works for live video
    capture.set(3,width)
    capture.set(4,height)

img = cv.imread("images/test.png")  # Make sure test.jpg exists
resized_image = rescaleFrame(img)
cv.imshow("reized image", resized_image)
cv.imshow("Test Image", img) #name of the window, and type of file


#reading videos 
capture = cv.VideoCapture('videos/test_chamber.mp4') #numer reference the camera number

while True:
    isTrue, frame = capture.read()
    
    frame_resized = rescaleFrame(frame, scale=.2)

    cv.imshow('Video', frame)
    cv.imshow('Video Rezised', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'): #if press d, destroy the window
        break

capture.release()

cv.destroyAllWindows()