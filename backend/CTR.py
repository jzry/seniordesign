from preprocessing.scorefields import CTRSegments
from OCR import okra
from OCR import violin as v


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


def run(args, image_buffer):
    """
    Runs all the image processing code for the CTR type scorecard.

    Parameters:
        args (dict): A dictionary containing the arguments:
                     'torchserve' (bool): A flag to specify whether TorchServe
                                          should be used or not.
        image_buffer (bytes): The raw image data.

    Returns:
        dict: A dictionary containing values and confidences for each
              score-field.
    """

    # Get the score field segments
    extracted_fields = CTRSegments(image_buffer)

    # Prepare the OCR
    dg = okra.DigitGetter(ts=args['torchserve'])

    output_dict = {}

    for field_num, key in enumerate(extracted_fields.keys()):

        if key == 'gut_sounds':
            continue

        raw_ouput = dg.image_to_digits(extracted_fields[key])

        num, conf = v.validate_score(raw_ouput, max_score_per_field[field_num])

        output_dict[out_field_keys[field_num]] = {'value': num, 'confidence': conf}

    return output_dict


def _debug_main():

    import sys
    from termcolor import colored

    if len(sys.argv) != 2:
        print('\n  Usage: python BCE.py <Path to image>\n')
        return

    try:
        with open(sys.argv[1], 'rb') as file:
            image_buffer = file.read()

    except FileNotFoundError:
        print(f'\n  Cannot open "{sys.argv[1]}"\n')
        return

    ret_val = run({'torchserve': False}, image_buffer)

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
    _debug_main()

