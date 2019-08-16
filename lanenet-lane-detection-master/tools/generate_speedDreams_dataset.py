#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-18 下午7:31
# @Author  : Luo Yao
# @Site    : https://github.com/MaybeShewill-CV/lanenet-lane-detection
# @File    : generate_tusimple_dataset.py
# @IDE: PyCharm Community Edition
"""
处理tusimple数据集脚本
"""
import argparse
import glob
import json
import os
import os.path as ops
import shutil

import cv2
import numpy as np
import random

training_data_amount = 0


def init_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', type=str, help='The origin path of unzipped tusimple dataset')
    parser.add_argument('--val_size', type=int, help='Size of the validation set', default=0.)

    return parser.parse_args()


def process_json_file(json_file_path, src_dir, ori_dst_dir, binary_dst_dir, instance_dst_dir):
    """

    :param json_file_path:
    :param src_dir: 原始clips文件路径
    :param ori_dst_dir: rgb训练样本
    :param binary_dst_dir: binary训练标签
    :param instance_dst_dir: instance训练标签
    :return:
    """
    global training_data_amount
    assert ops.exists(json_file_path), '{:s} not exist'.format(json_file_path)

    image_nums = len(os.listdir(ori_dst_dir))

    with open(json_file_path, 'r') as file:
        for line_index, line in enumerate(file):
            info_dict = json.loads(line)

            image_dir = ops.split(info_dict['raw_file'])[0]
            image_dir_split = image_dir.split('/')[1:]
            image_dir_split.append(ops.split(info_dict['raw_file'])[1])
            image_name = '_'.join(image_dir_split)
            image_path = ops.join(src_dir, info_dict['raw_file'])
            assert ops.exists(image_path), '{:s} not exist'.format(image_path)

            h_samples = info_dict['h_samples']
            lanes = info_dict['lanes']

            image_name_new = '{:s}.png'.format('{:d}'.format(line_index + image_nums).zfill(4))

            src_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            dst_binary_image = np.zeros([src_image.shape[0], src_image.shape[1]], np.uint8)
            dst_instance_image = np.zeros([src_image.shape[0], src_image.shape[1]], np.uint8)

            for lane_index, lane in enumerate(lanes):
                assert len(h_samples) == len(lane)
                lane_x = []
                lane_y = []
                for index in range(len(lane)):
                    if lane[index] == -2:
                        continue
                    else:
                        ptx = lane[index]
                        pty = h_samples[index]
                        lane_x.append(ptx)
                        lane_y.append(pty)
                if not lane_x:
                    continue
                lane_pts = np.vstack((lane_x, lane_y)).transpose()
                lane_pts = np.array([lane_pts], np.int64)

                cv2.polylines(dst_binary_image, lane_pts, isClosed=False,
                              color=255, thickness=5)
                cv2.polylines(dst_instance_image, lane_pts, isClosed=False,
                              color=lane_index * 50 + 20, thickness=5)

            dst_binary_image_path = ops.join(binary_dst_dir, image_name_new)
            dst_instance_image_path = ops.join(instance_dst_dir, image_name_new)
            dst_rgb_image_path = ops.join(ori_dst_dir, image_name_new)

            cv2.imwrite(dst_binary_image_path, dst_binary_image)
            cv2.imwrite(dst_instance_image_path, dst_instance_image)
            cv2.imwrite(dst_rgb_image_path, src_image)

            print('Process {:s} success'.format(image_name))
            training_data_amount = training_data_amount + 1


def gen_train_sample(src_dir, b_gt_image_dir, i_gt_image_dir, image_dir):
    """
    生成图像训练列表
    :param src_dir:
    :param b_gt_image_dir: 二值基准图
    :param i_gt_image_dir: 实例分割基准图
    :param image_dir: 原始图像
    :return:
    """
    print('Generating dataset.txt file...')

    with open('{:s}/training/dataset.txt'.format(src_dir), 'w') as file:

        for image_name in os.listdir(b_gt_image_dir):
            if not image_name.endswith('.png'):
                continue

            binary_gt_image_path = ops.join(b_gt_image_dir, image_name)
            instance_gt_image_path = ops.join(i_gt_image_dir, image_name)
            image_path = ops.join(image_dir, image_name)

            assert ops.exists(image_path), '{:s} not exist'.format(image_path)
            assert ops.exists(instance_gt_image_path), '{:s} not exist'.format(instance_gt_image_path)

            b_gt_image = cv2.imread(binary_gt_image_path, cv2.IMREAD_COLOR)
            i_gt_image = cv2.imread(instance_gt_image_path, cv2.IMREAD_COLOR)
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)

            if b_gt_image is None or image is None or i_gt_image is None:
                print('图像对: {:s}损坏'.format(image_name))
                continue
            else:
                info = '{:s} {:s} {:s}'.format(image_path, binary_gt_image_path, instance_gt_image_path)
                file.write(info + '\n')
    return


def process_tusimple_dataset(src_dir):
    """

    :param src_dir:
    :return:
    """
    traing_folder_path = ops.join(src_dir, 'training')
    testing_folder_path = ops.join(src_dir, 'testing')

    os.makedirs(traing_folder_path, exist_ok=True)
    os.makedirs(testing_folder_path, exist_ok=True)

    for json_label_path in glob.glob('{:s}/label*.json'.format(src_dir)):
        json_label_name = ops.split(json_label_path)[1]

        shutil.copyfile(json_label_path, ops.join(traing_folder_path, json_label_name))

    for json_label_path in glob.glob('{:s}/test*.json'.format(src_dir)):
        json_label_name = ops.split(json_label_path)[1]

        shutil.copyfile(json_label_path, ops.join(testing_folder_path, json_label_name))

    gt_image_dir = ops.join(traing_folder_path, 'gt_image')
    gt_binary_dir = ops.join(traing_folder_path, 'gt_binary_image')
    gt_instance_dir = ops.join(traing_folder_path, 'gt_instance_image')

    os.makedirs(gt_image_dir, exist_ok=True)
    os.makedirs(gt_binary_dir, exist_ok=True)
    os.makedirs(gt_instance_dir, exist_ok=True)

    for json_label_path in glob.glob('{:s}/*.json'.format(traing_folder_path)):
        process_json_file(json_label_path, src_dir, gt_image_dir, gt_binary_dir, gt_instance_dir)

    gen_train_sample(src_dir, gt_binary_dir, gt_instance_dir, gt_image_dir)

    return


def generate_validation_set(src_dir, val_size):

    print('Generating train.txt and val.txt files...')

    training_file = open('{:s}/training/train.txt'.format(src_dir), 'w')
    validation_file = open('{:s}/training/val.txt'.format(src_dir), 'w')

    print("Number of lines in the file: ", training_data_amount)
    if training_data_amount <= val_size:
        raise ValueError("Value to high. Set a value lower then", training_data_amount)

    random_number_list = random.sample(range(0, training_data_amount), val_size)
    print(random_number_list)

    with open('{:s}/training/dataset.txt'.format(src_dir), 'r') as dataset:

        for x ,line in enumerate(dataset.readlines()):
            if (x in random_number_list):
                validation_file.write(line)
            else:
                training_file.write(line)



def train_file_lines_counter(src_dir):
    with open('{:s}/training/train.txt'.format(src_dir), 'r') as file:
        for counter, l in enumerate(file):
            pass
            return counter + 1

def picklines(thefile, whatlines):
  return [x for i, x in enumerate(thefile) if i in whatlines]


if __name__ == '__main__':
    args = init_args()

    process_tusimple_dataset(args.src_dir)
    generate_validation_set(args.src_dir, args.val_size)
