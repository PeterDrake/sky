import Preprocessor
import sys

csv = sys.argv[1]
p = Preprocessor('/home/users/jkleiss/TSI_C1', '../raw_csv', '../data')
p.write_clean_csv(csv)
p.create_image_directories(csv)
p.preprocess_images(csv)
