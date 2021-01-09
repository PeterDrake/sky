from Preprocessor import Preprocessor
import sys
from config import *

csv = sys.argv[1]
p = Preprocessor(RAW_DATA_DIR, RAW_CSV_DIR, DATA_DIR)
p.write_clean_csv(csv)
p.create_image_directories(csv)
p.preprocess_images(csv)
p.allocate_timestamps(csv, [0.6, 0.2, 0.2],
                      ['typical_training_timestamps', 'typical_validation_timestamps', 'typical_testing_timestamps'])
p.allocate_timestamps(csv, [0.5, 0.5], ['dubious_validation_timestamps', 'dubious_testing_timestamps'])