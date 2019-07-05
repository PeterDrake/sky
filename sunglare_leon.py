from replace_green_lines import new_remove_green
from center_preprocess import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob


def format_img(mask_path, img_path):
	m = np.asarray(imageio.imread(mask_path, pilmode="RGB"))
	img = np.asarray(imageio.imread(img_path, pilmode="RGB"))
	m, img = center_and_add_border(m, img)
	imageio.imwrite('typical_data/sunglare/formatted_mask.{}.png'.format(extract_timestamp(mask_path)),
					new_remove_green(m))
	imageio.imwrite('typical_data/sunglare/formatted_img.{}.jpg'.format(extract_timestamp(img_path)), img)


def sun_glare(path):
	img = cv2.imread(path, 0)
	edges = cv2.Canny(img, 0, 950, 2000, 3, True)

	laplacian = cv2.Laplacian(img, cv2.CV_64F)
	sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
	sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

	plt.subplot(121), plt.imshow(img, cmap='gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122), plt.imshow(edges, cmap='gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

	plt.savefig('typical_data/sunglare/canny_edge.{}.png'.format(extract_timestamp(path)))

	plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2, 2, 2), plt.imshow(laplacian, cmap='gray')
	plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
	plt.subplot(2, 2, 3), plt.imshow(sobelx, cmap='gray')
	plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
	plt.subplot(2, 2, 4), plt.imshow(sobely, cmap='gray')
	plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

	plt.savefig('typical_data/sunglare/gradient.{}.png'.format(extract_timestamp(path)))



if __name__ == '__main__':
	# files = glob.glob("typical_data/sunglare/sgptsi*")
	# files.sort(key=lambda x: x[-18:])
	#
	# for f in range(0, len(files), 2):
	# 	format_img(str(files[f + 1]), str(files[f]))

	files = glob.glob("typical_data/sunglare/formatted_mask*")

	for f in files:
		sun_glare(f)
