import cv2 as cv
import numpy as np


class LeafImage:
    def __init__(self, path, name):
        self.image = cv.imread(path)
        self.image_name = name

    def GetImage(self):
        return self.image

    def HSVAreas(self):
        hsv_image = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        hsv_total_leaf_area = cv.inRange(hsv_image, (19, 38, 0), (101, 255, 255))
        hsv_nondamage_area = cv.inRange(hsv_image, (35, 25, 25), (87, 255, 255))
        hsv_damage_area = hsv_total_leaf_area - hsv_nondamage_area
        hsv_non_damage_area = hsv_total_leaf_area - hsv_damage_area
        return hsv_damage_area, hsv_non_damage_area

    def HSVtoBGR(self):
        hsv_damage_area, hsv_non_damage_area = self.HSVAreas()
        non_damage_area = np.zeros_like(self.image, np.uint8)
        non_damage_area[hsv_non_damage_area > 0] = self.image[hsv_non_damage_area > 0]
        damage_area = np.zeros_like(self.image, np.uint8)
        damage_area[hsv_damage_area > 0] = self.image[hsv_damage_area > 0]
        return non_damage_area, damage_area

    def CalculateDamage(self):
        hsv_damage_area, hsv_non_damage_area = self.HSVAreas()
        damage = cv.countNonZero(hsv_damage_area)
        non_damage = cv.countNonZero(hsv_non_damage_area)
        total_area = damage + non_damage
        percent_damage = damage * 100. / total_area
        return total_area, percent_damage

    def Mask(self):
        non_damage_area_1, damage_area = self.HSVtoBGR()
        non_damage_area_2 = np.zeros_like(self.image, np.uint8)
        for x in range(len(damage_area)):
            for y in range(len(damage_area[x])):
                if non_damage_area_1[x][y][0] != 0 | non_damage_area_1[x][y][1] != 0 | non_damage_area_1[x][y][2] != 0:
                    non_damage_area_2[x][y] = (0, 255, 0)
                if damage_area[x][y][0] != 0 | damage_area[x][y][1] != 0 | damage_area[x][y][2] != 0:
                    damage_area[x][y] = (19, 69, 139)
                    non_damage_area_1[x][y] = (0, 0, 0)
                    non_damage_area_2[x][y] = (0, 0, 0)
        return non_damage_area_1 + damage_area, non_damage_area_2 + damage_area

    def Save(self, save_directory):
        img_mask_on_leaf, img_mask = self.Mask()
        image_directory = save_directory + self.image_name
        image_mask_on_leaf_directory = save_directory + "_MASK_on_LEAF_" + self.image_name
        img_mask_directory = save_directory + "_MASK_ALL_" + self.image_name
        cv.imwrite(image_directory, self.GetImage())
        cv.imwrite(image_mask_on_leaf_directory, img_mask_on_leaf)
        cv.imwrite(img_mask_directory, img_mask)
