import cv2 as cv
import glob
from os import listdir
import numpy as np


class LeafImageWithWatershed:
    def __init__ (self, path, name):
        self.image = cv.imread(path)
        self.image_name = name

    def GetImage (self):
        return self.image

    def GetErodeImage (self):
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(6,6))
        er_img = cv.erode(self.image, kernel)
        return er_img

    def HSVAreas (self):
        hsv_image = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        markers = np.zeros((hsv_image.shape[0], hsv_image.shape[1]), dtype = "int32")
        markers[100:140,100:140] = 255
        markers[245:255,0:10] = 1
        markers[0:10,0:10] = 1
        markers[0:10,245:255] = 1
        markers[245:255,245:255] = 1
        watershed_BGR_total_leaf_area = cv.watershed(self.GetErodeImage(), markers) ## С помощью watershed определяем границу листа в BGR
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
        '''image_directory = save_directory + self.image_name
        image_mask_on_leaf_directory = save_directory + "_MASK_on_LEAF_" + self.image_name
        cv.imwrite(image_directory, self.GetImage())
        cv.imwrite(image_mask_on_leaf_directory, self.HSVtoBGR()[0])'''

        image_directory = save_directory + self.image_name
        image_mask_on_leaf_directory = save_directory + "_MASK_on_LEAF_" + self.image_name
        img_mask_directory = save_directory + "_MASK_ALL_" + self.image_name
        cv.imwrite(image_directory, self.GetImage())
        cv.imwrite(image_mask_on_leaf_directory, self.HSVtoBGR()[0])
        cv.imwrite(img_mask_directory, self.HSVtoBGR()[2])


