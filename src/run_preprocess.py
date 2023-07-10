from Preprocessor import Preprocessor
import sys
from config import *

csv = sys.argv[1]
p = Preprocessor(RAW_DATA_DIR, RAW_CSV_DIR, DATA_DIR)
p.write_clean_csv(csv)
p.create_image_directories(csv)
p.preprocess_images(csv)
