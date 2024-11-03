# Imports
import cv2 as cv
import os

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

        image = cv.imread(image_path)

        # Define the new file path
        new_file_path = os.path.splitext(image_path)[0] + '.jpg'
        cv.imwrite(new_file_path, image)

        return new_file_path
    else:
        print(f"File extension '.{extension}' is supported.")
        return image_path

