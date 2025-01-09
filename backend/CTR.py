from preprocessing.scorefields import CTRSegments
from OCR import okra
from OCR import violin as v


def process_CTR(image_buffer, torchserve):
    """
    Runs all the image processing code for the CTR type scorecard.

    Parameters:
        image_buffer (bytes): The raw image data.
        torchserve (bool): A flag to specify whether TorchServe should be used
                           or not.

    Returns:
        dict: A dictionary containing values and confidences for each
              score-field.
    """

    extracted_fields = CTRSegments(image_buffer)

    # Prepare the OCR
    dg = okra.DigitGetter(ts=torchserve)

    field_keys = extracted_fields.keys()

    output_dict = {}

    max_score_per_field = [5, 5, 5, 5, 5, 3, 0, 2, 5, 5, 20, 5, 10, 25, 5, 5, None, None]
    out_field_keys = [
        'Pulse Before Trot Out',
        'Pulse After Trot Out',
        'Mucous Membrane',
        'Capillary Refill',
        'Skin Pinch',
        'Jugular Vein Refill',
        'Gut Sounds',
        'Anal Tone',
        'Muscle Tone',
        'Unwillingness to trot',
        'Tendons, Ligaments, Joints, Filings',
        'Interferences',
        'Grade 1',
        'Grade 2',
        'Back Tenderness',
        'Tack Area',
        'Hold on Trail',
        'Time Penalty'
    ]

    for i, key in enumerate(field_keys):

        if key == 'gut_sounds':
            continue

        #
        # Dictionary   <--   OCR validation   <--   OCR   <--   Image Segments
        #

        raw_ouput = dg.image_to_digits(extracted_fields[key])

        num, conf = v.validate_score(raw_ouput, max_score_per_field[i])

        output_dict[out_field_keys[i]] = {'value': num, 'confidence': conf}

    return { 'data': output_dict, 'status': 0 }


def debug_main():

    from termcolor import colored
    from pathlib import Path

    filename = 'CTR-1.jpg'

    full_path = Path(__file__).parent.parent / 'Python' / 'Preprocessing_Package' / 'preprocessing' / 'ctr' / filename

    with open(full_path, 'rb') as file:
        image_buffer = file.read()

    ret_val = process_CTR(image_buffer, False)['data']

    for key in ret_val.keys():

        if key == 'gut_sounds':
            continue

        if ret_val[key]['confidence'] >= 90.0:
            print(key, colored(ret_val[key]['value'], color='green', attrs=['bold']))
        elif ret_val[key]['confidence'] >= 80.0:
            print(key, colored(ret_val[key]['value'], color='yellow', attrs=['bold']))
        elif ret_val[key]['value'] == '':
            print(colored(key, color='red', attrs=['bold']))
        else:
            print(key, colored(ret_val[key]['value'], color='red', attrs=['bold']))


if __name__ == '__main__':
    debug_main()

