import os
import shutil
from preprocess_old import create_dirs

def simplify_all_names():
    """Simplifies all of the filenames in skyimage/ and cldmask/."""
    for dir in ('skyimage/', 'cldmask/'):
        for f in os.listdir(dir):
            if not f.endswith('.tar'):
                os.rename(dir + f, dir + simplify_name(f))


if __name__=='__main__':
	before = os.getcwd()
	os.chdir('data')
	create_dirs()
	os.chdir(before)
	os.chdir('testdata')
	files = os.listdir()
	for file in files:
		time = file[39:-4]
		newname = "simplemask" + time + ".png"
		shutil.copy(file, before + '/data/simplemask/' + newname)
		print(newname)
	os.chdir(before)