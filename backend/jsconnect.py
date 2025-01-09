import sys
import json
from contextlib import redirect_stdout, redirect_stderr
from os import devnull


def main():

    # Receive from parent process
    image_buffer, scorecard_type, torchserve_flag = receive()

    result = {}

    # Temporarily redirect stdout and stderr so random
    # messages aren't sent to the parent process
    #
    with open(devnull, 'w') as null_device:
        with redirect_stdout(null_device):
            with redirect_stderr(null_device):

                print('ERROR if you see this message')

                if scorecard_type == 'ctr':
                    from CTR import process_CTR
                    result = process_CTR(image_buffer, torchserve_flag)

                else:
                    from BCE import process_BCE
                    result = process_BCE(image_buffer, torchserve_flag)

    # Send to parent process
    send(result)


def receive():
    """
    Receives image data and parameters from the parent JavaScript process.

    Parameters:
        None

    Returns:
        bytes: A byte array storing an image.
        str: A string with the scorecard type ("ctr" or "bce")
        bool: A flag to specify whether TorchServe should be used or not.

    Raises:
        ValueError: Invalid command line arguments.
    """

    if len(sys.argv) == 4:

        try:
            # The first argument is the number of bytes to read from stdin
            input_length_bytes = int(sys.argv[1])

        except ValueError:
            raise ValueError('Expected first argument to be an integer')

        if input_length_bytes <= 0:
            raise ValueError('Expected first argument to be positive')


        # The second argument specifies the type of scorecard
        card_type = sys.argv[2].lower()

        if card_type != 'ctr' and card_type != 'bce':
            raise ValueError(f'Expected second argument to be "ctr" or "bce"; Received "{card_type}"')

        # The third argument specifies whether TorchServe should be used
        torchserve_flag = sys.argv[3] == 'torchserve'

        # Read the image data from standard input
        image_buffer = sys.stdin.buffer.read(input_length_bytes)

        return image_buffer, card_type, torchserve_flag

    else:
        raise ValueError(f'Expected 3 command line arguments; Received {sys.argv - 1}')


def send(data):
    """
    Sends JSON data to the parent JavaScript process.

    Parameters:
        data (dict): The response data stored in a dictionary object.

    Returns:
        None
    """

    # Convert the dictionary to a JSON string
    # and return through standard output
    print(json.dumps(data))


# Run It
main()

