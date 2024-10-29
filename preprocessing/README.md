# Preprocessing

## About

This directory holds all the relevant code for identifying the corners of a scoresheet from an image and processing it so that every image is standardized in a flat rectangle. Instead of the scoresheets appearing at an angle or distorted with background noise, they will all be processed to be clear with a black background and a numpy array of the corners is returned.

## Purpose

Having an image preprocessor is necessary for the Optical Character Recognition (OCR) program because the OCR is only able to identify one character at a time, so breaking down the letters inside an image is necessary. However, in our implementation we aren't concerned about all the words inside an image, we're concerned about the numerical values in specific locations on a scoresheet so that we can use those numerical values to generate a score.

The preprocessor will allow the segmentor to go to generalized coordinates of where a score box *should* be and it will extract the handwritten characters from that box. Once the characters are extracted, they can be used to automatically calculate a score for the box.

## Functions

- Read the input
- Convert to gray
- Gaussian blur
- Otsu threshold
- Morphology open/close to clean up the threshold
- Get largest contour
- Approximate a polygon from the contour
- Get the corners
- Draw the polygon on the input
- Compute side lengths
- Compute output corresponding corners
- Get perspective transformation matrix from corresponding corner points
- Warp the input image according to the matrix
- Save the results

# Segmentor

## About and Purpose

Every scoresheet that we are processing has the same exact structure, so our segmentor will be able to go to specific coordinates on a page and identify a box from that general zone. It is general because our preprocessor will not be able to process the image perfectly every time, so our program will have to look within a radius range to identify the four corners of a box and use that to extract the image. The segmentor will then take that box and preprocess what's inside to make sure we are only taking the handwritten numerical value inside of that.

## Functions

- Search within a box range (using the numpy corners as the whole scoresheet) to locate the box for each BC and CTR score box.
- Then apply the same functions as above to find the coordinates to a specific box and create a flattened output for the Okra OCR Classifier.

# How to use

**WARNING:** Running the preprocessor will create several images of the warped scoresheet and running the segmentor will create an image output for every score category.

1. Go into the preprocessor directory on your command line.
2. Make sure all dependencies are installed (OpenCV, Numpy, Python3, etc) that preprocessor.py and segmentor.py use.
3. In preprocessor.py and segmentor.py you have to make sure that you are processing the correct file, so in preprocessor.py, make sure the following lines at the top are set to the filepath and filename for the image you want to process. Change the lines ```filePath = "test_input/"``` ```fileName = "bc1.jpeg"``` at the top of preprocessor.py and ```filePath = "test_output/"``` ```fileName = "bc1out.jpg"```. You can also change the directory of where the output appears if you want by changing ```fileOutPath = "your_output_directory"```.
3. Enter ```Python3 preprocessor.py``` in your command line to create an standardized output of a scoresheet image.
4. Enter ```Python3 segmentor.py``` in your command line to create the output of the scoresheet boxes for each score category.

## Image Processing OpenCV Documentation

https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html

## Preprocessor.py

This is the first version of the preprocessor. It doesn't use canny or convex hull to find the perimeter of a page.

## Preprocessor2.py

This is the second version of the preprocessor. It uses canny and convex hull to create an outline to a page.

## Problems with preprocessor:

- We need an adaptable preprocessor that is able to adapt when there is a white page on a light background, a white page on a dark background, a white pack on a background with a lot of noise, etc.
- The outliner is incorrectly drawing corners from the lines on the page, to fix this we need to eliminate all the words on the page before trying to find the corner. Need to experiment with different ways to solve this.

## Code credits:

https://stackoverflow.com/questions/60941012/how-do-i-find-corners-of-a-paper-when-there-are-printed-corners-lines-on-paper-i
https://stackoverflow.com/questions/67644977/recognizing-corners-page-with-opencv-partialy-fails