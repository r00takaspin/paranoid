#-*- coding: UTF-8 -*-
__author__ = 'voldemar'

import unittest

from detector import Detector
from camera import Camera
import cv

from mock import MagicMock

class testDetector(unittest.TestCase):
    """тестируем детектор"""

    def setUp(self):
        self.camera = Camera()
        self.camera.get_storage = MagicMock(return_value=cv.CreateMemStorage())

    def testDetectFace(self):
        detector = Detector(self.camera)
        self.assertTrue(detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg")))

    def testNotDetect(self):
        detector = Detector(self.camera)
        self.assertEqual(detector.detect(cv.LoadImageM("tests/samples/bad/orange.jpeg")),False)

    def testMontion(self):
        detector = Detector(self.camera)
        detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg"))
        detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg"))
        self.assertEqual(detector.detect_move(),False)
        detector.detect(cv.LoadImageM("tests/samples/good/gaga.jpeg"))
        self.assertTrue(detector.detect_move())

if __name__ == '__main__':

    unittest.main()