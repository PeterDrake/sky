#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preprocess Total Sky Imager data from arm.gov. To use this:

1) Get the skyimage and cldmask data as described in Jessica's email.
2) Put the .tar files in a new directory called 'data' (which should live in
the same directory as this file -- git will ignore it).
3) Run this file.

This will create (within data):
    
- A folder skyimage containing the raw sky images (which will have shorter
names than the original files)
- A folder cldmask containing the raw TSI cloud masks (again, renamed)
- A folder simpleimage containing cropped 480x480 images
- A folder simplemask containing cloud masks that have been cropped and had
the sun removed from the shadowband
- Files train.stamps, valid.stamps, and test.stamps. These contain the
timestamp numbers for training, validation, and testing subsets of the data.
These files are not human-readable; they are pickled Python lists.
- Files always_black_mask.png and always_green_mask.png. These indicate
pixels that always have a particular color in the mask, so the network needn't
be asked to classify them.

After all of this has succeeded, you may wish to delete the huge .tar files
to save memory. Because obtaining them is nontrivial, this script does not
automatically delete them.

NOTE: For simplicity, the functions in this file assume that you are running
them from the data directory. Running this file temporarily switches to that
directory.

See the code at the end for a high-level description of the steps this
program goes through.

Created on Fri May 26 10:45:02 2017

@author: drake
"""

import os
import tarfile
from scipy import misc
import numpy as np
from PIL import Image
import random
import pickle
import time

# These constants are colors that appear in cloud masks
WHITE = np.array([255, 255, 255])
BLUE = np.array([0, 0, 255])
GRAY = np.array([192, 192, 192])
BLACK = np.array([0, 0, 0])
GREEN = np.array([0, 255, 0])
YELLOW = np.array([255, 255, 0])
COLORS = (WHITE, BLUE, GRAY, BLACK, GREEN)

def count_colors(img):
    """Returns an array of the number of WHITE, BLUE, GRAY, BLACK, and
    GREEN pixels in img."""
    counts = [(img == color).all(axis=2).sum() for color in COLORS]
    return np.array(counts)

def create_constant_mask(color, filename):
    """Creates a mask where any pixels not of color are BLUE. Saves it in
    filename."""
    b_mask = np.full((480,480,3), color)
    for file in os.listdir('simplemask/'):
        img = misc.imread('simplemask/' + file)
        b_mask[(img != color).any(axis=2)] = BLUE
    Image.fromarray(b_mask.astype('uint8')).save(filename)

def create_dirs():
    """Creates the necessary directories (if they don't already exist)."""
    for d in ('skyimage', 'cldmask', 'simpleimage', 'simplemask'):
        if not os.path.isdir(d):
            os.mkdir(d)

def crop_image(img):
    """Returns a version of img cropped down to 480 x 480."""
    return np.delete(img,
                     np.concatenate((np.arange(80), np.arange(80)+560)),
                     axis=0)

def delete_images_without_matching_masks():
    """Deletes image files that do not have matching mask files."""
    for f in os.listdir('skyimage/'):
        g = 'cldmask/cldmask' + extract_timestamp(f) + '.png'
        if not os.path.isfile(g):
            print('removing ' + f + ', which has no target mask')
            os.remove('skyimage/' + f)
        elif os.path.getsize(g) == 0:
            print('removing ' + f + ', which has a target mask of size 0')
            os.remove('skyimage/' + f)
            os.remove(g)           

def depth_first_search(r, c, img, visited, ever_visited, stack):
    """Returns True if there is a connected region including img[r][c] that is all
    WHITE and surrounded by BLACK. Modifies visited to include all of the white pixels.
    Modified ever_visited to include all pixels explored."""
    while stack:
        r, c = stack.pop()
        if ((img[r][c] == BLACK).all()):
            continue
        if (visited[r][c]):
            continue
        visited[r][c] = True
        if (ever_visited[r][c]):
            return False
        ever_visited[r][c] = True
        if (img[r][c] == GREEN).all() or (img[r][c] == BLUE).all() or (img[r][c] == GRAY).all():
            return False
        stack.extend(((r+1, c), (r-1, c), (r, c+1), (r, c-1)))
    return True

def extract_timestamp(filename):
    """Returns the timestamp within filename. Assumes filename ends in
    something like 20160415235930.jpg or 20160415235930.png."""
    return filename[-18:-4]

def remove_white_sun(img):
    """Removes the sun disk from img if it is white. (A yellow sun is easier
    to remove; that is handled directly in simpllify_masks.)"""
    start = time.clock()
    ever_visited = np.full(img.shape[:2], False, dtype=bool)
    visited = np.full(img.shape[:2], False, dtype=bool)
    for r in range(0, img.shape[0], 10):
        for c in range(0, img.shape[1], 10):
            if ((img[r][c] == WHITE).all()):
                stack = []
                stack.append((r, c))
                visited.fill(False)
                if depth_first_search(r, c, img, visited, ever_visited, stack):
                    img[visited] = BLACK
                    print('Removed the sun in ' + str(time.clock()-start) + ' seconds')
                    return img
    print('No sun found!')
    return img

def separate_data():
    """Saves pickled lists of timestamps to test.stamps, valid.stamps, and
    train.stamps."""
    stamps = [int(extract_timestamp(f)) for f in os.listdir('simpleimage/')]
    test, valid, train = separate_stamps(stamps)
    with open('test.stamps', 'wb') as f:
        pickle.dump(test, f)
    with open('valid.stamps', 'wb') as f:
        pickle.dump(valid, f)
    with open('train.stamps', 'wb') as f:
        pickle.dump(train, f)
    return test, valid, train

def separate_stamps(stamps):
    """Shuffles stamps and returns three lists: 20% of the stamps for
    testing, 16% for validation, and the rest for training."""
    random.shuffle(stamps)
    test = stamps[0:int(len(stamps)*0.2)]
    valid = stamps[int(len(stamps)*0.2):int(len(stamps)*0.36)]
    train = stamps[int(len(stamps)*0.36):]
    return test, valid, train

def simplify_all_names():
    """Simplifies all of the filenames in skyimage/ and cldmask/."""
    for dir in ('skyimage/', 'cldmask/'):
        for f in os.listdir(dir):
            if not f.endswith('.tar'):
                os.rename(dir + f, dir + simplify_name(f))

def simplify_all_images():
    """Crops the images in skyimage/ down to 480x480, writes those to
    simpleimage/, and returns the number of images cropped."""
    counts = 0
    for file in os.listdir('skyimage/'):
        if file.endswith('.jpg'):
            img = misc.imread('skyimage/' + file)
            cropped = crop_image(img)
            counts = counts + 1
            Image.fromarray(cropped).save('simpleimage/simpleimage' +
                           extract_timestamp(file) + '.jpg')
    return counts

def simplify_all_masks():
    """Writes similified versions of all images in cldmask to simplemask.
    Returns an array of relative frequencies of WHITE, BLUE, GRAY, BLACK, and
    GREEN."""
    counts = np.zeros(5, dtype=np.int)
    for file in os.listdir('cldmask/'):
        if file.endswith('.png'):
            img = misc.imread('cldmask/' + file)
            img = crop_image(img)
            print('About to remove sun from ' + file)
            if (img == YELLOW).all(axis=2).any():
                print('Removing yellow sun')
                img[(img == YELLOW).all(axis=2)] = BLACK
            else:
                print('Removing white sun')
                img = remove_white_sun(img)
            counts = counts + count_colors(img)
            Image.fromarray(img).save('simplemask/simplemask' + extract_timestamp(file) + '.png')
    return (counts / counts.sum())

def simplify_name(filename):
    """Accepts an arm.gov filename and returns a shorter, simpler version."""
    return filename[6:filename.index('C1')] + filename[-18:]

def test_remove_white_sun():
    """For manually (visually) verifying that remove_white_sun works."""
    img = misc.imread('data/cldmask/cldmask20160414174600.png')
    img = remove_white_sun(img)
    img = Image.fromarray(img.astype('uint8'))
    img.show()
    return img

def unpack_all_tars():
    """Unpacks all available .tar files into the appropriate directories."""
    for f in os.listdir('./'):
        if f.endswith('.tar'):
            if 'skyimage' in f:
                unpack_tar(f, 'skyimage/')
            elif 'cldmask' in f:
                unpack_tar(f, 'cldmask/')

def unpack_tar(file, dir):
    """Given a .tar file, moves it to dir and unpacks it."""
    g = dir + file
    os.rename(file, g)
    tar = tarfile.open(g)
    tar.extractall(path=dir)
    tar.close()


if __name__ == '__main__':
    before = os.getcwd()
    os.chdir('data')
    print('Creating directories')
    create_dirs()
    print('Unpacking tars')
    unpack_all_tars()
    print('Simplifying names')
    simplify_all_names()
    print('Deleting images without masks')
    delete_images_without_matching_masks()
    print('Simplifying images')
    print(str(simplify_all_images()) + ' images processed')
    print('Simplifying masks')
    print('[White, Blue, Gray, Black, Green] = ' + str(simplify_all_masks()))
    print('Separating data')
    test, valid, train = separate_data()
    print(str(len(test)) + ' test cases; ' +
          str(len(valid)) + ' validation cases; ' +
          str(len(train)) + ' training cases.')
    print('Creating always-black mask.')
    create_constant_mask(BLACK, 'always_black_mask.png')
    print('Creating always-green mask.')
    create_constant_mask(GREEN, 'always_green_mask.png')
    os.chdir(before)
    print('Done')
