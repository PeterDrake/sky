from utils import *
from config import *
import pandas as pd
import numpy as np
from preprocess import *
import PIL
from PIL import ImageDraw
import random


mask = np.asarray(imageio.imread('simplemask20170923235300.png', pilmode="RGB"))


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
			mask[i][j] = random.choice(choices)


imageio.imwrite('simplemask20170923235300_after_green.png', mask)