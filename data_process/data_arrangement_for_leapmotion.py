import sys, os
import argparse
import pandas


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


def arrange_data(main_dir_path, time_list, raw_data_name_series, raw_data_dir):
    next_file_name = 0
    for time_info in time_list:
        folder_path = os.path.join(main_dir_path, str(next_file_name))
        next_file_name += 1
        try:
            os.mkdir(folder_path)
        except Exception as e:
            print(e)
        time_start, time_end = time_info[1], time_info[2]
        target_file_names_series = raw_data_name_series[
            raw_data_name_series.between(time_start + ".dat", time_end + ".dat")]
        print(time_start + ".dat", time_end + ".dat", len(raw_data_name_series), len(target_file_names_series), raw_data_name_series[10000])
        move_files(raw_data_dir, folder_path, target_file_names_series)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('time_dir', type=str)
    parser.add_argument('raw_data_dir', type=str)
    parser.add_argument('--output_dir', type=str, default="./output_leapmotion")
    args = parser.parse_args()
    time_dir = args.time_dir
    raw_data_dir = args.raw_data_dir
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except:
            print("Output directory is invalid!")
            exit()
    raw_data_name_list = os.listdir(raw_data_dir)
    raw_data_name_series = pandas.Series(raw_data_name_list)
    for file_name in os.listdir(time_dir):
        time_list = read_csv(os.path.join(time_dir, file_name))
        main_dir_name = file_name[:-4]
        main_dir_path = os.path.join(output_dir, main_dir_name)
        try:
            os.mkdir(main_dir_path)
        except Exception as e:
            print(e)
        arrange_data(main_dir_path, time_list, raw_data_name_series, raw_data_dir)
