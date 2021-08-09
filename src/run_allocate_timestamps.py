from TimestampAllocator import TimestampAllocator
import sys
from config import *

csv = sys.argv[1]
typical_or_dubious = sys.argv[2]
a = TimestampAllocator(DATA_DIR, TYPICAL_PROPORTIONS, DUBIOUS_PROPORTIONS)
a.allocate_timestamps(csv, typical_or_dubious)
