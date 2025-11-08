from GlareRemover import GlareRemover
import sys
from config import *

csv = sys.argv[1]
g = GlareRemover(DATA_DIR, DATA_DIR)
g.create_image_directories(csv)
g.write_deglared_files(csv)
