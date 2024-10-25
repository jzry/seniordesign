# The preprocessor creates a black and white image of the scoresheet,
# warps it so it's flattened, and returns a numpy array of the corners of
# where the scoresheet is on an image.
# This is the first version of the preprocessor without canny.

import cv2
import numpy as np

# The filepath & filename for the file that you want to process.
filePath = "test_input/"
fileName = "bc1.jpg"
fileOutPath = "test_output/"

# Read image.
img = cv2.imread(filePath + fileName)

# Convert img to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur image.
blur = cv2.GaussianBlur(gray, (3,3), 0)

# Do Otsu threshold on gray image.
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# Apply morphology.
kernel = np.ones((7,7), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

# Get the largest contour.
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
area_thresh = 0
for c in contours:
    area = cv2.contourArea(c)
    if area > area_thresh:
        area_thresh = area
        big_contour = c

# Draw white filled largest contour on black just as a check to see it got the correct region.
page = np.zeros_like(img)

contours_drawn = cv2.drawContours(page, [big_contour], 0, (255,255,255), -1)

# Get perimeter and approximate a polygon.
peri = cv2.arcLength(big_contour, True)
corners = cv2.approxPolyDP(big_contour, 0.04 * peri, True)

# Draw polygon on input image from detected corners.
polygon = img.copy()
cv2.polylines(polygon, [corners], True, (0,0,255), 1, cv2.LINE_AA)
# Alternate: cv2.drawContours(page,[corners],0,(0,0,255),1)

# Print the number of found corners and the corner coordinates.
# They seem to be listed counter-clockwise from the top most corner.
print(len(corners))
print(corners)

# for simplicity get average of top/bottom side widths and average of left/right side heights
# note: probably better to get average of horizontal lengths and of vertical lengths
width = 0.5*( (corners[0][0][0] - corners[1][0][0]) + (corners[3][0][0] - corners[2][0][0]) )
height = 0.5*( (corners[2][0][1] - corners[1][0][1]) + (corners[3][0][1] - corners[0][0][1]) )
width = np.int8(width)
height = np.int8(height)

# reformat input corners to x,y list
icorners = []
for corner in corners:
    pt = [ corner[0][0],corner[0][1] ]
    icorners.append(pt)
icorners = np.float32(icorners)

# get corresponding output corners from width and height
ocorners = [ [width,0], [0,0], [0,height], [width,height] ]
ocorners = np.float32(ocorners)

print("ocorners", ocorners)
print("icorners", icorners)

# get perspective tranformation matrix
M = cv2.getPerspectiveTransform(icorners, ocorners)

# do perspective 
warped = cv2.warpPerspective(img, M, (width, height))

# write results
cv2.imwrite(fileOutPath + "out_thresh.jpg", thresh)
cv2.imwrite(fileOutPath + "out_morph.jpg", morph)
cv2.imwrite(fileOutPath + "out_polygon.jpg", polygon)
cv2.imwrite(fileOutPath + "out_warped.jpg", warped)
cv2.imwrite(fileOutPath + "out_page.jpg", page)
cv2.imwrite(fileOutPath + "out_original.jpg", img)

# # display it
# cv2.imshow("out_thresh", thresh)
# cv2.imshow("out_morph", morph)
# cv2.imshow("out_olygon", polygon)
# cv2.imshow("out_warped", warped)
# cv2.imshow("out_page", page)
# cv2.waitKey(0)