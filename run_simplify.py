import os

files = os.listdir('res')
for file in files:
	os.system('SGE_batch -r "{}" -c "python3 -u run_batch.py {}" -P 1'.format(file[:-4], "res/" + file))
	print("Launched {} successfully".format(file))
