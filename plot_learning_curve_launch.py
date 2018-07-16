"""
This script can be launched anytime after training of the networks is complete, since it only requires the output.txt
file. Ie results/e70-00/output.txt must exist

For each network specified in experiment labels, this script makes a plot of the training and validation accuracy
"""

import matplotlib.pyplot as plt

EXP_LABELS = ['e70-00']


# TODO: Refactor for poster use instead of presentation use
if __name__ == "__main__":
	for exp_label in EXP_LABELS:
		with open("results/" + exp_label + "/output.txt") as f:
			x, train, valid = [], [], []
			for line in f.readlines()[1:]:
				line = line.split()
				x.append(int(line[0]))
				train.append(float(line[1]))
				valid.append(float(line[2]))
			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1)
			ax.set_xlabel("Minibatches of 50 Images")
			ax.set_ylabel("Accuracy")
			ax.set_title("Machine Learning Curve")
			ax.plot(x, train, label="training")
			ax.plot(x, valid, label="validation")
			ax.legend(loc='lower right')
			plt.tight_layout()
			fig.savefig('results/' + exp_label + '/accuracy_vs_batch.png', dpi=300,
					bbox_inches='tight')
