from __future__ import print_function
import argparse
import cv2
import lmdb
import numpy
import os
from os.path import exists, join

__author__ = 'Fisher Yu'
__email__ = 'fy@cs.princeton.edu'
__license__ = 'MIT'


def view(db_path):
    print('Viewing', db_path)
    print('Press ESC to exist or SPACE to advance.')
    window_name = 'LSUN'
    cv2.namedWindow(window_name)
    env = lmdb.open(db_path, map_size=1099511627776,
                    max_readers=100, readonly=True)
    with env.begin(write=False) as txn:
        cursor = txn.cursor()
        for key, val in cursor:
            print('Current key:', key)
            img = cv2.imdecode(
                numpy.fromstring(val, dtype=numpy.uint8), 1)
            cv2.imshow(window_name, img)
            c = cv2.waitKey()
            if c == 27:
                break


def export_images(db_path, out_dir, flat=False, limit=-1):
    print('Exporting', db_path, 'to', out_dir)
    env = lmdb.open(db_path, map_size=1099511627776,
                    max_readers=100, readonly=True)
    count = 0
    with env.begin(write=False) as txn:
        cursor = txn.cursor()
        for key, val in cursor:
            if not flat:
                image_out_dir = join(out_dir, '/'.join(key[:6].decode()))
            else:
                image_out_dir = out_dir
            if not exists(image_out_dir):
                os.makedirs(image_out_dir)
            image_out_path = join(image_out_dir, key.decode() + '.webp')
            with open(image_out_path, 'wb') as fp:
                fp.write(val)
            count += 1
            if count == limit:
                break
            if count % 1000 == 0:
                print('Finished', count, 'images')


def slice_lmdb(db_path, new_lmdb_dir, limit):
    """ Stores an array of images to LMDB.
        Parameters:
        ---------------
        images       images array, (N, 32, 32, 3) to be stored
        labels       labels array, (N, 1) to be stored
    """
    # num_images = len(images)

    # map_size = num_images * images[0].nbytes * 10
    # Open original lmdb database from which you are slicing
    env_orig = lmdb.open(db_path, map_size=1099511627776,
                    max_readers=100, readonly=True)
    count = 0
    with env_orig.begin(write=False) as txn_orig:
        length = txn_orig.stat()['entries']
        mapsize = round(limit/length * 1099511627776)
        # Create a new LMDB DB for all the images
        env_new = lmdb.open(join(new_lmdb_dir,"train_sliced_lmdb"), map_size= mapsize)
        with env_new.begin(write=True) as txn_new:
            cursor = txn_orig.cursor()
            for key, val in cursor:
                txn_new.put(key, val)
                count += 1
                if count == limit:
                    break
                if count % 1000 == 0:
                    print('Finished', count, 'images')
        env_new.close()
    env_orig.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', type=str,
                        choices=['view', 'export', 'slice'],
                        help='view: view the images in the lmdb database '
                             'interactively.\n'
                             'export: Export the images in the lmdb databases '
                             'to a folder. The images are grouped in subfolders'
                             'slice: Slice the original database to a smaller'
                             'size as defined by limit argument'
                             ' determinted by the prefiex of image key.')
    parser.add_argument('lmdb_path', nargs='+', type=str,
                        help='The path to the lmdb database folder. '
                             'Support multiple database paths.')
    parser.add_argument('--out_dir', type=str, default='')
    parser.add_argument('--limit', type=int, default=-1)
    parser.add_argument('--flat', action='store_true',
                        help='If enabled, the images are imported into output '
                             'directory directly instead of hierarchical '
                             'directories.')
    args = parser.parse_args()

    command = args.command
    lmdb_paths = args.lmdb_path

    for lmdb_path in lmdb_paths:
        if command == 'view':
            view(lmdb_path)
        elif command == 'export':
            export_images(lmdb_path, args.out_dir, args.flat, args.limit)
        elif command == 'slice':
            slice_lmdb(lmdb_path, args.out_dir, args.limit)



if __name__ == '__main__':
    main()
