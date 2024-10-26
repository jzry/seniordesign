# imports
import cv2 as cv

BC_WIDTH = 760
BC_HEIGHT = 584

# Global dictionary containing score field coordinates for each rider
BC_TEMPLATE_FIELDS = {
    "Rider1": {
        "Rider#": (122, 111, 38, 12),
        "recovery": (120, 175, 40, 15),  # (x, y, width, height)
        "hydration": (120, 188, 40, 15),
        "lesions": (120, 203, 40, 15),
        "soundness": (120, 230, 40, 15),
        "qual_movement": (120, 243, 40, 15),
        "rider1_time": (108, 330, 40, 15),
        "rider1_weight": (108, 450, 40, 15)
    },
    "Rider2": {
        "Rider#": (265, 114, 38, 12),
        "recovery": (260, 175, 40, 15),  # (x, y, width, height)
        "hydration": (263, 191, 40, 15),
        "lesions": (260, 203, 40, 15),
        "soundness": (260, 230, 40, 15),
        "qual_movement": (260, 243, 40, 15),
        "rider2_time": (250, 330, 40, 15),
        "rider2_weight": (250, 450, 40, 15)
    },
    "Rider3": {
        "Rider#": (405, 115, 38, 12),
        "recovery": (400, 180, 40, 15),  # (x, y, width, height)
        "hydration": (400, 193, 40, 15),
        "lesions": (403, 205, 40, 15),
        "soundness": (400, 230, 40, 15),
        "qual_movement": (400, 245, 40, 15),
        "rider3_time": (390, 333, 40, 15),
        "rider3_weight": (390, 450, 40, 15)
    },
    "Rider4": {
        "Rider#": (544, 115, 38, 12),
        "recovery": (543, 180, 40, 15),  # (x, y, width, height)
        "hydration": (543, 193, 40, 15),
        "lesions": (545, 205, 40, 15),
        "soundness": (545, 230, 40, 15),
        "qual_movement": (545, 245, 40, 15),
        "rider4_time": (535, 333, 40, 15),
        "rider4_weight": (535, 450, 40, 15)
    },
    "Rider5": {
        "Rider#":(685, 115, 38, 12),
        "recovery": (687, 178, 40, 15),  # (x, y, width, height)
        "hydration": (687, 193, 40, 15),
        "lesions": (687, 205, 40, 15),
        "soundness": (687, 230, 40, 15),
        "qual_movement": (687, 245, 40, 15),
        "rider5_time": (677, 333, 40, 15),
        "rider5_weight": (676, 452, 40, 15)
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