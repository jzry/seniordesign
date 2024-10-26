# Imports
import cv2 as cv
import numpy as np
import Common_Methods as cm

"""
Function Brief: Sorts four corner points of a contour in clockwise order, starting from the top-left point.
Parameters:
    corner_pts_arr (numpy.ndarray): An array of four corner points (shape: (4, 2)).
Returns:
    pts (numpy.ndarray): An array of sorted corner points in clockwise order (shape: (4, 2)).
    width (int): The width of the rectangle formed by the points.
    height (int): The height of the rectangle formed by the points.
"""
def processContour(corner_pts_arr):

    corner_pts_arr = corner_pts_arr.reshape((4, 2))

    # Sort points in clockwise order, starting from top left
    pts = np.zeros((4, 2), dtype=np.float32)

    s = corner_pts_arr.sum(axis=1)
    # Smallest sum = top left point
    pts[0] = corner_pts_arr[np.argmin(s)] 
    # Largest sum = bottom right point
    pts[2] = corner_pts_arr[np.argmax(s)]

    # For the other 2 points, compute difference:
    diff = np.diff(corner_pts_arr, axis=1)
    # Smallest difference = top right point
    pts[1] = corner_pts_arr[np.argmin(diff)]
    # Largest difference = bottom left point
    pts[3] = corner_pts_arr[np.argmax(diff)]

    # Smallest height and width
    width = int(min(pts[1][0] - pts[0][0], pts[2][0] - pts[3][0]))
    height = int(min(pts[3][1] - pts[0][1], pts[2][1] - pts[1][1]))

    return pts, width, height

"""
Function Brief: Finds the largest quadrilateral contour from a list of contours.
Parameters:
    contours (list): A list of contours, where each contour is an array of points.
Returns:
    biggest_contour (list): A list containing the largest 4-sided contour found.
    biggest_contour_approx (list): A list containing the approximated points of the largest contour.
"""
def largestQuadrilateralContour(contours):
    
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)

    for contour in sorted_contours:

        perimeter = cv.arcLength(contour, True)

        # Approximate a shape that resembles the contour with sharp edges
        approx = cv.approxPolyDP(contour, 0.01 * perimeter, True)

        # Check if the approximation contains only 4 sides
        if len(approx) == 4:
            biggest_contour = contour
            biggest_contour_approx = approx
            break

    return [biggest_contour], [biggest_contour_approx]

"""
Function Brief: Extract and warp a score sheet from an input image by detecting 
the largest quadrilateral contour and applying a perspective transformation.
Parameters:
    BC_scoresheet (str): The file path of the input image containing the score sheet.
Returns:
    warped_img (numpy.ndarray): The resulting image of the extracted and 
    warped score sheet with sharp borders.
"""
def BC_Paper_Extraction(BC_scoresheet):

    original_img = cv.imread(BC_scoresheet)

    # Prepocess Image
    gray_scale_img = cv.cvtColor(original_img, cv.COLOR_BGR2GRAY)
    
    # Guassian to blur image 
    gaussian_img = cv.GaussianBlur(gray_scale_img, (17,17), 0)
 
    # Adaptive Threshold
    thresholded_img = cv.adaptiveThreshold(gaussian_img, 255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
    cv.imwrite("threshold.jpg", thresholded_img)


    contours, hierarchy = cv.findContours(thresholded_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour_img = cv.drawContours(original_img.copy(), contours, -1, (0,255, 0), thickness=2, lineType=cv.LINE_AA)
    cv.imwrite("contour.jpg", contour_img)

    # Identify Contour with largest 4 sides
    paper_contour, paper_contour_approx = largestQuadrilateralContour(contours)
    if paper_contour[0] is None:
        raise ValueError("Paper not detected.")
    print(paper_contour_approx)
    
    # Sort points in clockwise order, compute paper width and height
    paper_pts, paper_width, paper_height = processContour(paper_contour_approx[0])

    # Get the sharp borders
    warped_img = cm.fourPointTransform(original_img, paper_pts)

    cv.imwrite("warped.jpg", warped_img)

    return warped_img

extracted_paper = BC_Paper_Extraction('BC Scoresheet Pictures\BC-1.jpg')