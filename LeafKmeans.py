import os
import imageio
import cv2 as cv
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import copy


class LeafKmeans:
    def __init__ (self, path, name):
        self.image = cv.imread(path)
        self.image_name = name

    def GetImage (self):
        return self.image



    def HSVAreas (self):
        Z = np.float32(self.image.reshape((-1, 3)))
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 64
        ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()].reshape((self.image.shape))


        hsv_image = cv.cvtColor(result, cv.COLOR_BGR2HSV)
        markers = np.zeros((hsv_image.shape[0], hsv_image.shape[1]), dtype="int32")
        markers[90:140, 90:140] = 255
        markers[236:255, 0:20] = 1
        markers[0:20, 0:20] = 1
        markers[0:20, 236:255] = 1
        markers[236:255, 236:255] = 1

        watershed_BGR_total_leaf_area = cv.watershed(result, markers) ## С помощью watershed определяем границу листа в BGR
        watershed_HSV_total_leaf_area = cv.watershed(hsv_image, markers)
        hsv_nondamage_area = cv.inRange(hsv_image, (35,25,25),(87, 255,255))
        hsv_damage_area = watershed_HSV_total_leaf_area - hsv_nondamage_area
        return hsv_damage_area, watershed_HSV_total_leaf_area

    def HSVtoBGR (self):
        hsv_damage_area, watershed_HSV_total_leaf_area = self.HSVAreas()
        total_leaf_area = np.zeros_like(self.image, np.uint8)
        damage_area = np.zeros_like(self.image, np.uint8)
        total_leaf_area[watershed_HSV_total_leaf_area > 1] = self.image[watershed_HSV_total_leaf_area > 1]
        damage_area[hsv_damage_area > 1] = (19, 69, 139)
        total_leaf_area[hsv_damage_area > 1] = (19, 69, 139)
        total_leaf_area_mask = np.zeros_like(self.image, np.uint8)
        total_leaf_area_mask[watershed_HSV_total_leaf_area > 1] = (0, 255, 0)
        total_leaf_area_mask[hsv_damage_area > 1] = (19, 69, 139)
        return total_leaf_area, damage_area,  total_leaf_area_mask

    def CalculateDamage (self):
        total_leaf_area, damage_area, a = self.HSVtoBGR()
        GRAY_total_leaf_area = cv.cvtColor(total_leaf_area, cv.COLOR_BGR2GRAY)
        GRAY_damage_area = cv.cvtColor(damage_area, cv.COLOR_BGR2GRAY)
        total_area = cv.countNonZero(GRAY_total_leaf_area)
        damage = cv.countNonZero(GRAY_damage_area)
        percent_damage = damage * 100. / total_area
        return total_area, percent_damage

    def Save (self, save_directory):
        name = self.image_name.split('.')[0] + ".gif"
        imageio.mimsave(name, [self.image, self.HSVtoBGR()[0]], duration=0.8)

        image_directory = save_directory + self.image_name
        image_mask_on_leaf_directory = save_directory + "_MASK_on_LEAF_" + self.image_name
        #img_mask_directory = save_directory + "_MASK_ALL_" + self.image_name
        cv.imwrite(image_directory, self.GetImage())
        cv.imwrite(image_mask_on_leaf_directory, self.HSVtoBGR()[0])
        #cv.imwrite(img_mask_directory, self.HSVtoBGR()[2])


