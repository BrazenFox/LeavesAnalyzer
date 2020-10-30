import glob
from os import listdir
from LeafImage import LeafImage


class Main:
    def __init__ (self, path, file_name):
        self.path = path
        self.text_file_name = file_name
        self.run()

    def run(self):
        for directory in self.path:
            self.out = open(text_file_name, "w")
            self.out.write(directory)
            self.out.write("\n")
            self.out.write("Number\tTotal Leaf Area\tPercent Leaf Damage\tImage name\n")
            i = 0
            for filename in listdir(directory):

                path = directory + "\\" + filename

                image = LeafImage(path, filename)

                total_leaf_area_pixels, percent_leaf_damage = image.CalculateDamage()
                self.out.write("{0:^5}\t{area:^15}\t{percent:^19f}\t{name}\n".format(i, area = total_leaf_area_pixels, percent = percent_leaf_damage, name = filename))

                if (i == 111):
                    image.Save(".\\results\\")
                i += 1

        self.out.close()


path = glob.glob(".\\files\**")
text_file_name = ".\\results\\" + "Data_Leafs.txt"
if __name__ == '__main__':
    app = Main(path, text_file_name)
    app.run()

