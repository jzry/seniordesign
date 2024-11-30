import numpy as np
import cv2
from enum import Enum
import requests
import json

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_ENABLED = True
except ImportError:
    MATPLOTLIB_ENABLED = False


class DigitGetter:
    """
    A basic OCR class that only recognizes numbers.

    Attributes:
        debug_images (bool): Output the input image after the preprocessing
                             stage (default=False).
        column_skip (int): The number of image columns to be skipped each loop
                           of the scan (default=2).
        fraction_padding (float): The minimum fractional percentage of the
                                  segmented image's height or width that
                                  should be padding (default=0.2).
        find_decimal_points (bool): Determines whether or not decimal points
                                    will appear in the output (default=True).
        find_minus_signs (bool): Determines whether or not minus signs will
                                 appear in the output (default=False).
    """

    def __init__(self, debug=False):
        """Creates a new instance of DigitGetter"""

        self.__debug = debug

        if debug:

            from .OkraHandler import OkraHandler            
            
            self.__model_handle = OkraHandler()
            self.__model_handle.initialize()

        # Set default attributes
        
        self.debug_images = False
        self.column_skip = 2
        self.fraction_padding = 0.2
        self.find_decimal_points = True
        self.find_minus_signs = False
        self.blank_threshold = 120


    def __preprocess_image(self, img):
        """
        Prepares an image for OCRing.

        Parameters:
            img (numpy.ndarray): The image to process.

        Returns:
            numpy.ndarray: The processed image.
        """

        # Convert to grayscale
        if img.ndim == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # If there is a number in the image, there
        # will be a large difference between the
        # brightest pixel and the darkest pixel
        if (img.max() - img.min() <= self.blank_threshold):
            raise Exception

        # Apply a slight blur
        img = cv2.bilateralFilter(img, 5, self.blank_threshold, 20)

        # Apply threshold
        _, img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # Perform dilation to make digits stand out better
        img = cv2.dilate(img, (3, 3), iterations=1)

        self.__show_debug_image(img, 'Pre-processed Image')

        return img


    def digit_from_image(self, img):
        """
        Extracts a single digit from an image.

        Parameters:
            img (numpy.ndarray): An image containing a single digit.

        Returns:
            (int, float): A tuple with the digit's value and the confidence as
                          a percentage.
        """

        try:
            img = self.__preprocess_image(img)
        except:
            return (None, None)

        return self.__digit_from_image(img)


    def __digit_from_image(self, img):
        """
        Extracts a single digit from an image (no pre-processing).

        Parameters:
            img (numpy.ndarray): An image containing a single digit.

        Returns:
            (int, float): A tuple with the digit's value and the confidence as
                          a percentage.
        """

        self.__show_debug_image(img, 'Digit')
        
        req = {"data": img.tobytes(), "x": img.shape[1], "y": img.shape[0]}

        if self.__debug:

            res = self.__model_handle.handle(req)
            body = json.loads(res[0])

        else:

            res = requests.post('http://localhost:6060/predictions/OkraClassifier', data=req)
            body = res.json()

            if res.status_code != 200:
                print(body)
                raise Exception('Torchserve error')

        return (body['Digit'], body['Confidence'])


    def image_to_digits(self, img):
        """
        Extracts a line of digits from an image.

        Parameters:
            img (numpy.ndarray): An image containing some digits.

        Returns:
            (list(int), list(float)): A tuple with a list of digit values and
                                      a list of confidences as percentages.
        """

        try:
            img = self.__preprocess_image(img)
        except:
            return ([], [])

        # The return values
        numbers = []
        confidence = []

        # A dictionary to save the state of the scan
        scan_state = {}

        # Loop until the scan returns 'None'
        while True:

            digit_pixel = self.__scan_columns(img, scan_state)

            if digit_pixel == None:
                break

            # Get the slice of the image containing the digit
            segment, segment_type = self.__segment_digit(img, digit_pixel, scan_state)

            if segment_type == SegmentType.DIGIT:

                # Classify the digit
                num, conf = self.__digit_from_image(segment)
                numbers.append(num)
                confidence.append(conf)

            elif segment_type == SegmentType.DECIMAL:

                if self.find_decimal_points:
                    conf = self.__get_decimal_confidence(segment.shape)
                    numbers.append('.')
                    confidence.append(conf)

                self.__show_debug_image(segment, 'Decimal Point')

            elif segment_type == SegmentType.MINUS:

                if self.find_minus_signs:
                    conf = 100.0 - self.__get_decimal_confidence(segment.shape)
                    numbers.append('-')
                    confidence.append(conf)

                self.__show_debug_image(segment, 'Minus Symbol')

            else:

                self.__show_debug_image(segment, 'Ignored')

        return (numbers, confidence)


    def __scan_columns(self, img, scan_state):
        """
        Scans the columns of an image to find digits.

        Parameters:
            img (numpy.ndarray): An image containing some digits.
            scan_state (dict): A dictionary object to save the state of the
                               scan between calls. This should be {} on the
                               first call.

        Returns:
            (int, int): The coordinates of the first digit pixel encountered.
            None: No digits found.
        """

        if scan_state == {}:

            scan_state['column'] = 0

            scan_state['upper'] = [0]
            scan_state['lower'] = [img.shape[0]]
            scan_state['upper_stop'] = [img.shape[1]]
            scan_state['lower_stop'] = [img.shape[1]]


        # x is the current column
        # y is the current row

        x = scan_state['column']

        while x < img.shape[1]:

            while scan_state['upper_stop'][-1] < x:

                del scan_state['upper'][-1]
                del scan_state['upper_stop'][-1]

            while scan_state['lower_stop'][-1] < x:

                del scan_state['lower'][-1]
                del scan_state['lower_stop'][-1]

            upper = scan_state['upper'][-1]
            lower = scan_state['lower'][-1]

            for y in range(upper, lower):

                # Handwriting will have a non-zero value.
                # The background has a value of 0.
                if img[y, x] != 0:

                    scan_state['column'] = x
                    return (x, y)

            # Move to the next column
            x = x + self.column_skip + 1

        return None


    def __segment_digit(self, img, start_pixel, scan_state):
        """
        Segments out a single digit from an image.

        Parameters:
            img (numpy.ndarray): An image.
            start_pixel (int, int): The coordinate of the starting pixel.
            scan_state (dict): A dictionary object to save the state of the
                               scan between function calls.

        Returns:
            (numpy.ndarray, SegmentType): A tuple with a slice of img
                                          containing a single digit and the
                                          type of segment.
        """

        bounds = Boundary(start_pixel[1], start_pixel[0], start_pixel[1], start_pixel[0])

        # Find the actual boundary of the digit.
        # 'bounds' will be updated with the correct values.
        self.__trace_digit(img, bounds, start_pixel)

        # Update the scan state
        if bounds.bottom < img.shape[0] // 2:

            scan_state['upper'].append(bounds.bottom + 1)
            scan_state['upper_stop'].append(bounds.right)

        elif bounds.top > img.shape[0] // 2:

            scan_state['lower'].append(bounds.top)
            scan_state['lower_stop'].append(bounds.right)

        else:
            scan_state['column'] = bounds.right + 1

        # Figure out whats in this segment based on its size and shape
        segment_type = self.__get_segment_type(bounds.shape(), img.shape)

        # Copy the box containing the digit from the image
        digit_segment = bounds.get_slice(img)

        # Only apply padding if this is a digit
        if segment_type == SegmentType.DIGIT:
            digit_segment = self.__apply_padding(digit_segment)

        return (digit_segment, segment_type)


    def __trace_digit(self, img, bounds, pixel):
        """
        An edge tracing algorithm that finds the smallest box that fits a
        digit.

        Parameters:
            img (numpy.ndarray): An image.
            bounds (Boundary): The object to store the bounds of the digit.
            pixel (int, int): The coordinate of the starting pixel.
        """

        def move(direction):

            move_val = directions[direction % len(directions)]
            return (current_pixel[0] + move_val[0], current_pixel[1] + move_val[1])

        def in_bounds(location):

            if location[0] < 0 or location[0] >= img.shape[1]:
                return False
            if location[1] < 0 or location[1] >= img.shape[0]:
                return False

            return True

        def is_white(location):

            return img[location[1], location[0]] != 0

        def update_bounds(location):

            if location[0] > bounds.right:
                bounds.right = location[0]
            elif location[0] < bounds.left:
                bounds.left = location[0]

            if location[1] > bounds.bottom:
                bounds.bottom = location[1]
            elif location[1] < bounds.top:
                bounds.top = location[1]

        def get_start_direction(direction):

            direction = direction % len(directions)

            if direction < 2:
                return 6        # Left
            elif direction < 4:
                return 0        # Up
            elif direction < 6:
                return 2        # Right
            else:
                return 4        # Down

        #                .         .                                                 .
        #                |        /       __.      \       |        /      .__        \
        #                                           '      '       '
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

        start_direction = 0    # Up

        current_pixel = pixel

        while True:

            for next_direction in range(start_direction, start_direction + len(directions)):

                next_pixel = move(next_direction)

                if in_bounds(next_pixel):
                    if is_white(next_pixel):

                        update_bounds(next_pixel)
                        start_direction = get_start_direction(next_direction)
                        current_pixel = next_pixel
                        break

            if current_pixel == pixel:
                break


    def __get_segment_type(self, segment_shape, img_shape):
        """
        Determines the contents of a segment based on its size and shape.

        Parameters:
            segment_shape (int, int): The shape of the segment.
            img_shape (int, int): The shape of the original image.

        Returns:
            SegmentType: The type of the segment.
        """

        if img_shape[0] > img_shape[1]:
            size_criteria = img_shape[0] // 2

        else:
            size_criteria = img_shape[0]

        digit_min_height = size_criteria // 3
        noise_max_size = size_criteria // 7

        # Is this tall enough to be a digit?
        if segment_shape[0] >= digit_min_height:
            return SegmentType.DIGIT

        # Is this really small?
        if segment_shape[0] < noise_max_size and segment_shape[1] < noise_max_size:
            return SegmentType.NOISE

        # Is this flat and long?
        if segment_shape[1] >= segment_shape[0] * 1.75:
            return SegmentType.MINUS

        # It's probably a decimal if we reach here
        return SegmentType.DECIMAL


    def __apply_padding(self, img):
        """
        Adds padding around an image. The resulting image will be very close
        to being square in shape.

        Parameters:
            img (numpy.ndarray): The image to pad.

        Returns:
            numpy.ndarray: The padded image.
        """

        fixed_padding = int(max(img.shape) * self.fraction_padding)

        # This will be the size of the image after padding
        largest_dim = max(img.shape) + 2 * fixed_padding

        # This is how much padding will be needed to make the image a square
        dynamic_padding = int((largest_dim - min(img.shape)) / 2)

        dynamic_pad = (dynamic_padding, dynamic_padding)
        fixed_pad = (fixed_padding, fixed_padding)

        # If the y dimension is smaller the x dimension
        #     then use the dynamic pad on the y dimension (add more rows than columns)
        #
        # If the x dimension is smaller the y dimension
        #     then use the dynamic pad on the x dimension (add more columns than rows)
        #
        if (img.shape[0] <= img.shape[1]):
            img = np.pad(img, (dynamic_pad, fixed_pad))
        else:
            img = np.pad(img, (fixed_pad, dynamic_pad))

        return img


    def __get_decimal_confidence(self, segment_shape):
        """
        Computes a confidence value for a decimal based on how round it is.

        Parameters:
            segment_shape (int, int): The shape of the image segment
                                      containing the decimal point.

        Returns:
            float: The confidence as a percentage.
        """

        # Divide the smaller dimension by the larger dimension
        # Multiply by 100 to convert to percentage
        percentage = 100.0 * min(segment_shape) / max(segment_shape)

        return percentage


    def __show_debug_image(self, img, title):
        """Helper function to display a matplotlib plot of an image"""

        if self.__debug:
            if self.debug_images:
                if MATPLOTLIB_ENABLED:

                    plt.imshow(img)
                    plt.title(title)
                    plt.show()

                else:

                    print('Warning: matplotlib is not configured')


class Boundary:
    """
    A class for storing the location of an image slice.

    Attributes:
        top (int): The index of the top edge.
        right (int): The index of the right edge.
        bottom (int): The index of the bottom edge.
        left (int): The index of the left edge.
    """

    def __init__(self, top, right, bottom, left):
        """Creates a new instance of Boundary"""

        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


    def shape(self):
        return (self.bottom - self.top + 1, self.right - self.left + 1)


    def get_slice(self, img):
        """
        Returns a slice of an image within the boundary.

        Parameters:
            img (numpy.ndarray): An image.

        Returns:
            numpy.ndarray: A slice of img.
        """

        # Adjust the edges if necessary
        self.fit_image(img)

        # Return a slice
        return img[self.top:(self.bottom + 1), self.left:(self.right + 1)]


    def fit_image(self, img):
        """
        Adjusts the boundary to fit within an image.

        Parameters:
            img (numpy.ndarray): An image.
        """

        # Make sure there are no negative edges

        if self.top < 0:
            self.top = 0

        if self.right < 0:
            self.right = 0

        if self.bottom < 0:
            self.bottom = 0

        if self.left < 0:
            self.left = 0

        # Make sure the edges are within the image

        if self.top >= img.shape[0]:
            self.top = img.shape[0] - 1

        if self.right >= img.shape[1]:
            self.right = img.shape[1] - 1

        if self.bottom >= img.shape[0]:
            self.bottom = img.shape[0] - 1

        if self.left >= img.shape[1]:
            self.left = img.shape[1] - 1


class SegmentType(Enum):
    """
    An enumerated type to differentiate between digits, minus symbols,
    decimals, and noise.

    Values:
        NOISE = 0   : A few disconnected pixels that should be ignored.
        DIGIT = 1   : A digit that should be passed to the classifier.
        MINUS = 2   : A minus symbol that will likely be ignored.
        DECIMAL = 3 : A decimal point.
    """

    NOISE = 0
    DIGIT = 1
    MINUS = 2
    DECIMAL = 3

