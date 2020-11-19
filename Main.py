import glob
from os import listdir
from LeafImage import LeafImage
from LeafImageWithWatershed import LeafImageWithWatershed
from LeafKmeans import LeafKmeans
import imageio
from os import listdir


class Main:
    def __init__(self, path, file_name, file_name1):
        self.path = path
        self.text_file_name = file_name
        self.text_file_name1 = file_name1
        self.run()

    def run(self):
        self.out = open(text_file_name, "w")
        self.out1 = open(text_file_name1, "w")
        for directory in self.path:
            self.out.write(directory)
            self.out.write("\n")
            self.out.write("Number\tTotal Leaf Area\tPercent Leaf Damage\tImage name\n")
            self.out1.write(directory)
            self.out1.write("\n")
            self.out1.write("Number\tTotal Leaf Area\tPercent Leaf Damage\tImage name\n")
            i = 0
            for filename in listdir(directory):
                if (i == 25 or i == 75):
                    path = directory + "\\" + filename
                    image1 =LeafKmeans(path, filename)
                    total_leaf_area_pixels1, percent_leaf_damage1 = image1.CalculateDamage()
                    self.out1.write(
                        "{0:^5}\t{area:^15}\t{percent:^19f}\t{name}\n".format(i, area=total_leaf_area_pixels1,
                                                                              percent=percent_leaf_damage1,
                                                                              name=filename))


                    image1.Save(".\\results1\\")
                    # image = LeafImage(path, filename)
                    # total_leaf_area_pixels, percent_leaf_damage = image.CalculateDamage()
                    # self.out.write("{0:^5}\t{area:^15}\t{percent:^19f}\t{name}\n".format(i, area=total_leaf_area_pixels,
                    #                                                           percent=percent_leaf_damage,
                    #                                                            name=filename))
                    # image.Save(".\\results\\")
                i += 1

        self.out.close()
        self.out1.close()


path = glob.glob(".\\files\**")
text_file_name = ".\\results\\" + "Data_Leafs.txt"
text_file_name1 = ".\\results1\\" + "Data_Leafs.txt"
if __name__ == '__main__':
    app = Main(path, text_file_name, text_file_name1)
    app.run()
