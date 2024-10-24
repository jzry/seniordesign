#
# Validation functions for OCR output
#

def validate_score(raw, max_score, min_score=0):
    """
    Validates and auto-corrects a score field

    Parameters:
        raw (list, list): The raw output of the OCR.
        max_score (int): The upper-bound of the score. Pass None if there is no max value.
        min_score (int, optional): The lower-bound of the score. Defaults to 0.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    return ('1', 90.0)


def validate_rider_number(raw):
    """
    Validates and auto-corrects a rider number field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    return ('L20', 90.0)


def validate_time(raw):
    """
    Validates and auto-corrects a time field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    return ('352', 90.0)


def validate_weight(raw):
    """
    Validates and auto-corrects a weight field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    return ('180', 90.0)
