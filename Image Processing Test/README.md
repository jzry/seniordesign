-------------------------
# Image Processing Test #
-------------------------

---------------------
# About and Purpose #
---------------------

This directory contains code for detecting the corners of scoresheets in images, processing them to ensure each is transformed into a standardized, flat rectangle. This correction prevents the images from appearing distorted, angled, or skewed and results in a clear presentation with black backgrounds. It also provides a numpy array containing the detected corner points for further analysis.

The purpose of this image preprocessor is to support Optical Character Recognition (OCR), which works by reading characters individually. In this project, the primary focus is on extracting numerical values from designated score boxes on the scoresheet for automated score calculations. The preprocessor enables the segmentor to focus on specific coordinates to extract fields with handwritten numbers. Once segmented, these fields are primed for OCR, allowing for seamless score computation based on extracted values.

---------------------
# Code Descriptions #
---------------------

# BC_Scoresheet_Image.py and CTR_Scoresheet_Image.py
Both the scripts are designed to extract and standardize a specific type of scoresheet from an image by detecting its corners and applying a perspective transformation to ensure the sheet appears flat and rectangular. It processes the image by converting it to grayscale, applying Gaussian blur, and adaptive thresholding, followed by detecting the largest quadrilateral contour. The script then sorts the corner points in clockwise order and uses helper functions from Common_Methods.py to resize and warp the image for a clear, sharp output. This prepares the image for further processing, such as segmentation or OCR.

# Common_Methods.py
The Common_Methods.py file contains essential helper functions for image processing tasks, including resizing images to fit screen dimensions, ordering contour points to ensure they follow a specific sequence (top-left, top-right, bottom-right, bottom-left), and applying a four-point perspective transformation to create a top-down view of selected areas. Additionally, it includes functions to verify if a set of points forms a proper rectangle and to determine screen resolution, ensuring images are displayed with optimal dimensions. These utilities support accurate contour detection, transformation, and display, facilitating streamlined processing in various image manipulation workflows.

# Scorefields.py
Scorefields.py provides two main functions, BCSegments() and CTRSegments(), which enable targeted extraction of score fields from specific regions of a scoresheet image. These functions support OCR processing by allowing the identification of fields for different score categories: BC and CTR. Each segment is visually marked, saved, and stored in a dictionary, preparing them for further processing and score calculation.

- BCSegments(): Extracts predefined fields for BC score sections from the scoresheet image.
Detects and marks each field in the BC section, displays each segment with green rectangles, and saves each marked segment in a dictionary.

- CTRSegments(): Similar to BCSegments(), this function targets CTR score sections.
It extracts each predefined CTR score field, displays, marks, and saves the fields for efficient OCR integration.
Both functions are designed to handle images with consistent scoresheet layouts, ensuring that extracted fields align correctly with OCR requirements

--------------
# How to use #
--------------

- Navigate to the directory containing the image preprocessing scripts.

- Ensure that all dependencies (OpenCV, Numpy, Python3, etc.) are installed.

- Open BC_ScoreSheet_Image.py or CTR_ScoreSheet_Image.py and ensure that the input filepath and filename for the image you want to process are set correctly. Modify the lines like ```filePath = "BC Scoresheet Pictures/" (or "CTR Scoresheet Pictures/")``` and ```fileName = "BC-1.jpg" (or "CTR-1.jpg)``` respectively. 

- Run the following commands in the terminal:
```Python3 BC_ScoreSheet_Image.py``` or ```Python3 CTR_ScoreSheet_Image.py``` to generate a standardized output of the scoresheet image.