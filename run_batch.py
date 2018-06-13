import sys
from preprocess import simplify_image, simplify_mask

if __name__ == "__main__":
	f = open(sys.argv[1])  # This is the name of the file containing timestamps
	print("Opened {}".format(sys.argv[1]))
	for i in range(len(f)):
		time = f[i]
		time = time.replace('\n', '')
		if i % 1000 == 0:
			print("Simplifying image & mask number {}".format(i))
		simplify_mask(time)
		simplify_image(time)
