import sys, os
import argparse
import pandas
import imageio


def read_csv(file_path):
    with open(file_path) as handle:
        lines = handle.readlines()
    line_No = 1
    time_list = []
    if len(lines) == 2:
        line = lines[1]
        items = line.strip().split(", ")
        time_list.append(["free", items[1], items[2]])
        return time_list
    while line_No < len(lines):
        line = lines[line_No]
        items = line.strip().split(", ")
        time_list.append([items[0], items[1], items[2]])
        line_No += 1
    return time_list


def move_files(images_dir, images_target_dir, target_file_names_series):
    for image_file_name in target_file_names_series:
        os.rename(os.path.join(images_dir, image_file_name), os.path.join(images_target_dir, image_file_name))
    # try:
    #     images = []
    #     for image_file_name in target_file_names_series:
    #         images.append(imageio.imread(os.path.join(images_target_dir, image_file_name)))
    #     imageio.mimsave(os.path.join(images_target_dir, "preview.gif"), images)
    # except Exception as e:
    #     print(e)
    #     print(images_target_dir)

def arrange_data(main_dir_path, time_list, image_names_1_series, image_names_2_series, images_1_dir, images_2_dir):
    next_file_name_dict = {}
    if len(time_list) == 1:
        os.mkdir(os.path.join(main_dir_path, "free"))
        next_file_name_dict["free"] = 0
    else:
        for i in range(9):
            os.mkdir(os.path.join(main_dir_path, str(i)))
            next_file_name_dict[str(i)] = 0

    for time_info in time_list:
        folder_path = os.path.join(main_dir_path, time_info[0], str(next_file_name_dict[time_info[0]]))
        next_file_name_dict[time_info[0]] += 1
        images_1_target_dir = os.path.join(folder_path, "1")
        images_2_target_dir = os.path.join(folder_path, "2")
        os.mkdir(folder_path)
        os.mkdir(images_1_target_dir)
        os.mkdir(images_2_target_dir)
        time_start, time_end = time_info[1], time_info[2]
        target_file_names_1_series = image_names_1_series[
            image_names_1_series.between(time_start + ".jpg", time_end + ".jpg")]
        target_file_names_2_series = image_names_2_series[
            image_names_2_series.between(time_start + ".jpg", time_end + ".jpg")]
        move_files(images_1_dir, images_1_target_dir, target_file_names_1_series)
        move_files(images_2_dir, images_2_target_dir, target_file_names_2_series)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('time_dir', type=str)
    parser.add_argument('images_1_dir', type=str)
    parser.add_argument('images_2_dir', type=str)
    parser.add_argument('--output_dir', type=str, default="./output")
    args = parser.parse_args()
    time_dir = args.time_dir
    images_1_dir = args.images_1_dir
    images_2_dir = args.images_2_dir
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            print("Output directory is invalid!")
            exit()
    image_names_1_list = os.listdir(images_1_dir)
    image_names_2_list = os.listdir(images_2_dir)
    image_names_1_series = pandas.Series(image_names_1_list)
    image_names_2_series = pandas.Series(image_names_2_list)
    for file_name in os.listdir(time_dir):
        time_list = read_csv(os.path.join(time_dir, file_name))
        main_dir_name = file_name[:-4]
        main_dir_path = os.path.join(output_dir, main_dir_name)
        try:
            os.mkdir(main_dir_path)
        except Exception as e:
            print(e)
        arrange_data(main_dir_path, time_list, image_names_1_series, image_names_2_series, images_1_dir, images_2_dir)
