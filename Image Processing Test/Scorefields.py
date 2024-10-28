# Imports
import numpy as np
import cv2 as cv
import ScoreSheet_Image as img
import Template as bc_temp

"""
Function Brief: Extracts and marks predefined segments (fields) for each rider section on an image. 
                It draws rectangles on each defined field, displaying them and saving each segment in a dictionary.
Parameters:
    image (str): Path to the source image from which segments need to be extracted.

Returns:
    extracted_fields (dict): A dictionary containing each rider's section with marked field images.
"""
def BCSegments(image):
    extracted_fields = {}
    extracted_image = "output.jpg"
    image = cv.imread(extracted_image)
    image = cv.resize(image, (bc_temp.BC_WIDTH, bc_temp.BC_HEIGHT))

    for rider, fields in bc_temp.BC_TEMPLATE_FIELDS.items():
        extracted_fields[rider] = {}
        
        for field_name, (x, y, w, h) in fields.items():
            field_image = cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the extracted field image
            extracted_fields[rider][field_name] = field_image

    cv.imwrite("Segmentation.jpg", field_image)

    return extracted_fields
        
BC_score_fields = BCSegments('output.jpg')