import torch
import torchvision.transforms as transforms
import numpy as np
import cv2
import matplotlib.pyplot as plt
from OkraClassifier import OkraClassifier

class DigitGetter:
    """
    A basic OCR class that only works with numbers

    Attributes:
        debug_images (bool): Output the input image after the preprocessing stage (default=False)
        column_skip (int): The number of image columns to be skipped each loop of the scan
    """

    def __init__(self):
        """Creates a new instance of DigitGetter"""

        # Load model
        self.__model = OkraClassifier()
        state_dict = torch.load('./okra3.model.weights', weights_only=True)
        self.__model.load_state_dict(state_dict)
        self.__model.to('cpu')
        self.__model.eval()

        # Set default attributes
        self.debug_images = False
        self.column_skip = 5

        self.segment_padding_hori = 30
        self.segment_padding_vert = 20


    def __preprocess_image(self, img):
        """
        Prepares an image for OCRing

        Parameters:
            img (numpy.ndarray): The image to process

        Returns:
            numpy.ndarray: The processed image
        """

        # Apply a slight blur
        kernel = np.ones((3,3), np.float32) / 50
        img = cv2.filter2D(img, -1, kernel)

        # Calculate a threshold value based on the darkest and brightest pixels
        threshold = int(img.min() + (img.max() / 2))

        # Apply threshold
        _, img = cv2.threshold(
            img,
            threshold,
            255,
            cv2.THRESH_BINARY_INV
        )

        # Show debugging image
        if self.debug_images:
            plt.imshow(img)
            plt.show()

        return img


    def digit_from_image(self, img):
        """
        Extracts a single digit from an image

        Parameters:
            img (numpy.ndarray): An image containing a single digit

        Returns:
            (int, float): A tuple with the digit's value and the confidence as a percentage
        """

        img = self.__preprocess_image(img)
        return self.__digit_from_image(img)


    def __digit_from_image(self, img):
        """
        Extracts a single digit from an image (no pre-processing)

        Parameters:
            img (numpy.ndarray): An image containing a single digit

        Returns:
            (int, float): A tuple with the digit's value and the confidence as a percentage
        """

        # Covert the numpy array to a torch tensor.
        # Resize it to 28x28 (This is the size of the MNIST images).
        transform = transforms.Compose([transforms.ToTensor(), transforms.Resize((28, 28))])
        img = transform(img)

        # Show debugging image
        if self.debug_images:
            plt.imshow(img[0].numpy())
            plt.show()

        # Adds two dimensions to the 28x28 img so it "fits" into the model.
        # This doesn't actually alter the data; it basically adds extra brackets around the array
        img = img.reshape((1, 1, 28, 28))

        # Run the model with the image
        results = self.__model(img)

        # Convert the results into probabilities
        probabilities = torch.nn.functional.softmax(results[0], dim=0)

        # The index with the highest probability is the predicted value
        digit_value = torch.argmax(probabilities)
        confidence = probabilities[digit_value] * 100

        return (digit_value.item(), confidence.item())


    def image_to_digits(self, img):
        """
        Extracts a line of digits from an image

        Parameters:
            img (numpy.ndarray): An image containing some digits

        Returns:
            (list(int), list(float)): A tuple with a list of digit values and a list of confidences as percentages
        """

        img = self.__preprocess_image(img)

        # The return values
        numbers = []
        confidence = []

        # Start with the image's first column
        current_column = 0

        # Loop until the scan returns 'None'
        while True:

            digit_pixel = self.__scan_columns(img, current_column)

            if digit_pixel == None:
                break

            # Get the slice of the image containing the digit
            digit_segment, current_column = self.__segment_digit(img, digit_pixel)

            # Classify the digit
            num, conf = self.__digit_from_image(digit_segment)
            numbers.append(num)
            confidence.append(conf)

        return (numbers, confidence)


    def __scan_columns(self, img, start_column):
        """
        Scans the columns of an image to find digits

        Parameters:
            img (numpy.ndarray): An image containing some digits
            start_column (int): The column index to start at

        Returns:
            (int, int): The coordinates of the first digit pixel encountered
            None: No digits found
        """

        # x is the current column
        # y is the current row

        x = start_column

        while x < img.shape[1]:
            for y in range(img.shape[0]):

                # Handwriting will have a value of 255
                # The background has a value of 0
                if img[y, x] != 0:
                    return (x, y)

            # Move to the next column
            x = x + self.column_skip + 1

        return None


    def __segment_digit(self, img, start_pixel):
        """
        Segments out a single digit from an image

        Parameters:
            img (numpy.ndarray): An image
            start_pixel (int, int): The coordinate of the starting pixel

        Returns:
            (numpy.ndarray, int): A tuple with a slice of img containing a single digit and the adjacent column's index
        """

        bounds = Boundary(start_pixel[1], start_pixel[0], start_pixel[1], start_pixel[0])

        # Find the actual boundary of the digit
        self.__fill_digit(img, bounds, start_pixel)

        # The next column will be the column to the right of the segment
        next_column = bounds.right + 1

        # Add padding around the digit
        bounds.top -= self.segment_padding_vert
        bounds.right += self.segment_padding_hori
        bounds.bottom += self.segment_padding_vert
        bounds.left -= self.segment_padding_hori

        return (bounds.get_slice(img), next_column)


    def __fill_digit(self, img, bounds, pixel):
        """
        A recursive, space fill, search algorithm thing...

        Parameters:
            img (numpy.ndarray): An image
            bounds (Boundary): The currently known boundary of the digit
            pixel (int, int): The coordinate of the current pixel
        """

        x = pixel[0]
        y = pixel[1]

        # Check if we're in bounds
        if x < 0 or x >= img.shape[1]:
            return
        if y < 0 or y >= img.shape[0]:
            return

        # Check if this is part of the background
        if img[y,x] == 0:
            return

        # Check if we've been here before
        if img[y,x] == 254:
            return

        # Mark this spot (Changing the color by 1 shouldn't hurt anything)
        img[y,x] = 254

        # Adjust the boundary
        if x > bounds.right:
            bounds.right = x
        elif x < bounds.left:
            bounds.left = x

        if y > bounds.bottom:
            bounds.bottom = y
        elif y < bounds.top:
            bounds.top = y

        # Move to the surrounding pixels
        for move_x in [-1, 0, 1]:
            for move_y in [-1, 0, 1]:
                self.__fill_digit(img, bounds, (x + move_x, y + move_y))


class Boundary:
    """
    A class for storing the location of an image slice

    Attributes:
        top (int): The index of the top edge
        right (int): The index of the right edge
        bottom (int): The index of the bottom edge
        left (int): The index of the left edge
    """

    def __init__(self, top, right, bottom, left):
        """Creates a new instance of Boundary"""

        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


    def get_slice(self, img):
        """
        Returns a slice of an image within the boundary

        Parameters:
            img (numpy.ndarray): An image

        Returns:
            numpy.ndarray: A slice of img
        """

        # Adjust the edges if necessary
        self.fit_image(img)

        # Return a slice
        return img[self.top:(self.bottom + 1), self.left:(self.right + 1)]


    def fit_image(self, img):
        """
        Adjusts the boundary to fit within an image

        Parameters:
            img (numpy.ndarray): An image
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

