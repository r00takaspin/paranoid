#-*- coding: UTF-8 -*-
from camera import Camera
import cv
import time

class Detector():
    """
    обертка для opencv, отвечает за распознавание человека, сидящего за монитором
    """
    _modify_time = False
    _camera = None
    _detection_time = False
    _what_was_detected = None
    _current_picture = None
    _last_coord = {}
    _prev_coord = {}

    def __init__(self,camera):
        self._camera = camera

    #TODO:эта функция требует рядя рефакторингв
    def detect(self):
        """
        производим последовательный поиск любого из элементов: глаз, лица, плеч и головы
        """
        start_time = time.time()
        self._detection_time = False
        self._what_was_detected = None

        self._current_picture = self._camera.take_picture()

        cascade = cv.Load('haar_xml/haarcascade_frontalface_alt.xml')
        faces = cv.HaarDetectObjects(self._current_picture, cascade,self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50,50))

        if faces:
            self._what_was_detected = 'face'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_coord = self._last_coord.copy()
            self._last_coord['faces'] = faces
            '''
            for face in faces:

                cv.Rectangle(grayscale,(face[0][0],face[0][1]),
                    (face[0][0]+face[0][2],face[0][1]+face[0][3]),
                    cv.RGB(155, 55, 200),2)
                cv.ShowImage("Camera", grayscale)
            '''
            return True


        cascade = cv.Load('haar_xml/haarcascade_profileface.xml')
        profiles = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))

        if profiles:
            self._what_was_detected = 'profile'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_coord = self._last_coord.copy()
            self._last_coord['profiles'] = profiles
            '''
            for face in faces:

                cv.Rectangle(grayscale,(face[0][0],face[0][1]),
                    (face[0][0]+face[0][2],face[0][1]+face[0][3]),
                    cv.RGB(155, 55, 200),2)
                cv.ShowImage("Camera", grayscale)
            '''
            return True

        cascade = cv.Load('haar_xml/hs.xml')
        hs = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,22))

        if hs:
            self._what_was_detected = 'hs'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_coord = self._last_coord.copy()
            self._last_coord['hs'] = hs
            """
            for hs_i in hs:

                cv.Rectangle(self._current_picture,(hs_i[0][0],hs_i[0][1]),
                    (hs_i[0][0]+hs_i[0][2],hs_i[0][1]+hs_i[0][3]),
                    cv.RGB(155, 55, 200),2)
                cv.ShowImage("Camera", self._current_picture)
            """
            return True
            #cv.ShowImage("Camera", grayscale)

        cascade = cv.Load('haar_xml/haarcascade_mcs_upperbody.xml')
        ub = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,22))

        if ub:
            self._what_was_detected = 'upper body'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_coord = self._last_coord.copy()
            self._last_coord['ub'] = ub

            '''
            for hs_i in hs:

                cv.Rectangle(grayscale,(hs_i[0][0],hs_i[0][1]),
                    (hs_i[0][0]+hs_i[0][2],hs_i[0][1]+hs_i[0][3]),
                    cv.RGB(155, 55, 200),2)
                cv.ShowImage("Camera", grayscale)
            '''
            return True
            #cv.ShowImage("Camera", grayscale)

        cascade = cv.Load("haar_xml/haarcascade_upperbody.xml")
        ub2 = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (22,18))

        if ub2:
            print 'haarcascade_upperbody found'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_coord = self._last_coord.copy()
            self._last_coord['ub2'] = ub2

            '''
            for hs_i in hs:

                cv.Rectangle(grayscale,(hs_i[0][0],hs_i[0][1]),
                    (hs_i[0][0]+hs_i[0][2],hs_i[0][1]+hs_i[0][3]),
                    cv.RGB(155, 55, 200),2)
                cv.ShowImage("Camera", grayscale)
            '''
            return True
            #cv.ShowImage("Camera", grayscale)

        self._detection_time = time.time() - start_time
        return False

    def set_modify_time(self,time):
        self._modify_time = time

    def get_modify_time(self):
        return self._modify_time

    def get_detect_time(self):
        return self._detection_time

    def what_was_found(self):
        return self._what_was_detected

    def get_current_picture(self):
        return self._current_picture

    def detect_move(self):
        print self._last_coord,self._prev_coord
        return self._last_coord!=self._prev_coord