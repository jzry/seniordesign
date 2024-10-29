# imports
# import cv2 as cv

BC_WIDTH = 2839
BC_HEIGHT = 2103

# Global dictionary containing score field coordinates for each rider
BC_TEMPLATE_FIELDS = {
    "Rider1": {
        "Rider#": (456, 399, 149, 43),
        "recovery": (448, 642, 149, 43),  # (x, y, width, height)
        "hydration": (448, 690, 149, 43),
        "lesions": (448, 736, 149, 43),
        "soundness": (448, 828, 149, 43),
        "qual_movement": (448, 882, 149, 43),
        "rider_time": (403, 1204, 149, 43),
        "rider_weight": (403, 1622, 149, 43)
    },
    "Rider2": {
        "Rider#": (988, 407, 149, 43),
        "recovery": (971, 642, 149, 43),  # (x, y, width, height)
        "hydration": (982, 692, 149, 43),
        "lesions": (971, 742, 149, 43),
        "soundness": (971, 834, 149, 43),
        "qual_movement": (971, 882, 149, 43),
        "rider_time": (934, 1203, 149, 43),
        "rider_weight": (936, 1618, 149, 43)
    },
    "Rider3": {
        "Rider#": (1513, 409, 149, 43),
        "recovery": (1494, 648, 149, 43),  # (x, y, width, height)
        "hydration": (1494, 695, 149, 43),
        "lesions": (1505, 742, 149, 43),
        "soundness": (1494, 837, 149, 43),
        "qual_movement": (1494, 883, 149, 43),
        "rider_time": (1462, 1199, 149, 43),
        "rider_weight": (1464, 1615, 149, 43)
    },
    "Rider4": {
        "Rider#": (2032, 400, 149, 43),
        "recovery": (2028, 644, 149, 43),  # (x, y, width, height)
        "hydration": (2028, 692, 149, 43),
        "lesions": (2036, 741, 149, 43),
        "soundness": (2036, 834, 149, 43),
        "qual_movement": (2036, 882, 149, 43),
        "rider_time": (1999, 1199, 149, 43),
        "rider_weight": (1999, 1615, 149, 43)
    },
    "Rider5": {
        "Rider#":(2562, 398, 149, 43),
        "recovery": (2562, 641, 149, 43),  # (x, y, width, height)
        "hydration": (2562, 689, 149, 43),
        "lesions": (2562, 736, 149, 43),
        "soundness": (2562, 828, 149, 43),
        "qual_movement": (2562, 880, 149, 43),
        "rider_time": (2525, 1199, 149, 43),
        "rider_weight": (2520, 1620, 149, 43)
    },
}

CTR_TEMPLATE_FIELDS = {}

# def crop_field(image, x, y, w, h) :
#     cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
#     return image

# image = cv.imread('template-image.jpg')
# image = cv.resize(image, (BC_WIDTH, BC_HEIGHT))

# templated_bc_scores = {}
# recovery_score = crop_field(image, 122, 111, 38, 12)

# cv.imshow('Recovery Score', recovery_score)
# cv.waitKey(0)
# cv.destroyAllWindows()