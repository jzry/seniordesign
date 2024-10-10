# Imports
import cv2 as cv
import numpy as np
import math

# Read RGB image uisng CV and result is a RGB image
def Read_RGB_Image(path):
    image=cv.imread(path,1)
    
    # cv.IMREAD_COLOR: It specifies to load a color image. Any transparency of image will be neglected.
    # Converting BGR color to RGB color format
    RGB_img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    return RGB_img  

# Function to sort points in a contour in clockwise order, starting from top left
def processContour(approx):
    # Reshape array([x, y], ...) to array( array([x], [y]), ...)
    approx = approx.reshape((4, 2))

    # Sort points in clockwise order, starting from top left
    pts = np.zeros((4, 2), dtype=np.float32)

    # Add up all values
    # Smallest sum = top left point
    # Largest sum = bottom right point
    s = approx.sum(axis=1)
    pts[0] = approx[np.argmin(s)]
    pts[2] = approx[np.argmax(s)]

    # For the other 2 points, compute difference between all points
    # Smallest difference = top right point
    # Largest difference = bottom left point
    diff = np.diff(approx, axis=1)
    pts[1] = approx[np.argmin(diff)]
    pts[3] = approx[np.argmax(diff)]

    # Calculate smallest height and width
    width = int(min(pts[1][0] - pts[0][0], pts[2][0] - pts[3][0]))
    height = int(min(pts[3][1] - pts[0][1], pts[2][1] - pts[1][1]))

    return pts, width, height

# Function to find the largest 4-sided contour from an array of countours
def findLargestQuadrilateralContour(contours):
    # Sort contours from smallest area to biggest
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)

    biggest_contour = None
    biggest_contour_approx = None

    for cnt in sorted_contours:
        # Get the length of the perimeter
        perimeter = cv.arcLength(cnt, True)

        # Approximate a shape that resembles the contour
        # This is needed because the image might be warped, thus
        # edges are curved and not perfectly straight
        approx = cv.approxPolyDP(cnt, 0.01 * perimeter, True)

        # Check if the approximation contains only 4 sides
        # (i.e. quadrilateral)
        if len(approx) == 4:
            biggest_contour = cnt
            biggest_contour_approx = approx
            break

    return [biggest_contour], [biggest_contour_approx]

# Function to get screen resolution (device size)
def get_screen_resolution():
    # Get screen resolution using OpenCV's `cv.getWindowImageRect` 
    # We'll use a blank window to detect the screen resolution.
    cv.namedWindow('TempWindow', cv.WINDOW_NORMAL)
    screen_width, screen_height = cv.getWindowImageRect('TempWindow')[2:4]
    cv.destroyWindow('TempWindow')
    
    return screen_width, screen_height

# Function to resize the image based on screen size
def resize_image_to_screen(image):
    # Get screen resolution
    screen_width, screen_height = get_screen_resolution()
    
    # Calculate the aspect ratio of the image
    height, width = image.shape[:2]
    aspect_ratio = width / height

    # Determine whether to scale by width or height
    if width > height:
        new_width = int(screen_width * 1.25)  # Scale image to 125% of screen width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(screen_height * 1.25)  # Scale image to 125% of screen height
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image accordingly
    resized_image = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)
    
    return resized_image

def Paper_Extraction(path):
    # Read Image
    img=cv.imread(path)

    # Resize the image based on device screen resolution
    img = resize_image_to_screen(img)

    # Gray_Scale_img=rgb2gray(Original_img)
    Gray_Scale_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Step 1 Enhance lines of the image
    #1.Guassian to blur image 
    kernel_size=max(int(Gray_Scale_img.shape[0] * 0.005), int(Gray_Scale_img.shape[1] * 0.005))
    # Kernel must have odd values because of GaussianBlur
    if kernel_size % 2 == 0:
        kernel_size += 1
    kernel=(kernel_size,kernel_size) #filter size
    Gaussian_Img=cv.GaussianBlur(Gray_Scale_img,kernel,1)
    print(np.shape(Gaussian_Img))
    
    #2.Adpative Thresholding
    # If we tried to use Normal Thresholding =>Global Thresholding Regions Black so use like local thershold for every region depending on its neigh
    Thresholded_Img = cv.adaptiveThreshold(Gaussian_Img, 255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 21, 10)
    #3.La Placian
    laplacian = cv.Laplacian(Thresholded_Img, cv.CV_64F)
    # Convert data type from 64f to unsigned 8-bit integer
    laplacian = np.uint8(np.absolute(laplacian))
#     show_images([Gray_Scale_img,Gaussian_Img],['Gray Scale Imge','Guassian Sigma=1'])
#     show_images([Thresholded_Img,laplacian],['Thersholded Img','La Placian'])
    cv.imshow('Thresholded_img', Thresholded_Img)
    cv.waitKey(0)

    # Extract Table Region
    #Table takes most of the Region so Extract table by finding largest countor with 4 sides

    #1.Find Largest rectangle in the image
    # FIND CONTOUR
    contours, _ = cv.findContours(laplacian, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    #Identifying Contour with largest 4 sides
    table_contour, table_contour_approx = findLargestQuadrilateralContour(contours)
    if table_contour[0] is None:
        raise ValueError("No table detected.")
    print(table_contour_approx)
    
    # Sort points in clocwise order, compute table width and height
    table_pts, table_width, table_height =processContour(table_contour_approx[0])\

    #2.
    # EXTRACT TABLE REGION
    # Start with a full black image
    mask = np.zeros(Gray_Scale_img.shape).astype(Gray_Scale_img.dtype)
    # Create a mask for the table region
    cv.fillPoly(mask, table_contour, (255, 255, 255))
    
    # Apply the mask to the thresholded image, filling the region
    # outside of the table with white
    Extracted_table = cv.bitwise_and(Gray_Scale_img, mask)
    return Extracted_table

extracted_paper = Paper_Extraction('BC-1.jpg')

cv.imshow('Extracted Paper', extracted_paper)
cv.waitKey(0)
cv.destroyAllWindows()