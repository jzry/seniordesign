import cv2 as cv
import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from pillow_heif import register_heif_opener

"""
Function Brief: Checks the file extension of an image file. If the extension is not one of the allowed types 
                (jpg, jpeg, png, bmp, tif, tiff), the function converts the image to JPG format and saves it
                with a .jpg extension.

Parameters:
    file_path (str): Path to the image file to be checked and potentially converted.

Returns:
    new_file_path (str): Path to the image file, either the original path (if the extension was allowed) 
                         or the path to the converted JPG file.
"""
def checkExtension(image_path):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff'}

    extension = image_path.split('.')[-1].lower()

    # Check if the file extension is in the allowed list
    if extension not in allowed_extensions:
        print(f"File extension '.{extension}' is not supported. Converting to JPG...")

        if extension == 'heic' or extension == 'HEIC':

            # Register HEIF opener with Pillow
            register_heif_opener()

            # Open the HEIC file using Pillow
            image = Image.open(image_path)

            # Convert the image to a numpy array that OpenCV can use
            img_np = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)

            # Define the new file path
            new_file_path = os.path.splitext(image_path)[0] + '.jpg'
            cv.imwrite(new_file_path, img_np)

        if extension == 'pdf' or extension == 'PDF':

            # Convert the PDF to images
            images = convert_from_path(image_path)

            # Save the images as JPG files
            new_file_path = os.path.splitext(image_path)[0] + '.jpg'
            image.save(new_file_path, 'JPEG')

        return new_file_path
    else:
        print(f"File extension '.{extension}' is supported.")
        return image_path