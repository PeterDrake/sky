from TimestampAllocator import TimestampAllocator
import sys
from config import *

csv = sys.argv[1]
typical = sys.argv[2]  # True or False
a = TimestampAllocator(DATA_DIR, TYPICAL_PROPORTIONS, DUBIOUS_PROPORTIONS)
a.allocate_timestamps(csv, bool(typical))
