import sys
import json
import contextlib
import os

ret_val = {}

if len(sys.argv) == 2:
 
    # The number of bytes to read from stdin
    input_size = int(sys.argv[1])

    ret_val['length'] = input_size
    ret_val['output'] = ''

    # Read the image data from stdin
    val = sys.stdin.buffer.read(input_size)

    # Temporarily redirect stdout so random
    # messages aren't sent to Express
    with contextlib.redirect_stdout(open(os.devnull, 'w')):

        print('ERROR if you see this message')

        #
        # Run actual Segmentation / OCR code here
        #

        for i in range(input_size):

            if i > 10:
                break

            ret_val['output'] += f'{val[i]:2x} '

else:

    ret_val['error'] = 'Incorrect number of arguments'


# Return the results as JSON through stdout
print(json.dumps(ret_val))

