import sys
import json
from contextlib import redirect_stdout
from os import devnull


def main():

    ret_val = {}

    if len(sys.argv) == 2:
    
        # The number of bytes to read from stdin
        input_length_bytes = int(sys.argv[1])

        # Read the image data from stdin
        image_buffer = sys.stdin.buffer.read(input_length_bytes)

        # Temporarily redirect stdout so random
        # messages aren't sent to Express
        with redirect_stdout(open(devnull, 'w')):

            print('ERROR if you see this message')

            ret_val = process_BCE(image_buffer)

    else:

        ret_val['error'] = 'Incorrect number of arguments'


    # Return the results as JSON through stdout
    print(json.dumps(ret_val))



# 
# Run all the code to process the BCE scoresheet
# 
def process_BCE(image_buffer):

    from preprocessing.scorefields import BCSegments
    from OCR import okra
    from OCR import violin as v

    extracted_fields = BCSegments(image_buffer)

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

    return output_dict

# 
# Helper function to insert outputs into the dictionary
# 
def insert_into_dict(dictionary, rider, field, output):

    num, conf = output

    dictionary[rider][field] = {'value': num, 'confidence': conf}


# Do It
main()
