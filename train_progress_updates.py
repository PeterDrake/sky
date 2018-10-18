"""
Silly little file to print out updated progress for each training task running.
You specify the directories, and it prints out their progress from output.txt.
Just prints the last line from each directory.
"""

import time

if __name__ == "__main__":
	exp_labels = ['e77-00']
	while True:
		for exp_label in exp_labels:
			with open('results/' + exp_label + '/output.txt', 'r') as f:
				print(exp_label)
				line = f.readlines()[-1].strip('\n').split()
				print("{}%".format(int(line[0]) / 20))
				print(line)
		print()
		time.sleep(30)
