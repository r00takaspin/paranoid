#-*- coding: UTF-8 -*-
from camera import Camera
import cv
import time

class HaarDetector(object):
    """
    класс производит поиск по изображению используя HAAR файл
    """
    __filename = None
    picture = None
    camera_storage = None
    minimal_size = None
    start_time = None
    end_time = None
    found_objects = None

    def __init__(self,filename,camera_storage,minimal_size):
        self.__filename = filename
        self.camera_storage = camera_storage
        self.minimal_size = minimal_size

    def detect(self,picture):
        cascade = cv.Load(self.__filename)
        objects = cv.HaarDetectObjects(picture, cascade,self.camera_storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, self.minimal_size)
        if objects:
            self.found_objects = objects
            return True

    def get_found_objects(self):
        return self.found_objects

class HaarManager(object):
    """фабрика отдающая детектор нужной части тела"""
    _instance = None
    __detector_collection = {}

    def add_detector(self,name,instance):
        self.__detector_collection[name] = instance

    def get_detector(self,name):
        return self._instance.__detector_collection[name]

    def get_all_detectors(self):
        return self._instance.__detector_collection

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HaarManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.add_detector('face',HaarDetector('haar_xml/haarcascade_frontalface_alt.xml',Camera().get_storage(),(100,100)))
            cls._instance.add_detector('profile',HaarDetector('haar_xml/haarcascade_profileface.xml',Camera().get_storage(),(20,20)))
            cls._instance.add_detector('hs',HaarDetector('haar_xml/hs.xml',Camera().get_storage(),(40,40)))
            cls._instance.add_detector('upperbody',HaarDetector('haar_xml/haarcascade_upperbody.xml',Camera().get_storage(),(22,18)))
        return cls._instance

class Detector(object):
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

    def detect(self,picture):
        """производим последовательный поиск любого из элементов: глаз, лица, плеч и головы"""
        start_time = time.time()
        self._detection_time = False
        self._what_was_detected = None
        self._current_picture = picture

        #TODO: сделать обход в следующем порядке: face->profile->hs->upperbody т.к. тормозит сильно
        for handler_name,detector in HaarManager().get_all_detectors().iteritems():
            if detector.detect(self._current_picture):
                self._what_was_detected = handler_name
                self.set_modify_time(time.time())
                self._detection_time = time.time() - start_time
                self._prev_found_objs = list(self._curr_found_objs)
                self._curr_found_objs = detector.get_found_objects()
                return True

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