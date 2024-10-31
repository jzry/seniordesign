#
# BCE Scoresheet Processing
#

######################### README #########################
#
# I put this file in the preprocessing folder for testing.
# Eventually, this code will be moved to the scanBCE.py
# file that is in the backend folder.
#


#
#
# Get the image from Express
#
#


# Import all modules
from scorefields import BCSegments
from OCR import okra
from OCR import violin as v

from contextlib import redirect_stdout
from os import devnull
from pathlib import Path



def insert_into_dict(dictionary, rider, field, output):

    num, conf = output

    dictionary[rider][field] = {'value': num, 'confidence': conf}


with redirect_stdout(open(devnull, 'w')):

    # Obtain the score fields
    extracted_fields = BCSegments(Path('bc') / 'BC-1.jpg')


    # Prepare the OCR
    dg = okra.DigitGetter()

    rider_keys = extracted_fields.keys()
    output_dict = dict.fromkeys(rider_keys, {})

    for rider_key in rider_keys:

        output_dict[rider_key] = dict.fromkeys(extracted_fields[rider_key].keys())

        #
        # Dictionary   <--   OCR validation   <--   OCR   <--   Image Segments
        #

        insert_into_dict(output_dict, rider_key, 'Rider#',        v.validate_rider_number(dg.image_to_digits(extracted_fields[rider_key]['Rider#'])))

        insert_into_dict(output_dict, rider_key, 'recovery',      v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['recovery']),      10, 1))
        insert_into_dict(output_dict, rider_key, 'hydration',     v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['hydration']),     10, 1))
        insert_into_dict(output_dict, rider_key, 'lesions',       v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['lesions']),       10, 1))
        insert_into_dict(output_dict, rider_key, 'soundness',     v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['soundness']),     10, 1))
        insert_into_dict(output_dict, rider_key, 'qual_movement', v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['qual_movement']), 10, 1))

        insert_into_dict(output_dict, rider_key, 'rider_time',    v.validate_time(dg.image_to_digits(extracted_fields[rider_key]['rider_time'])))
        insert_into_dict(output_dict, rider_key, 'rider_weight',  v.validate_weight(dg.image_to_digits(extracted_fields[rider_key]['rider_weight'])))


print(output_dict)

#
#
# Return output_dict to Express as JSON
#
#

