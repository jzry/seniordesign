-------------------------
# Image Processing Test #
-------------------------

---------------------
# About and Purpose #
---------------------

This directory contains code for detecting the corners of scoresheets in images, processing them to ensure each is transformed into a standardized, flat rectangle. This correction prevents the images from appearing distorted, angled, or skewed and results in a clear presentation with black backgrounds.

The purpose of this image preprocessor is to support Optical Character Recognition (OCR), which works by reading characters individually. In this project, the primary focus is on extracting numerical values from designated score boxes on the scoresheet for automated score calculations. The preprocessor enables the segmentor to focus on specific coordinates to extract fields with handwritten numbers. Once segmented, these fields are primed for OCR, allowing for seamless score computation based on extracted values.

---------------------
# Code Descriptions #
---------------------

# scoresheet.py
The scripts are designed to extract and standardize a specific type of scoresheet from an image by detecting its corners and applying a perspective transformation to ensure the sheet appears flat and rectangular. It processes the image by converting it to grayscale, applying Gaussian blur, and adaptive thresholding, followed by detecting the largest quadrilateral contour. The script then sorts the corner points in clockwise order to resize and warp the image for a clear, sharp output. This prepares the image for further processing, such as segmentation or OCR.

# scorefields.py
scorefields.py provides two main functions, BCSegments() and CTRSegments(), which enable targeted extraction of score fields from specific regions of a scoresheet image. These functions support OCR processing by allowing the identification of fields for different score categories: BC and CTR. Each segment is visually marked, saved, and stored in a dictionary, preparing them for further processing and score calculation.

- BCSegments(): Extracts predefined fields for BC score sections from the scoresheet image.
Detects and marks each field in the BC section, displays each segment with green rectangles, and saves each marked segment in a dictionary.

- CTRSegments(): Similar to BCSegments(), this function targets CTR score sections.
It extracts each predefined CTR score field, displays, marks, and saves the fields for efficient OCR integration.
Both functions are designed to handle images with consistent scoresheet layouts, ensuring that extracted fields align correctly with OCR requirements

--------------
# How to use #
--------------

- Ensure that all dependencies (OpenCV, Numpy, Python3, etc.) are installed, it is useful to make a virtual environment (venv) in the directory of the code that you're testing so that you can delete these installations once you're done using them. Refer to: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments for instructions on setting up a virtual environment to test out. Make sure to delete the .venv before pushing code again because we don't want to upload .venv to the repo.

- main.py is the file that you will use to extract the scoresheet from an image and to simultaneously extract the segments from the warped image. In main.py, "fileName" is the file that you want to extract the information out of, "filePath" is the path of the file location.

- To extract the file and segment out the scorecards, do: ```python3 main.py```.