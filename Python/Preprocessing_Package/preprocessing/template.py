# imports
# import cv2 as cv

BC_WIDTH = 2200
BC_HEIGHT = 1700

CTR_WIDTH = 1971
CTR_HEIGHT = 3169

# Global dictionary containing score field coordinates for each rider
BC_TEMPLATE_FIELDS = {
    "Rider1": {
        'Rider#': (363, 321, 95, 44),
        'recovery': (361, 510, 107, 49), # (x, y, width, height)
        'hydration': (361, 555, 107, 41),
        'lesions': (361, 594, 107, 41),
        'soundness': (361, 664, 107, 49),
        'qual_movement': (361, 711, 107, 41),
        'rider_time': (307, 971, 116, 44),
        'rider_weight': (307, 1310, 119, 44)
    },
    "Rider2": {
        'Rider#': (770, 321, 95, 44),
        'recovery': (768, 510, 107, 49),
        'hydration': (768, 555, 107, 41),
        'lesions': (768, 594, 107, 41),
        'soundness': (768, 664, 107, 49),
        'qual_movement': (768, 711, 107, 41),
        'rider_time': (714, 971, 116, 44),
        'rider_weight': (714, 1310, 119, 44)
    },
    "Rider3": {
        'Rider#': (1183, 321, 95, 44),
        'recovery': (1181, 510, 107, 49),
        'hydration': (1181, 555, 107, 41),
        'lesions': (1181, 594, 107, 41),
        'soundness': (1181, 664, 107, 49),
        'qual_movement': (1181, 711, 107, 41),
        'rider_time': (1127, 971, 116, 44),
        'rider_weight': (1127, 1310, 119, 44)
    },
    "Rider4": {
        'Rider#': (1590, 321, 95, 44),
        'recovery': (1588, 510, 107, 49),
        'hydration': (1588, 555, 107, 41),
        'lesions': (1588, 594, 107, 41),
        'soundness': (1588, 664, 107, 49),
        'qual_movement': (1588, 711, 107, 41),
        'rider_time': (1534, 971, 116, 44),
        'rider_weight': (1534, 1310, 119, 44)
    },
    "Rider5": {
        'Rider#': (2003, 321, 95, 44),
        'recovery': (2001, 510, 107, 49),
        'hydration': (2001, 555, 107, 41),
        'lesions': (2001, 594, 107, 41),
        'soundness': (2001, 664, 107, 49),
        'qual_movement': (2001, 711, 107, 41),
        'rider_time': (1947, 971, 116, 44),
        'rider_weight': (1947, 1310, 119, 44)
    },
}

CTR_TEMPLATE_FIELDS = {
    "initial_pulse_before": (1608, 1227, 115, 95), # (x, y, width, height)
    "initial_pulse_after": (1608, 1337, 120, 120),
    "mucous_membrane": (1607, 1587, 115, 42),
    "capillary_refill": (1607, 1630, 115, 40),
    "skin_pinch": (1607, 1674, 115, 40),
    "jugular_vein_refill": (1607, 1721, 115, 40),
    "gut_sounds": (1607, 1768, 115, 40),
    "anal_tone": (1607, 1925, 115, 88),
    "muscle_tone": (1606, 2020, 115, 40),
    "unwillingness_to_trot": (1606, 2071, 115, 40),
    "leg_injuries": (1607, 2120, 115, 120),
    "injury_interference": (1607, 2255, 115, 55),
    "lameness_grade1": (1607, 2340, 115, 80),
    "lameness_grade2": (1607, 2430, 115, 44),
    "back_stress": (1607, 2585, 115, 62),
    "tack_area": (1607, 2679, 115, 65),
    "hold_on_trail": (1728, 2777, 108, 40),
    "time_penalty": (1728, 2824, 108, 50)
}
