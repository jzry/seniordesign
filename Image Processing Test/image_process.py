import cv2
import numpy as np

# Load the image
img = cv2.imread('test.jpg')

# Preprocess the image
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 150, 800)

# Detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=20, maxLineGap=10)

# Draw detected lines on the original image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Show the result
cv2.imshow('Detected Columns', img)
cv2.waitKey(0)
cv2.destroyAllWindows()