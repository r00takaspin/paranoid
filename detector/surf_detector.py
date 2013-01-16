__author__ = 'webgeist_xor'
#-*- coding: UTF-8 -*-

import cv
import cv2
import sys
import numpy as np
import os

class SURFDetector:

    # порог гауссиана
    __hessianThreshold = 100

    def __init__(self, hs):
        self.__hessianThreshold = hs

    def getMatch(self, file1, file2 ):

        img1 = cv.LoadImage( file1 )
        img2 = cv.LoadImage( file2 )
        result = self.__compareImages(img1, img2)

        return result

    def __compareImages(self, gray_img1, gray_img2):

        # получаем характерные точки и их дескрипторы
        (aKeyPoints1, aDescriptors1) = cv.ExtractSURF(gray_img1, None,cv.CreateMemStorage(),(0, self.__hessianThreshold, 3, 4))
        (aKeyPoints2, aDescriptors2) = cv.ExtractSURF(gray_img2, None,cv.CreateMemStorage(),(0, self.__hessianThreshold, 3, 4))

        result = sys.float_info.max

        if aKeyPoints1 > 0 and aKeyPoints2 > 0:
            result = self.__matchDescriptors(aDescriptors1, aDescriptors2)
            '''
            my_keypoints = []
            for i in range(0,len(result)):
                my_keypoints.append(result[i][1])

            current_index=0
            for ((x, y), laplacian, size, dir, hessian) in aKeyPoints2:
                if (current_index in my_keypoints):
                    cv.Circle(gray_img2, (int(x),int(y)), int(size*1.2/9.*2), cv.Scalar(0,0,255), 1, 8, 0)
                current_index += 1

            cv.ShowImage("SURF_mvg2", gray_img2)
            cv.WaitKey(1000)
            '''
            return len(result)

    # подсчитаем
    def __matchDescriptors(self, aDesc1, aDesc2):

        result = 0

        return self.match_flann(aDesc1 ,aDesc2)


    def match_flann(self, desc1, desc2, r_threshold = 0.75):
        flann_params = dict(algorithm = 1, trees = 4)
        flann = cv2.flann_Index(np.asanyarray(desc2,dtype="float32"), flann_params)
        idx2, dist = flann.knnSearch(np.asanyarray(desc1,dtype="float32"), 2, params = {}) # bug: need to provide empty dict
        mask = dist[:,0] / dist[:,1] < r_threshold
        idx1 = np.arange(len(desc1))
        pairs = np.int32( zip(idx1, idx2[:,0]) )
        return pairs[mask]

#TODO: remove
if __name__ == "__main__":
    surf = SURFDetector(1000)
    dir = "/img/no_block/"
    for file in os.listdir("../"+dir):
        if file!='.gitignore' and file!='.DS_Store':
            print str(surf.getMatch("../tests/samples/good/my_face.png","../"+dir+file)) + dir+file
    #cv.WaitKey(100000)