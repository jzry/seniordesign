# Imports
import numpy as np
import cv2 as cv
# import BC_Scoresheet_Image as bc_img
# import BC_Template as bc_temp
# import CTR_Scoresheet_Image as ctr_img
# import CTR_Template as ctr_temp

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

    for rider, fields in bc_temp.TEMPLATE_FIELDS.items():
        extracted_fields[rider] = {}

        extracted_image = bc_img.BC_Paper_Extraction(image)
        
        for field_name, (x, y, w, h) in fields.items():
            field_image = cv.rectangle(extracted_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the extracted field image
            extracted_fields[rider][field_name] = field_image

            cv.imshow(f"{rider} - {field_name}", field_image)
            cv.waitKey(0)
            cv.destroyAllWindows()

    return extracted_fields
        
# BC_score_fields = BCSegments('bc/BC-1.jpg')