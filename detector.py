#-*- coding: UTF-8 -*-
from camera import Camera
import cv
import time

class Detector():
    """обертка для opencv, отвечает за распознавание человека, сидящего за монитором"""

    MONTION_DELTA = 5

    _modify_time = False
    _camera = None
    _detection_time = False
    _what_was_detected = None
    _current_picture = None
    _curr_found_objs = {}
    _prev_found_objs = {}


    def __init__(self,camera):
        self._camera = camera

    #TODO:эта функция требует рядя рефакторингв
    def detect(self,picture):
        """производим последовательный поиск любого из элементов: глаз, лица, плеч и головы"""
        start_time = time.time()
        self._detection_time = False
        self._what_was_detected = None
        self._current_picture = picture

        cascade = cv.Load('haar_xml/haarcascade_frontalface_alt.xml')
        faces = cv.HaarDetectObjects(self._current_picture, cascade,self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50,50))

        if faces:
            self._what_was_detected = 'face'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_found_objs = list(self._curr_found_objs)
            self._curr_found_objs = faces
            return True


        cascade = cv.Load('haar_xml/haarcascade_profileface.xml')
        profiles = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))

        if profiles:
            self._what_was_detected = 'profile'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_found_objs = list(self._curr_found_objs)
            self._curr_found_objs = profiles
            return True

        cascade = cv.Load('haar_xml/hs.xml')
        hs = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,22))

        if hs:
            self._what_was_detected = 'hs'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_found_objs = list(self._curr_found_objs)
            self._curr_found_objs = hs
            print "hs",self._prev_found_objs," --- ",self._curr_found_objs
            return True
            #cv.ShowImage("Camera", grayscale)

        cascade = cv.Load('haar_xml/haarcascade_mcs_upperbody.xml')
        ub = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,22))

        if ub:
            self._what_was_detected = 'upper body'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._prev_found_objs = list(self._curr_found_objs)
            self._curr_found_objs = ub
            return True
            #cv.ShowImage("Camera", grayscale)

        cascade = cv.Load("haar_xml/haarcascade_upperbody.xml")
        ub2 = cv.HaarDetectObjects(self._current_picture, cascade, self._camera.get_storage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (22,18))

        if ub2:
            print 'haarcascade_upperbody found'
            self.set_modify_time(time.time())
            self._detection_time = time.time() - start_time
            self._what_was_detected = "haarcascade_upperbody"
            self._prev_found_objs = list(self._curr_found_objs)
            self._curr_found_objs = ub2
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

    def __between(self,a,b):
        return abs(a-b)<=self.MONTION_DELTA

    def __object_moved(self,state1,state2):
        if  (self.__between(state1[0],state2[0]) or
             self.__between(state1[1],state2[1]) or
             self.__between(state1[2],state2[2]) or
             self.__between(state1[3],state2[3])):
                return False
        return True

    def detect_move(self):
        """обнаруживаем, двигался ли объект"""
        for k in range(0,len(self._curr_found_objs)):
            try:
                old_object = self._curr_found_objs[k][0]
                new_object = self._prev_found_objs[k][0]
            except IndexError:
                return True
            if self.__object_moved(old_object,new_object):
                return True

        return False