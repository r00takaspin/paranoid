#-*- coding: UTF-8 -*-
__author__ = 'voldemar'

import unittest

from detector.detector import Detector,HaarDetector,HaarManager
from camera import Camera
import cv

from mock import MagicMock

class testDetector(unittest.TestCase):
    """тестируем детектор"""

    def setUp(self):
        self.camera = Camera()
        self.camera.get_storage = MagicMock(return_value=cv.CreateMemStorage())
        self.detector = Detector(self.camera)

    def testDetectFace(self):
        """тест который детектирует два произвольных лица"""
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg")))
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/face_rec.jpg")))

    def testDetectProfile(self):
        """тест на поиск профиля"""
        detector = HaarManager().get_detector('profile')
        self.assertTrue(detector.detect(cv.LoadImageM("tests/samples/good/profile1.jpg")))

    def testIgnoreChair(self):
        """тест на игнорирование предметов похожих на человеческий силуэт"""
        self.assertEquals(self.detector.detect(cv.LoadImageM("tests/samples/bad/chair.jpg")),False)

    def testBowedHead(self):
        """тест на поиск лица когда голова наклонена"""
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/bowed_head.jpg")))

    def testHeadAndHand(self):
        """тестируем детектирование когда человек поднес руку к лицу"""

        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/head_and_hand1.jpg")))
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/head_and_hand2.jpg")))
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/head_and_hand3.jpg")))
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/head_and_hand4.jpg")))

    def testAtTheCorner(self):
        """в кадре только часть лица"""
        self.assertTrue(self.detector.detect(cv.LoadImageM("tests/samples/good/at_the_corner.jpg")))

    def testNotDetect(self):
        self.assertEqual(self.detector.detect(cv.LoadImageM("tests/samples/bad/orange.jpeg")),False)

    def testDetect_Move(self):
        """детектируем изменение положения найденных объектов"""
        self.detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg"))
        self.detector.detect(cv.LoadImageM("tests/samples/good/swe.jpg"))
        self.assertEqual(self.detector.detect_move(),False)
        self.detector.detect(cv.LoadImageM("tests/samples/good/gaga.jpeg"))
        self.assertTrue(self.detector.detect_move())


    def testHaarManager(self):
        face_detector = HaarManager().get_detector('face');
        self.assertTrue(isinstance(face_detector,HaarDetector))

if __name__ == '__main__':

    unittest.main()