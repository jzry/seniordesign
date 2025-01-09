from preprocessing.scorefields import BCSegments
from OCR import okra
from OCR import violin as v


def process_BCE(image_buffer, torchserve):
    """
    Runs all the image processing code for the BCE type scorecard.

    Parameters:
        image_buffer (bytes): The raw image data.
        torchserve (bool): A flag to specify whether TorchServe should be used
                           or not.

    Returns:
        dict: A dictionary containing score-field values and confidences for
              each rider.
    """

    extracted_fields = BCSegments(image_buffer)

    # Prepare the OCR
    dg = okra.DigitGetter(ts=torchserve)

    rider_keys = extracted_fields.keys()
    output_dict = {}

    for rider_key in rider_keys:

        output_dict[rider_key] = {}

        #
        # Dictionary   <--   OCR validation   <--   OCR   <--   Image Segments
        #

        insert_into_dict(output_dict, rider_key, 'Rider number',        v.validate_rider_number(dg.image_to_digits(extracted_fields[rider_key]['Rider#'])))

        insert_into_dict(output_dict, rider_key, 'Recovery',      v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['recovery']),      10, 1))
        insert_into_dict(output_dict, rider_key, 'Hydration',     v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['hydration']),     10, 1))
        insert_into_dict(output_dict, rider_key, 'Lesions',       v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['lesions']),       10, 1))
        insert_into_dict(output_dict, rider_key, 'Soundness',     v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['soundness']),     10, 1))
        insert_into_dict(output_dict, rider_key, 'Qual Mvmt', v.validate_score(dg.image_to_digits(extracted_fields[rider_key]['qual_movement']), 10, 1))

        insert_into_dict(output_dict, rider_key, 'Ride time, this rider',    v.validate_time(dg.image_to_digits(extracted_fields[rider_key]['rider_time'])))
        insert_into_dict(output_dict, rider_key, 'Weight of this rider',  v.validate_weight(dg.image_to_digits(extracted_fields[rider_key]['rider_weight'])))

    return { 'data': output_dict, 'status': 0 }


#
# Helper function to insert outputs into the dictionary
#
def insert_into_dict(dictionary, rider, field, output):

    num, conf = output

    dictionary[rider][field] = {'value': num, 'confidence': conf}


def debug_main():

    from termcolor import colored
    from pathlib import Path

    filename = 'BC-1.jpg'

    full_path = Path(__file__).parent.parent / 'Python' / 'Preprocessing_Package' / 'preprocessing' / 'bc' / filename

    with open(full_path, 'rb') as file:
        image_buffer = file.read()

    ret_val = process_BCE(image_buffer, False)['data']

    for rider_key in ret_val.keys():

        print(colored(f'----------- {rider_key}', color='blue', attrs=['bold']))

        for key in ret_val[rider_key].keys():

            if ret_val[rider_key][key]['confidence'] >= 90.0:
                print(key, colored(ret_val[rider_key][key]['value'], color='green', attrs=['bold']))
            elif ret_val[rider_key][key]['confidence'] >= 80.0:
                print(key, colored(ret_val[rider_key][key]['value'], color='yellow', attrs=['bold']))
            elif ret_val[rider_key][key]['value'] == '':
                print(colored(key, color='red', attrs=['bold']))
            else:
                print(key, colored(ret_val[rider_key][key]['value'], color='red', attrs=['bold']))


if __name__ == '__main__':
    debug_main()
