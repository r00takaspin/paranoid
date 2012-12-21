#-*- coding: UTF-8 -*-
import cv

class Camera(object):
    """
    класс отвечает за работу с камерой
    """
    _capture = None
    _storage = None
    _camera = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Camera, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance


    def turn_on(self):
        """
        включаем камеру
        """
        self._storage = cv.CreateMemStorage(0)
        capture = cv.CaptureFromCAM(0)
        #выставляем размеры захватываемого изображения
        cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,640)
        cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,480)
        self._capture = capture

    def take_picture(self):
        """
        получаем картинку с веб-камеры
        """
        image = cv.QueryFrame(self._capture)
        image_size = cv.GetSize(image)

        #создаем чб версию изображения
        grayscale = cv.CreateImage(image_size, 8, 1)
        #конвертируем изображение в серый
        cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

        #увеличиваем контрастность изображения
        cv.EqualizeHist(grayscale, grayscale)

        return grayscale

    def turn_off(self):
        self._capture = None

    def is_turned(self):
        return not self._capture is None

    def get_storage(self):
        return self._storage