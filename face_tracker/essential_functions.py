import cv2 as cv


img = cv.imread("images/test.png")
# 5 basic functionalities

# convert to gray an image
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale
cv.imshow("Grayscale Image", gray)


# Blur image
blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
cv.imshow("blured", blur)


# Edge cascade
canny = cv.Canny(img, 125, 175)
cv.imshow("Canny edges", canny)


# Dilating the image
dilated = cv.dilate(canny, (7,7), iterations=3)
cv.imshow("dilated", dilated)


#eroding
eroded = cv.erode(dilated, (7,7), iterations=3)
cv.imshow("eroded", eroded)


#resize 
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow("resized", resized)


#CROPPING
cropped = img[50:300, 200:400]
cv.imshow("cropped", cropped)

cv.waitKey(0)