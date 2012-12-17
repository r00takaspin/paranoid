#-*- coding: UTF-8 -*-
import sys
import time
from camera import Camera
from detector import Detector
import logging
import cv

from OsHelpers import OsHelper

if __name__ == "__main__":


    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='detect.log',filemode='w',level=logging.DEBUG)

    camera = Camera()
    camera.turn_on()

    detector = Detector(camera);
    os_helper = OsHelper.OsHelper()

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

        #если человека нет перед камерой, лочим комьютер
        print detector.detect_move()
        if not detector.detect() or not detector.detect_move():
            logging.warn("nothing was found in %f",detector.get_detect_time())

            img_name = "img/before_block/"+str(time.time()).replace(".","")+".jpg";
            cv.SaveImage(img_name,detector.get_current_picture())

            if time.time()-detector.get_modify_time()>10:
                camera.turn_off()
                os_helper.lock()
        else:
            logging.debug(detector.what_was_found()+" in %f",detector.get_detect_time())
        time.sleep(1)