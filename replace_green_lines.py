from utils import *
from config import *
import pandas as pd
import numpy as np
from preprocess import *
import PIL
from PIL import ImageDraw
import random
import numpy_indexed as npi


mask = np.asarray(imageio.imread('typical_data/green_mask_test.png', pilmode="RGB"))


for i in range(480):
	for j in range(480):
		choices = []
		r = 1
		if np.array_equal(mask[i][j], GREEN):
			for r in range(1, 5):
				if not np.array_equal(mask[i][j - r], GREEN) and not np.array_equal(mask[i][j - r], BLACK):
					choices.append(mask[i][j - r])
				if not np.array_equal(mask[i][j + r], GREEN) and not np.array_equal(mask[i][j + r], BLACK):
					choices.append(mask[i][j + r])
				if not np.array_equal(mask[i - r][j], GREEN) and not np.array_equal(mask[i - r][j], BLACK):
					choices.append(mask[i - r][j])
				if not np.array_equal(mask[i + r][j], GREEN) and not np.array_equal(mask[i + r][j], BLACK):
					choices.append(mask[i + r][j])
				if len(choices) != 0:
					break
			np.array(choices)
			row = npi.mode(choices)
			mask[i][j] = row



imageio.imwrite('i_like_waffels.png', mask)