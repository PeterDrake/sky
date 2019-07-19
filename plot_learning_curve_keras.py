import json
import matplotlib.pyplot as plt
from config import *

data = []
with open('loss_log.json') as f:
	for line in f:
		data.append(json.loads(line))

acc = []
loss = []
val_acc = []
val_loss = []
for f in range(len(data)):
	if 'acc' in data[f].keys():
		acc.append(data[f]["acc"])
		loss.append(data[f]["loss"])
	if 'val_acc' in data[f].keys():
		val_acc.append(data[f]["val_acc"])
		val_loss.append(data[f]["val_loss"])

plt.plot(acc)
plt.plot([0, len(acc)], val_acc)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('batches')
plt.legend(['acc', 'val_acc'], loc='upper left')
plt.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/accuracy_vs_batch.png', bbox_inches='tight')