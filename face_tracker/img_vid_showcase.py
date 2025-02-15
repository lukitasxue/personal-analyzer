import cv2 as cv
print("OpenCV Version:", cv.__version__)


# Load and display an image
# img = cv.imread("images/test.png")  # Make sure test.jpg exists
# cv.imshow("Test Image", img) #name of the window, and type of file
# cv.waitKey(0)  # Press any key to close the window

#reading videos 
# capture = cv.VideoCapture(0) #numer reference the camera number

# while True:
#     isTrue, frame = capture.read() #capture frame by frame
#     cv.imshow('Video', frame)

#     if cv.waitKey(20) & 0xFF==ord('q'): #if press q, destroy the window
#         break
# capture.release()

# convert to gray an image
img = cv.imread("images/test.png")  # Load an image
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale

cv.imshow("Grayscale Image", gray)
cv.waitKey(0)



cv.destroyAllWindows()



