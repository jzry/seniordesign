# Imports
import os
import numpy as np
import cv2 as cv
import template
from scoresheet import Paper_Extraction

"""
Function Brief: Extracts and marks predefined segments (fields) for each rider section on an image. 
                It draws rectangles on each defined field, displaying them and saving each segment in a dictionary.
Parameters:
    image (str): Path to the source image from which segments need to be extracted.

Returns:
    extracted_fields (dict): A dictionary containing each rider's section with marked field images.
"""
def BCSegments(image):

    '''Just for the sake of verfiy the output
    -------------------------------------------'''
    output_folder='cropped_fields'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    '''-------------------------------------------'''

    extracted_fields = {}
    
    # imread() when image is file path
    # extracted_image = cv.imread(image)
    extracted_image = Paper_Extraction(image)

    # # Check if the result is an integer indicating failure
    if isinstance(extracted_image, int) and extracted_image == -1:
        print("Error: Cannot read image file after extraction.")
        return -1
    else:
        # Get, Check and Resize(if needed) dimensions of extracted_image
        height, width = extracted_image.shape[:2]
        if(height != template.BC_HEIGHT and width != template.BC_WIDTH) :
            extracted_image = cv.resize(extracted_image, (template.BC_WIDTH, template.BC_HEIGHT))

    
    
    '''Just for the sake of verfiy the output
    ------------------------------------------------------------------'''
    marked_image = extracted_image.copy()
    '''------------------------------------------------------------------'''


    for rider, fields in template.BC_TEMPLATE_FIELDS.items():
        extracted_fields[rider] = {}

        '''Just for the sake of verfiy the output
        ------------------------------------------------------------------'''
        # Create a subfolder for each rider to organize output
        rider_folder = os.path.join(output_folder, rider)
        if not os.path.exists(rider_folder):
            os.makedirs(rider_folder)
        '''------------------------------------------------------------------'''
        
        for field_name, (x, y, w, h) in fields.items():
            
            field_image = extracted_image[y:y + h, x:x + w]

            '''Just for the sake of verfiy the output
            ------------------------------------------------------------------'''
            # Save each cropped image to the specified folder
            field_path = os.path.join(rider_folder, f"{field_name}.jpg")
            cv.imwrite(field_path, field_image)

            # mark the fields on the image
            field_image = cv.rectangle(marked_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            '''------------------------------------------------------------------'''

            # Save the extracted field image
            extracted_fields[rider][field_name] = field_image
    
    '''Just for the sake of verfiy the output
    ------------------------------------------------------------------'''
    if cv.imwrite('outfield.jpg', marked_image):
        print(f"Extraction complete. Output saved to {marked_image}")
    '''------------------------------------------------------------------'''
    return extracted_fields
        
# BC_score_fields = BCSegments('output_extraction.jpg')