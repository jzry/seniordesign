# This program removes horizontal lines from the extracted boxes.
import cv2
import numpy as np

DEBUG = 0

# Given the image, return the same image with removed horizontal lines.
def remove_horizontal_lines(img):

    # Read in the segmented box.
    # img = cv2.imread(fileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove horizontal lines.
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,81,17)

    if DEBUG == 1:
        cv2.imwrite("thresh.jpg", thresh)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))

    # Using morph close to get lines outside the drawing.
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    mask = np.zeros(gray.shape, np.uint8)
    for c in cnts:
        cv2.drawContours(mask, [c], -1, (255,255,255),2)

    # First inpaint.
    img_dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    if DEBUG == 1:
        cv2.imwrite("img_dst.jpg", img_dst)

    gray_dst = cv2.cvtColor(img_dst, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_dst, 50, 150, apertureSize = 3)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))

    # Using morph open to get lines inside the drawing.
    opening = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    mask = np.uint8(img_dst)
    mask = np.zeros(gray_dst.shape, np.uint8)
    for c in cnts:
        cv2.drawContours(mask, [c], -1, (255,255,255),2)

    # Second inpaint.
    horizontals_removed = cv2.inpaint(img_dst, mask, 3, cv2.INPAINT_TELEA)

    # cv2.imwrite("horizontals_removed.jpg", horizontals_removed)
    # image = cv2.imread("horizontals_removed.jpg")

    return horizontals_removed