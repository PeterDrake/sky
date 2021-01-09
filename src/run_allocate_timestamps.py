from TimestampAllocator import TimestampAllocator
import sys
from config import *

csv = sys.argv[1]
typical = sys.argv[2]  # True or False
a = TimestampAllocator(DATA_DIR, [0.6, 0.2, 0.2], [0.5, 0.5])
a.allocate_timestamps(csv, bool(typical))
