"""
Silly little file to print out updated progress for each training task running.
You specify the directories, and it prints out their progress from output.txt.
Just prints the last line from each directory.
"""

import time

if __name__ == "__main__":
	base_folder = "results/e70-"
	sub_folders = ['00', '01', '02', '03', '04']
	files = []
	for ext in sub_folders:
		files.append(base_folder + ext + "/output.txt")

	while True:
		for file in files:
			with open(file, 'r') as f:
				print(file)
				print(f.readlines()[-1].strip('\n'))
		print()
		time.sleep(10)
