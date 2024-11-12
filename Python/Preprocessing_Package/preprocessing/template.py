# imports
# import cv2 as cv

BC_WIDTH = 2200
BC_HEIGHT = 1700

CTR_WIDTH = 1971
CTR_HEIGHT = 3169

# Global dictionary containing score field coordinates for each rider
BC_TEMPLATE_FIELDS = {
    "Rider1": {
        "Rider#": (363, 327, 95, 32),
        "recovery": (361, 516, 107, 37),  # (x, y, width, height)
        "hydration": (361, 561, 107, 29),
        "lesions": (361, 600, 107, 29),
        "soundness": (361, 670, 107, 37),
        "qual_movement": (361, 717, 107, 29),
        "rider_time": (307, 977, 116, 32),
        "rider_weight": (307, 1316, 119, 32)
    },
    "Rider2": {
        'Rider#': (770, 327, 95, 32),
        'recovery': (768, 516, 107, 37),
        'hydration': (768, 561, 107, 29),
        'lesions': (768, 600, 107, 29),
        'soundness': (768, 670, 107, 37),
        'qual_movement': (768, 717, 107, 29),
        'rider_time': (714, 977, 116, 32),
        'rider_weight': (714, 1316, 119, 32)
    },
    "Rider3": {
        'Rider#': (1183, 327, 95, 32),
        'recovery': (1181, 516, 107, 37),
        'hydration': (1181, 561, 107, 29),
        'lesions': (1181, 600, 107, 29),
        'soundness': (1181, 670, 107, 37),
        'qual_movement': (1181, 717, 107, 29),
        'rider_time': (1127, 977, 116, 32),
        'rider_weight': (1127, 1316, 119, 32)
    },
    "Rider4": {
        'Rider#': (1590, 327, 95, 32),
        'recovery': (1588, 516, 107, 37),
        'hydration': (1588, 561, 107, 29),
        'lesions': (1588, 600, 107, 29),
        'soundness': (1588, 670, 107, 37),
        'qual_movement': (1588, 717, 107, 29),
        'rider_time': (1534, 977, 116, 32),
        'rider_weight': (1534, 1316, 119, 32)
    },
    "Rider5": {
        'Rider#': (2003, 327, 95, 32),
        'recovery': (2001, 516, 107, 37),
        'hydration': (2001, 561, 107, 29),
        'lesions': (2001, 600, 107, 29),
        'soundness': (2001, 670, 107, 37),
        'qual_movement': (2001, 717, 107, 29),
        'rider_time': (1947, 977, 116, 32),
        'rider_weight': (1947, 1316, 119, 32)
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
