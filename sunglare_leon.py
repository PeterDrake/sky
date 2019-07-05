from replace_green_lines import new_remove_green
from center_preprocess import *


def test():
    m = np.asarray(imageio.imread('typical_data/sgptsicldmaskC1.a1.20120501.170000.png.20120501170000.png', pilmode="RGB"))
    img = np.asarray(imageio.imread('typical_data/sgptsiskyimageC1.a1.20120501.170000.jpg.20120501170000.jpg', pilmode="RGB"))
    m, img = center_and_add_border(m, img)
    imageio.imwrite('typical_data/mask_20120501170000_sunglare_v1.png', new_remove_green(m))
    imageio.imwrite('typical_data/img_20120501170000_sunglare_v1.jpg', img)


if __name__ == '__main__':
    test()
