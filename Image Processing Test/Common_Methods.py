# Imports
import cv2 as cv
import numpy as np

"""
Function Brief: Get the device size(screen resolution)
Returns:
    screen_width (int): The width of the screen in pixels.
    screen_height (int): The height of the screen in pixels.
"""
def getScreenResolution():
    cv.namedWindow('TempWindow', cv.WINDOW_NORMAL)
    screen_width, screen_height = cv.getWindowImageRect('TempWindow')[2:4]
    cv.destroyWindow('TempWindow')
    
    return screen_width, screen_height

"""
Function Brief: Resize the image based on the device screen size while maintaining the aspect ratio.
Parameters:
    image (numpy.ndarray): The input image to be resized.
Returns:
    resized_image (numpy.ndarray): The resized image with adjusted dimensions.
"""
def resizeImageToScreen(image, width_percent, height_percent):

    screen_width, screen_height = getScreenResolution()
    
    # Calculate the aspect ratio of the image
    height, width = image.shape[:2]
    aspect_ratio = width / height

    # Determine whether to scale by width or height
    if width > height:
        new_width = int(screen_width * width_percent)  # Scale image to 125% of screen width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(screen_height * height_percent)  # Scale image to 125% of screen height
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image accordingly
    resized_image = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)
    
    return resized_image

"""
Function Brief: Order the given contour points into a specific sequence:
[top-left, top-right, bottom-right, bottom-left].
Parameters:
    contour_arr (numpy.ndarray): An array of contour points (4 points) to be ordered.
Returns:
    rect (numpy.ndarray): An ordered array of points representing the rectangle corners.
"""
def orderPoints(contour_arr):
     
    # [top-left, top-right, bottom-right, bottom-left]
    rect_corners = np.zeros((4, 2), dtype="float32")

    s = contour_arr.sum(axis=1)
    # top-left -> smallest sum 
    rect_corners[0] = contour_arr[np.argmin(s)]
    # bottom-right -> largest sum
    rect_corners[2] = contour_arr[np.argmax(s)]
 
    diff = np.diff(contour_arr, axis=1)
    # top-right -> smallest difference
    rect_corners[1] = contour_arr[np.argmin(diff)]
    # bottom-left -> largest difference
    rect_corners[3] = contour_arr[np.argmax(diff)]

    return rect_corners

"""
Function Brief: Check if the given contour points form a proper rectangle.
Parameters:
    contour_arr (numpy.ndarray): An array of contour points (4 points) to check.
Returns:
    bool: True if the points form a rectangle, False otherwise.
"""
def isRectangle(contour_arr):
    
    if len(contour_arr) != 4:
        return False

    # Calculate the angle between three points (in degrees)
    def angle(pt1, pt2, pt3):
        vec1 = pt1 - pt2
        vec2 = pt3 - pt2
        dot_product = np.dot(vec1, vec2)
        mag1 = np.linalg.norm(vec1)
        mag2 = np.linalg.norm(vec2)
        cosine_angle = dot_product / (mag1 * mag2)
        angle_rad = np.arccos(cosine_angle)
        angle_deg = np.degrees(angle_rad)
        return angle_deg

    # Get the four angles formed
    angle1 = angle(contour_arr[0], contour_arr[1], contour_arr[2])
    angle2 = angle(contour_arr[1], contour_arr[2], contour_arr[3])
    angle3 = angle(contour_arr[2], contour_arr[3], contour_arr[0])
    angle4 = angle(contour_arr[3], contour_arr[0], contour_arr[1])

    # Check if all angles are close to 90 degrees
    return all(80 <= a <= 100 for a in [angle1, angle2, angle3, angle4])

"""
Function Brief: Apply a four-point perspective transform to the input image 
using the specified contour points, resulting in a top-down view of the selected area.
Parameters:
    image (numpy.ndarray): The input image to be warped.
    contour_arr (numpy.ndarray): The contour points used for the perspective transformation.
Returns:
    warped (numpy.ndarray): The resulting warped image with a top-down view.
"""
def fourPointTransform(image, contour_arr):
  
    rect = orderPoints(contour_arr)
    # top-left, top-right, bottom-right, bottom-left
    (tl, tr, br, bl) = rect 

    # Compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # Compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Set of destination points to obtain a "birds eye view" of the image
    dst = np.array([[0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def unblurImage(blurred_img):
    # Define a sharpening kernel (this is a simple one)
    sharpening_kernel = np.array([[-1, -1, -1, -1, -1],
                                  [-1, -1, 100, -1, -1],
                                  [-1, -1, -1, -1, -1]])
    
    # Apply the sharpening filter using cv2.filter2D
    unblurred_img = cv.filter2D(blurred_img, -5, sharpening_kernel)
    
    return unblurred_img