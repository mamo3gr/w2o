import os
import shutil
from typing import List

import cv2
import numpy as np


def copy_files(files: List[str], src_dir: str, dst_dir: str):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for file in files:
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)
        shutil.copy2(src_path, dst_path)


def main():
    root_dir = '/home/mamo/datasets/w2o'
    raw_dir = os.path.join(root_dir, 'raw')
    train_dir = os.path.join(root_dir, 'train')
    test_dir = os.path.join(root_dir, 'val')
    train_ratio = 0.8  # [0.0, 1.0]

    for class_name in os.listdir(raw_dir):
        if os.path.isfile(os.path.join(raw_dir, class_name)):
            continue

        class_dir = os.path.join(raw_dir, class_name)
        valid_files = []
        for file in os.listdir(class_dir):
            file_fullpath = os.path.join(class_dir, file)
            im = cv2.imread(file_fullpath)
            if im is not None:
                valid_files.append(file)

        n_files = len(valid_files)
        n_train_files = np.round(n_files * train_ratio).astype(int)
        print(n_train_files)
        np.random.shuffle(valid_files)
        train_files = valid_files[:n_train_files]
        test_files = valid_files[n_train_files:]
        print(f'split train:test = {len(train_files)}:{len(test_files)}')
        assert len(set(train_files) & set(test_files)) == 0
        copy_files(train_files, class_dir, os.path.join(train_dir, class_name))
        copy_files(test_files, class_dir, os.path.join(test_dir, class_name))


if __name__ == '__main__':
    main()
