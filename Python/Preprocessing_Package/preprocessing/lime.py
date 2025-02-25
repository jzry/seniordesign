import cv2 as cv
import numpy as np

from . import template
from .exceptions import PreprocessingAlignmentError


def BCAlignImage(image):
    """
    Aligns an extracted BC page with the template page.

    Parameters:
        image (numpy.ndarray): The image to align.

    Returns:
        numpy.ndarray: The aligned image.
    """

    try:

        # Locate the template corners
        scanned_corners = __find_corners_BCE(image)

    except PreprocessingAlignmentError:

        print('Warning: preprocessing.lime failed to align the image.')

        # If we can't find the corners, return the original image
        return image

    # Compute the scale between this image and the template image
    x_scale = image.shape[1] / template.BC_WIDTH
    y_scale = image.shape[0] / template.BC_HEIGHT

    # Calculate the the locations of the template corners at the scale of this
    # image
    template_corners = np.float32([
        [100  * x_scale, 96   * y_scale],
        [2098 * x_scale, 100  * y_scale],
        [100  * x_scale, 1587 * y_scale],
        [2098 * x_scale, 1587 * y_scale]
    ])

    # Apply a perspective transformation to align the image
    M = cv.getPerspectiveTransform(scanned_corners, template_corners)
    image = cv.warpPerspective(image, M, (image.shape[1], image.shape[0]))

    return image


def CTRAlignImage(image):
    """
    Aligns an extracted CTR page with the template page.

    Parameters:
        image (numpy.ndarray): The image to align.

    Returns:
        numpy.ndarray: The aligned image.
    """

    try:

        # Locate the template corners
        scanned_corners = __find_corners(image)

    except PreprocessingAlignmentError:

        print('Warning: preprocessing.lime failed to align the image.')

        # If we can't find the corners, return the original image
        return image

    # Compute the scale between this image and the template image
    x_scale = image.shape[1] / template.CTR_WIDTH
    y_scale = image.shape[0] / template.CTR_HEIGHT

    # Calculate the the locations of the template corners at the scale of this
    # image
    template_corners = np.float32([
        [117  * x_scale, 69   * y_scale],
        [1583 * x_scale, 64   * y_scale],
        [117  * x_scale, 2748 * y_scale],
        [1584 * x_scale, 2749 * y_scale]
    ])

    # Apply a perspective transformation to align the image
    M = cv.getPerspectiveTransform(scanned_corners, template_corners)
    image = cv.warpPerspective(image, M, (image.shape[1], image.shape[0]))

    return image


def __find_corners_BCE(image):
    """
    Locates the template corners of a BCE page. These are the four corners of
    the box that fits the grid layout of the scoresheet.

    Parameters:
        image (numpy.ndarray): The image of the page.

    Returns:
        numpy.ndarray: An array with shape (4, 2) containing the coordinates of
                       the four corners.

    Raises:
        PreprocessingAlignmentError: Unable to locate all corners.
   """

    # Create grayscale version of the image
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a threshold. We should pick a threshold value to reduce noise on
    # the page's margin as much as possible. If handwriting quality is reduced,
    # we don't really care.
    thresh = image.min() + ((image.max() - image.min()) // 2)
    _, thresh_image = cv.threshold(gray_image, thresh, 255, cv.THRESH_BINARY)

    line_points = __get_vertical_line_points(thresh_image)


    for point in line_points:
        cv.circle(image, point, radius=10, color=(0, 0, 255), thickness=-1)
    # Adjust fx and fy to fit your screen
    resized = cv.resize(image, (0, 0), fx = 0.4, fy = 0.4, interpolation=cv.INTER_AREA)
    cv.imshow('points', resized)
    cv.waitKey(0)
    cv.destroyAllWindows()

    #
    #
    # TODO: Use "line_points" to find the template corners
    #
    #

    # Place the corner coordinates in a numpy array
    # scanned_corners = np.float32([
    #     [TL_X, TL_Y],
    #     [TR_X, TR_Y],
    #     [BL_X, BL_Y],
    #     [BR_X, BR_Y]
    # ])

    # print(scanned_corners)

    # return scanned_corners

    # For testing, exit to save time
    import sys
    sys.exit(0)


def __get_vertical_line_points(image):
    """
    Finds the coordinates of the four vertical lines in a BCE scoresheet.

    Parameters:
        image (numpy.ndarray): The thresholded image of the page.

    Returns:
        numpy.ndarray: An array with shape (4, 2) containing four coordinates
                       that lie on the four lines.

    Raises:
        PreprocessingAlignmentError: The line points could not be found.
    """

    # The index of the middle row
    middle = image.shape[0] // 2

    # Use 5% margins on the left and right edges to avoid noise
    margin = int(image.shape[1] * 0.05)
    columns = slice(margin, -margin)

    # The starting row
    row = image[middle, columns]

    for next_row_i in range(middle + 1, image.shape[0]):

        row = np.logical_or(row, image[next_row_i, columns])
        x_points = __get_line_x(row)

        if len(x_points) == 4:
            # Found them!
            break

        elif len(x_points) < 4:
            raise PreprocessingAlignmentError('Failed to find vertical lines!')

    if len(x_points) > 4:
        raise PreprocessingAlignmentError('Failed to find vertical lines!')

    line_points = np.array([
        [margin + x_points[0], middle],
        [margin + x_points[1], middle],
        [margin + x_points[2], middle],
        [margin + x_points[3], middle]
    ])

    return line_points


def __get_line_x(img_row):
    """
    Returns the x-coordinates of lines in the image row slice.

    Parameters:
        img_row (numpy.ndarray): A row slice from the image being processed.

    Returns:
        list: The x-coordinates of the lines.
    """

    x_points = []
    line_flag = False

    for i in range(len(img_row)):

        if line_flag:

            # A value of True indicates a background pixel
            if img_row[i]:
                line_flag = False

        else:

            # A value of False indicates a line pixel
            if not img_row[i]:
                x_points.append(i)
                line_flag = True

    return x_points



def __find_corners(image):
    """
    Locates the corners of the page inside the margins.

    Parameters:
        image (numpy.ndarray): The image of the page.

    Returns:
        numpy.ndarray: An array with shape (4, 2) containing the coordinates of
                       the four corners.

    Raises:
        PreprocessingAlignmentError: Unable to locate all corners.
    """

    # Create grayscale version of the image
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a threshold. We should pick a threshold value to reduce
    # noise on the page's margin as much as possible. If handwriting and text
    # quality is reduced, we don't really care.
    thresh = image.min() + ((image.max() - image.min()) // 2)
    _, thresh_image = cv.threshold(gray_image, thresh, 255, cv.THRESH_BINARY)

    # Starting coordinates for the corners

    TL_X = 0
    TL_Y = 0

    TR_X = thresh_image.shape[1] - 1
    TR_Y = 0

    BL_X = 0
    BL_Y = thresh_image.shape[0] - 1

    BR_X = thresh_image.shape[1] - 1
    BR_Y = thresh_image.shape[0] - 1


    # Find the corners

    TL_X = __fit_x(thresh_image, TL_X, slice(100, 800), +1)
    TL_Y = __fit_y(thresh_image, TL_Y, slice(100, 800), +1)

    TR_X = __fit_x(thresh_image, TR_X, slice(100, 800), -1)
    TR_Y = __fit_y(thresh_image, TR_Y, slice(-800, -100), +1)

    BL_X = __fit_x(thresh_image, BL_X, slice(-800, -100), +1)
    BL_Y = __fit_y(thresh_image, BL_Y, slice(100, 800), -1)

    BR_X = __fit_x(thresh_image, BR_X, slice(-800, -100), -1)
    BR_Y = __fit_y(thresh_image, BR_Y, slice(-800, -100), -1)

    # Place the corner coordinates in a numpy array
    scanned_corners = np.float32([
        [TL_X, TL_Y],
        [TR_X, TR_Y],
        [BL_X, BL_Y],
        [BR_X, BR_Y]
    ])

    return scanned_corners


def __fit_x(image, col, row_slice, step):
    """
    Repeatedly checks a column of pixels until a black pixel is found

    Parameters:
        image (numpy.ndarray): A thresholded version of the image being
                               aligned.
        col (int): The index of the starting column.
        row_slice (slice): A slice defining which rows to check.
        step (int): The direction col should be updated after each check.
                    This should be either +1 or -1.

    Returns:
        int: The index of the column in which the first black pixel
             was found.

    Raises:
        PreprocessingAlignmentError: Unable to locate corner x-coordinate.
    """

    while image[row_slice, col].min() == 0:

        col += step

        if col >= image.shape[1] or col < 0:
            raise PreprocessingAlignmentError(
                'Unable to find x-coordinate of corner'
            )

    while image[row_slice, col].min() != 0:

        col += step

        if col >= image.shape[1] or col < 0:
            raise PreprocessingAlignmentError(
                'Unable to find x-coordinate of corner'
            )

    return col


def __fit_y(image, row, col_slice, step):
    """
    Repeatedly checks a row of pixels until a black pixel is found

    Parameters:
        image (numpy.ndarray): A thresholded version of the image being
                               aligned.
        row (int): The index of the starting row.
        col_slice (slice): A slice defining which columns to check.
        step (int): The direction row should be updated after each check.
                    This should be either +1 or -1.

    Returns:
        int: The index of the row in which the first black pixel
             was found.

    Raises:
        PreprocessingAlignmentError: Unable to locate corner y-coordinate.
    """

    while image[row, col_slice].min() == 0:

        row += step

        if row >= image.shape[0] or row < 0:
            raise PreprocessingAlignmentError(
                'Unable to find y-coordinate of corner'
            )

    while image[row, col_slice].min() != 0:

        row += step

        if row >= image.shape[0] or row < 0:
            raise PreprocessingAlignmentError(
                'Unable to find y-coordinate of corner'
            )

    return row
