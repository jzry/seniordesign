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

    nums, confs = raw

    __remove_excess_decimals(nums, confs)

    if max_score is not None:

        if '.' in nums:

            int_part = nums.index('.')

            if int_part > 0:

                if max_score <= 9:
                    __enforce_one_digit_score(nums[:int_part], confs[:int_part], max_score - 1, min_score)
                else:
                    __enforce_two_digit_score(nums[:int_part], confs[:int_part], max_score - 1, min_score)

        else:

            if max_score <= 9:
                __enforce_one_digit_score(nums, confs, max_score, min_score)
            else:
                __enforce_two_digit_score(nums, confs, max_score, min_score)

    return (__stringify(nums), __overall_confidence(confs))


def validate_rider_number(raw):
    """
    Validates and auto-corrects a rider number field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    nums, confs = raw

    __remove_decimals(nums, confs)

    if len(nums) >= 3:

        nums[0] = 'L'
        confs[0] = 90.0

        if len(nums) > 3:
            __prune_to_length(nums, confs, 3)

    return (__stringify(nums), __overall_confidence(confs))


def validate_time(raw):
    """
    Validates and auto-corrects a time field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    nums, confs = raw

    __remove_decimals(nums, confs)

    if len(nums) > 4:
        __prune_to_length(nums, confs, 4)

    if len(nums) >= 2:

        nums[-2], confs[-2] = __force_into_range(nums[-2], confs[-2], 5)

        if len(nums) == 4:
            nums[0], confs[0] = __force_into_range(nums[0], confs[0], 2)

    return (__stringify(nums), __overall_confidence(confs))


def validate_weight(raw):
    """
    Validates and auto-corrects a weight field

    Parameters:
        raw (list, list): The raw output of the OCR.

    Returns:
        str: The corrected and stringified OCR output.
        float: The overall confidence percentage.
    """

    nums, confs = raw

    __remove_decimals(nums, confs)

    if len(nums) > 3:

        __trim_until(nums, confs, range(1, 4), 3)
        __prune_to_length(nums, confs, 3)

    if len(nums) == 3:
        nums[0], confs[0] = __force_into_range(nums[0], confs[0], 3, 1)


    return (__stringify(nums), __overall_confidence(confs))



def __remove_decimals(nums, confs):

    i = 0

    while i < len(nums):

        if nums[i] == '.':

            del nums[i]
            del confs[i]

        else:

            i += 1


def __remove_excess_decimals(nums, confs):

    num_decimals = nums.count('.')

    # remove trailing decimals
    while nums[-1] == '.':

        del nums[-1]
        del confs[-1]
        num_decimals -= 1

    if num_decimals > 1:

        best_decimal = -1
        i = 0

        while i < len(nums):

            if nums[i] == '.':

                if best_decimal == -1:
                    best_decimal = i

                elif confs[i] > confs[best_decimal]:

                    del nums[best_decimal]
                    del confs[best_decimal]
                    i -= 1
                    best_decimal = i

                else:

                    del nums[i]
                    del confs[i]
                    i -= 1

            i += 1


def __enforce_one_digit_score(nums, confs, max_val, min_value):

    __prune_to_length(nums, confs, 1)
    nums[0], confs[0] = __force_into_range(nums[0], confs[0], max_val, min_value)


def __enforce_two_digit_score(nums, confs, max_val, min_value):

    if len(nums) == 1:
        nums[0], confs[0] = __force_into_range(nums[0], confs[0], 9, min_value)

    else:

        __prune_to_length(nums, confs, 2)

        ones = max_val % 10
        tens = max_val // 10

        nums[0], confs[0] = __force_into_range(nums[0], confs[0], tens, 1)

        if nums[0] == tens:
            nums[1], confs[1] = __force_into_range(nums[1], confs[1], ones)



def __prune_to_length(nums, confs, length):

    while len(nums) > length:

        lowest_conf = -1

        for i in range(len(nums)):

            if isinstance(nums[i], int):

                if lowest_conf == -1:
                    lowest_conf = i

                elif confs[i] < confs[lowest_conf]:
                    lowest_conf = i

        if lowest_conf == -1:
            return

        del nums[lowest_conf]
        del confs[lowest_conf]


def __trim_until(nums, confs, stop_vals, stop_len=0):

    while nums[0] not in stop_vals:

        if len(nums) <= stop_len:
            break

        del nums[0]
        del confs[0]


def __force_into_range(num, conf, max_val, min_val=0):

    if num < min_val:

        num = min_val
        conf = min(conf, 100.0 / (max_val - (min_val - 1)))

    elif num > max_val:

        num = max_val
        conf = min(conf, 100.0 / (max_val - (min_val - 1)))

    return num, conf


def __stringify(nums):
    return ''.join(str(e) for e in nums)

def __overall_confidence(confs):
    return min(confs)

