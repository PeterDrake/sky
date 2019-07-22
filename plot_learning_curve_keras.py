import json
import matplotlib.pyplot as plt
from config import *

data = []
with open(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/log_acc_and_loss.json') as f:
	for line in f:
		data.append(json.loads(line))

acc = []
loss = []
val_acc = []
val_loss = []
epoch = []
display = 10
for f in range(len(data)):
	if f % display == 0:
		if 'acc' in data[f].keys():
			acc.append(data[f]["acc"])
			loss.append(data[f]["loss"])
	if 'val_acc' in data[f].keys():
		val_acc.append(data[f]["val_conv2d_2_acc"])
		val_loss.append(data[f]["val_conv2d_2_loss"])
		max_epoch = data[f]["epoch"] + 1

for i in range(int(max_epoch)):
	epoch.append(len(acc)/max_epoch * (i + 1))

plt.plot(acc)
plt.plot(epoch, val_acc)
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('Display every ' + str(display) + ' batches')
plt.legend(['acc', 'val_acc'], loc='lower right')
plt.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/accuracy_vs_batch.png', bbox_inches='tight')

plt.plot(loss)
plt.plot(epoch, val_loss)
plt.title('model accuracy')
plt.ylabel('loss')
plt.xlabel('Display every ' + str(display) + ' batches')
plt.legend(['loss', 'val_loss'], loc='upper right')
plt.savefig(RESULTS_DIR + '/' + EXPERIMENT_LABEL + '/loss_vs_batch.png', bbox_inches='tight')