import cv2 as cv
import numpy as np

#create blank image
blank = np.zeros((500,500,3), dtype='uint8') # np.zeros((w,h,color channel), dtype)
cv.imshow("Blank Image", blank)

# 1. paint the image a certain colour
# blank[:] = 0,0,255 #red
# cv.imshow("Red", blank)

# 1.1 paint certain section
# blank[200:300, 300:400] = 0,0,255 #red square
# cv.imshow("Red square", blank)

# 2 draw rectangle
cv.rectangle(blank, (0,0), (250,250), (0,255,0), thickness=2) #canva, (origin), (point 2), (color), rectangle border thickness [for filling rectangle cv.FILLED or -1]
cv.imshow("Rectangle", blank)

#3. draw circle
cv.circle(blank, (250,250), 40, (0,0,255), thickness=3)
cv.imshow("Circle", blank)

# 4. draw line
cv.line(blank, (100,250), (400,450), (255,255,255), thickness=2)
cv.imshow("Line", blank)

# 5. write text
cv.putText(blank, 'Hello world', (255,255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), thickness=2)
cv.imshow("text", blank)

cv.waitKey(0)  # Press any key to close the window

