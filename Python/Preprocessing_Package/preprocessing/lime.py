import cv2 as cv
import numpy as np



def BCAlignImage(image):
    """
    Aligns an extracted BC page with the template page.

    Parameters:
        image (numpy.ndarray): The image to align.

    Returns:
        numpy.ndarray: The aligned image.
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


    def fit_x(col, row_slice, step):
        """
        Repeatedly checks a column of pixels until a black pixel is found

        Parameters:
            col (int): The index of the starting column.
            row_slice (slice): A slice defining which rows to check.
            step (int): The direction col should be updated after each check.
                        This should be either +1 or -1.

        Returns:
            int: The index of the column in which the first black pixel
                 was found.
        """

        while thresh_image[row_slice, col].min() == 0:
            col += step

        while thresh_image[row_slice, col].min() != 0:
            col += step

        return col


    def fit_y(row, col_slice, step):
        """
        Repeatedly checks a row of pixels until a black pixel is found

        Parameters:
            row (int): The index of the starting row.
            col_slice (slice): A slice defining which columns to check.
            step (int): The direction row should be updated after each check.
                        This should be either +1 or -1.

        Returns:
            int: The index of the row in which the first black pixel
                 was found.
        """

        while thresh_image[row, col_slice].min() == 0:
            row += step

        while thresh_image[row, col_slice].min() != 0:
            row += step

        return row


    # Find the corners

    TL_X = fit_x(TL_X, slice(100, 800), +1)
    TL_Y = fit_y(TL_Y, slice(100, 800), +1)

    TR_X = fit_x(TR_X, slice(100, 800), -1)
    TR_Y = fit_y(TR_Y, slice(-800, -100), +1)

    BL_X = fit_x(BL_X, slice(-800, -100), +1)
    BL_Y = fit_y(BL_Y, slice(100, 800), -1)

    BR_X = fit_x(BR_X, slice(-800, -100), -1)
    BR_Y = fit_y(BR_Y, slice(-800, -100), -1)


    # Compute the scale between this image and the template image
    x_scale = image.shape[1] / 2200
    y_scale = image.shape[0] / 1700

    # Calculate the the locations of the template corners at the scale of this
    # image
    template_corners = np.float32([
        [100  * x_scale, 96   * y_scale],
        [2098 * x_scale, 100  * y_scale],
        [100  * x_scale, 1587 * y_scale],
        [2098 * x_scale, 1587 * y_scale]
    ])

    # Place the corner coordinates in a numpy array
    scanned_corners = np.float32([
        [TL_X, TL_Y],
        [TR_X, TR_Y],
        [BL_X, BL_Y],
        [BR_X, BR_Y]
    ])

    # Apply a perspective transformation to align the image
    M = cv.getPerspectiveTransform(scanned_corners, template_corners)
    image = cv.warpPerspective(image, M, (image.shape[1], image.shape[0]))


    # for c in template_corners:
    #     cv.circle(image, (int(c[0]), int(c[1])), radius=6, color=(0, 0, 255), thickness=-1)

    # resized = cv.resize(image, (0, 0), fx = 0.4, fy = 0.4, interpolation=cv.INTER_AREA)

    # cv.imwrite('corner.jpg', resized)
    # cv.imshow('image', resized)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


    return image

