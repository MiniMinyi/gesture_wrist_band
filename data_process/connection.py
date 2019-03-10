import argparse
import os
import json
from skimage import color
import cv2
import numpy as np
import skimage
from skimage.filters import sobel


def extract_lm_data(data):
    hands = data.get("hands", [])
    if len(hands) != 1:
        return []
    hand = hands[0]
    wrist = np.array(hand.get('wrist', []))
    fingers = data.get("pointables", [])
    if len(fingers) != 5:
        return []
    vectors = []
    fingers.sort(key=lambda x: x["type"])
    for finger in fingers:
        vectors.append(np.array(finger["mcpPosition"]) - wrist)
        vectors.append(np.array(finger["pipPosition"]) - wrist)
        vectors.append(np.array(finger["dipPosition"]) - wrist)
        vectors.append(np.array(finger["tipPosition"]) - wrist)
    vectors.append(np.array(hand["palmPosition"]) - wrist)
    return vectors


def find_nearest_image_file(images_names, leapmotion_data_name, index):
    best_offset = 10000000
    best_index = -1
    timestamp = int(leapmotion_data_name[:-4])
    while index < len(images_names):
        image_name = images_names[index]
        image_timestamp = int(image_name[:-4])
        if abs(image_timestamp - timestamp) < best_offset:
            best_offset = abs(image_timestamp - timestamp)
            best_index = index
        else:
            break
        index += 1

    if best_index == -1:
        return None, index
    else:
        return images_names[best_index], index


def get_image_data(image_path):
    with open(image_path, 'rb') as handle:
        data = handle.read()
    imageBGR = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    img_gray = color.rgb2gray(imageRGB)
    img_resized = skimage.transform.resize(img_gray, (192, 256))
    return img_resized


def extract_data(leapmotion_dir, gege_images_dir, didi_images_dir):
    leapmotion_data_names = os.listdir(leapmotion_dir)
    leapmotion_data_names = sorted(leapmotion_data_names)
    gege_images_names = os.listdir(gege_images_dir)
    gege_images_names = sorted(gege_images_names)
    didi_images_names = os.listdir(didi_images_dir)
    didi_images_names = sorted(didi_images_names)
    gege_index = 0
    didi_index = 0
    frame_data_images = []
    frame_data_lms = []
    No = 0
    for leapmotion_data_name in leapmotion_data_names:
        lm_data_path = os.path.join(leapmotion_dir, leapmotion_data_name)
        with open(lm_data_path) as handle:
            lm_raw_data = json.load(handle)
        lm_data = extract_lm_data(lm_raw_data)
        if len(lm_data) == 0:
            continue
        gege_file_name, gege_index = find_nearest_image_file(gege_images_names, leapmotion_data_name, gege_index)
        didi_file_name, didi_index = find_nearest_image_file(didi_images_names, leapmotion_data_name, didi_index)
        if not gege_file_name or not didi_file_name:
            break
        gege_image_data = get_image_data(os.path.join(gege_images_dir, gege_file_name))
        didi_image_data = get_image_data(os.path.join(didi_images_dir, didi_file_name))
        frame_data_images.append([gege_image_data, didi_image_data])
        frame_data_lms.append(lm_data)
        No += 1
        if No % 1 == 0:
            print("%d    " % No, end="\r")
    frame_data_images = np.array(frame_data_images)
    frame_data_lms = np.array(frame_data_lms)
    print(frame_data_images.shape, frame_data_lms.shape)
    return frame_data_images, frame_data_lms


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', type=str)
    parser.add_argument('--output_dir', type=str, default="./output")
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    # datas = []
    No = 0
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            print("Output directory is invalid!")
            exit()
    for dir_name in os.listdir(input_dir):
        if dir_name[0] == '.':
            continue
        dir_path = os.path.join(input_dir, dir_name)
        leapmotion_dir = os.path.join(dir_path, '0')
        gege_images_dir = os.path.join(dir_path, '1')
        didi_images_dir = os.path.join(dir_path, '2')
        images_data, lms_data = extract_data(leapmotion_dir, gege_images_dir, didi_images_dir)
        No += 1
        np.save(os.path.join(output_dir, "input_%d" % No), images_data)
        np.save(os.path.join(output_dir, "output_%d" % No), lms_data)
    #
    # # datas_np = np.array(datas)
    # print("preparing saving")
    # np.save(output_path, datas)
