#-*- coding: UTF-8 -*-
import sys
import time
from camera import Camera
from detector.detector import Detector
import logging
import cv
import os
import argparse

from OsHelpers import OsHelper

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='Paranoid')
    parser.add_argument('-debug', action='store', dest='debug', help='Stores all screenshots')
    parser.add_argument('-clear', action='store', dest='clear', help='Simple value')

    args = vars(parser.parse_args())

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='detect.log',filemode='w',level=logging.DEBUG)

    camera = Camera()
    camera.turn_on()

    detector = Detector(camera);
    os_helper = OsHelper.OsHelper()

    if args['clear']:
        os_helper.clear_img_folders()

    if not camera.is_turned():
        print "Error opening capture device"
        sys.exit(1)
        #cv.NamedWindow("Camera",cv.CV_WINDOW_AUTOSIZE)

    #флаг, чтоб не происходило блокировки сразу после включения камеры
    bFirstTime = True

    while 1:
        #если ноут уже заблокирован - ничего не делаем
        if not os_helper.is_logged():
            continue

        image_file_name = str(time.time()).replace(".","")+".jpg";

        #если ноут не заблокирован, но потока с камеры нет - создаем его
        if not camera.is_turned():
            bFirstTime = True
            capture = camera.turn_on()

        picture = camera.take_picture()

        found = detector.detect(picture)

        if bFirstTime:
            bFirstTime = False
            continue

        if not found or (found and not detector.detect_move()):
            if not found:
                bad_file_name = "img/before_block/"+image_file_name;
                cv.SaveImage(bad_file_name,detector.get_current_picture())
                logging.warn("nothing was found in %f",detector.get_detect_time())
            else:
                logging.warn("all objects are static")
            img_name = "img/before_block/"+str(time.time()).replace(".","")+".jpg";

            if time.time()-detector.get_modify_time()>10:
                camera.turn_off()
                os_helper.lock()
        else:
            logging.debug(detector.what_was_found()+" in %f",detector.get_detect_time())
            if args['debug']:
                good_file_name = "img/no_block/"+image_file_name
                cv.SaveImage(good_file_name,picture)
        time.sleep(1)