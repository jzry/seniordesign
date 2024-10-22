import unittest
import numpy as np

import OCR.okra as okra


class DigitGetterTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.dg = okra.DigitGetter()

    def test_column_scan(self):
        
        # Don't use column skipping for this test
        self.dg.column_skip = 0
        
        img = np.array([
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ])
        
        first_pixel = self.dg._DigitGetter__scan_columns(img, 0)
        self.assertEqual(first_pixel, (0, 0), 'Did not find the first pixel')
        
        second_pixel = self.dg._DigitGetter__scan_columns(img, 1)
        self.assertEqual(second_pixel, (3, 3), 'Did not find the second pixel')
        
        third_pixel = self.dg._DigitGetter__scan_columns(img, 4)
        self.assertIsNone(third_pixel, 'Should return None for no pixels found')

    def test_trace_digit(self):
        
        img = np.array([
            [0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 1, 0, 1]
        ])
        
        boundary = okra.Boundary(2, 2, 2, 2)
        
        self.dg._DigitGetter__trace_digit(img, boundary, (2, 2))
        
        self.assertEqual(boundary.top, 1, 'Top boundary incorrect')
        self.assertEqual(boundary.bottom, 4, 'Bottom boundary incorrect')
        self.assertEqual(boundary.left, 1, 'Left boundary incorrect')
        self.assertEqual(boundary.right, 4, 'Right boundary incorrect')
        
    def test_get_segment_type(self):
        
        img_shape = (46, 156)
        
        seg_type = self.dg._DigitGetter__get_segment_type((40, 39), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.DIGIT, 'Digit segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((46, 35), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.DIGIT, 'Digit segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((7, 7), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.DECIMAL, 'Decimal segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((11, 8), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.DECIMAL, 'Decimal segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((10, 32), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.MINUS, 'Minus segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((9, 21), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.MINUS, 'Minus segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((1, 7), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.NOISE, 'Noise segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((0, 0), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.NOISE, 'Noise segment not indentified correctly')
        
        seg_type = self.dg._DigitGetter__get_segment_type((2, 1), img_shape)
        self.assertEqual(seg_type, okra.SegmentType.NOISE, 'Noise segment not indentified correctly')

