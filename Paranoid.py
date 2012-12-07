#-*- coding: UTF-8 -*-
import sys
import os
import cv
import time
import commands
import platform

#обертка для opencv, отвечает за распознавание человека, сидящего за монитором
class Detector():
    _storage = None
    _modify_time = False
    _capture = None


    #производим последовательный поиск любого из элементов: глаз, лица, плеч и головы
    def _find_cntr(self,grayscale):
        cascade = cv.Load('haarcascade_frontalface_alt.xml')
        faces = cv.HaarDetectObjects(grayscale, cascade, self._storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50,50))

        if faces:
            print 'face found'
            self.set_modify_time(time.time())
            for face in faces:
                cv.Rectangle(grayscale,(face[0][0],face[0][1]),
                    (face[0][0]+face[0][2],face[0][1]+face[0][3]),
                    cv.RGB(155, 55, 200),2)
                #cv.ShowImage("Camera", grayscale)
            return True

        else:
            cascade = cv.Load('hs.xml')
            hs = cv.HaarDetectObjects(grayscale, cascade, self._storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (20,22))

            if hs:
                print 'hs found'
                self.set_modify_time(time.time())
                for hs_i in hs:
                    cv.Rectangle(grayscale,(hs_i[0][0],hs_i[0][1]),
                        (hs_i[0][0]+hs_i[0][2],hs_i[0][1]+hs_i[0][3]),
                        cv.RGB(155, 55, 200),2)
                    #cv.ShowImage("Camera", grayscale)

                return True
        #cv.ShowImage("Camera", grayscale)
        return False


    def detect(self):
        image = cv.QueryFrame(self._capture)
        image_size = cv.GetSize(image)

        #создаем чб версию изображения
        grayscale = cv.CreateImage(image_size, 8, 1)
        #конвертируем изображение в серый
        cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

        # create storage
        if not self._storage:
            self._storage = cv.CreateMemStorage(0)

        #увеличиваем контрастность изображения
        cv.EqualizeHist(grayscale, grayscale)

        return self._find_cntr(grayscale)

    def set_modify_time(self,time):
        self._modify_time = time

    def get_modify_time(self):
        return self._modify_time

    #инициализируем камеру
    def init_cam(self):
        capture = cv.CaptureFromCAM(0)
        #выставляем размеры захватываемого изображения
        cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,640)
        cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,480)
        self._capture = capture
        return capture

    def disable_cam(self):
        self._capture = None

class OsHelperFactory():

    @staticmethod
    def get_os_helper():
        if platform.system()=='Darwin':
            return MacHelper()
        else:
            raise Exception("Sorry, your os not implemented yet")

class BaseOsHelper(object):
    #блокируем компьютер
    @staticmethod
    def lock(self):
        raise NotImplementedError()

    #проверяем, авторизован ли пользователь
    @staticmethod
    def is_logged(self):
        raise NotImplementedError()

class MacHelper(BaseOsHelper):
    def lock(self):
        os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')

    def is_logged(self):
        result = commands.getstatusoutput("stat -f%Su /dev/console | grep root")
        if result[1]=='root':
            return False
        return True

#проверяет, не пора ли залочить машину
def is_expired(modify_time):
    return time.time()-modify_time>10

#точка входа
if __name__ == "__main__":
    detector = Detector();
    os_helper = OsHelperFactory.get_os_helper()
    capture = detector.init_cam()
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
    #cv.NamedWindow("Camera",cv.CV_WINDOW_AUTOSIZE)
    while 1:
        #если ноут уже заблокирован - ничего не делаем
        if not os_helper.is_logged():
            capture = None
            detector.disable_cam()
            print "we logged off"
            continue
        #если ноут не заблокирован, но потока с камеры нет - создаем его
        elif not capture:
            capture = detector.init_cam()
        #если человека нет перед камерой, лочим ее
        if not detector.detect() and is_expired(detector.get_modify_time()):
            os_helper.lock()
            print 'lock'
        time.sleep(1)
