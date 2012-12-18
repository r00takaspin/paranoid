#-*- coding: UTF-8 -*-
import sys
import os
import time
import commands
import platform
from camera import Camera
from detector import Detector
import logging
import cv
class OsHelperFactory():

    @staticmethod
    def get_os_helper():
        if platform.system()=='Darwin':
            return MacHelper()
        else:
            raise Exception("Sorry, your os not implemented yet")

class BaseOsHelper(object):
    @staticmethod
    def lock(self):
        """
        блокируем компьютер
        """
        raise NotImplementedError()

    @staticmethod
    def is_logged(self):
        """
        проверяем, авторизован ли пользователь
        """
        raise NotImplementedError()

class MacHelper(BaseOsHelper):
    def lock(self):
        os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')

    def is_logged(self):
        result = commands.getstatusoutput("stat -f%Su /dev/console | grep root")
        if result[1]=='root':
            return False
        return True

if __name__ == "__main__":


    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='detect.log',filemode='w',level=logging.DEBUG)

    camera = Camera()
    camera.turn_on()

    detector = Detector(camera);
    os_helper = OsHelperFactory.get_os_helper()

    if not camera.is_turned():
        print "Error opening capture device"
        sys.exit(1)
        cv.NamedWindow("Camera",cv.CV_WINDOW_AUTOSIZE)
    while 1:
        #если ноут уже заблокирован - ничего не делаем
        if not os_helper.is_logged():
            continue

        #если ноут не заблокирован, но потока с камеры нет - создаем его
        if not camera.is_turned():
            capture = camera.turn_on()

        picture = camera.take_picture()
        found = detector.detect(picture)
        if not found or (found and not detector.detect_move()):
            if not found:
                logging.warn("nothing was found in %f",detector.get_detect_time())
            else:
                logging.warn("all objects are static")
            img_name = "img/before_block/"+str(time.time()).replace(".","")+".jpg";
            cv.SaveImage(img_name,detector.get_current_picture())

            if time.time()-detector.get_modify_time()>10:
                camera.turn_off()
                os_helper.lock()
        else:
            logging.debug(detector.what_was_found()+" in %f",detector.get_detect_time())
        time.sleep(1)