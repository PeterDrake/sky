"""
This script can be launched anytime after training of the networks is complete, since it only requires the output.txt
file. Ie results/e70-00/output.txt must exist

For each network specified in experiment labels, this script makes a plot of the training and validation accuracy
"""

import matplotlib.pyplot as plt
from config import RESULTS_DIR, EXPERIMENT_LABEL


if __name__ == "__main__":
	with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + "/output.txt") as f:
		x, train, valid = [], [], []
		for line in f.readlines()[1:]:
			line = line.split()
			x.append(int(line[0]))
			train.append(float(line[1]))
			valid.append(float(line[2]))
		fig = plt.figure(figsize=(12, 9))
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xlabel("Minibatches of 50 Images", fontsize=26)
		ax.set_ylabel("Accuracy", fontsize=26)
		ax.set_title("Machine Learning Curve", fontsize=30)
		ax.tick_params(labelsize='x-large')
		ax.plot(x, train, label="training")
		ax.plot(x, valid, label="validation")
		ax.legend(loc='lower right', fontsize=20)
		plt.tight_layout()
		fig.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/accuracy_vs_batch.png', bbox_inches='tight')
