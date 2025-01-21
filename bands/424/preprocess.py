

import csv
from curses import raw
from email.mime import base
import logging
import os
from pyexpat import features
import re
import time
from unittest import result
import numpy as np
import json
from typing import Callable, Optional


def extract_cash_multiplier(s: str) -> str:
    # 找到第一个和第二个波浪号的位置
    first_tilde_index = s.find('~')
    second_tilde_index = s.find('~', first_tilde_index + 1)

    # 截取从开头到第二个波浪号的位置
    return s[:second_tilde_index]


def feature_inspector(file_name: str) -> dict:
    with open(file_name, 'r') as f:
        slot_data_list = json.load(f)

    feature_dict = {}
    for slot in slot_data_list:
        if 'trail' in slot:
            tag_free = 'fsres' if 'fsres' in slot else 'base'
            features = slot['trail'].split(';')
            for feature in features:
                if feature == 'wim~true' and 'slm_mv' in slot:
                    slm_mvs = slot['slm_mv'].split(',')
                    for slm_mv in slm_mvs:
                        modified_feature = tag_free + \
                            'wim~true' + '~' + str(slm_mv)
                        feature_dict[modified_feature] = feature_dict.get(
                            modified_feature, 0) + 1
                elif re.match(r'^cmt~', feature) and 'stf' in slot:
                    stfs = slot['stf'].split(',')
                    skip_feature = False
                    for stf in stfs:
                        if ';' in stf:
                            skip_feature = True
                            break
                    if skip_feature:
                        continue
                    modified_feature = tag_free + feature + '~'
                    feature_dict[modified_feature] = feature_dict.get(
                        modified_feature, 0) + 1
                elif feature == 'fsc~0,10':
                    modified_feature = tag_free + 'fsc~010' + '~'
                    feature_dict[modified_feature] = feature_dict.get(
                        modified_feature, 0) + 1
                else:
                    modified_feature = tag_free + feature + '~'
                    feature_dict[modified_feature] = feature_dict.get(
                        modified_feature, 0) + 1

    return feature_dict


def read_column(file_name: str, column_number: int, is_free: bool) -> list:
    with open(file_name, 'r') as f:
        slot_data_list = json.load(f)

    column_data = []
    for key, slot in enumerate(slot_data_list):
        if 'w' in slot:
            # 检查是否为免费旋转
            if (is_free and 'fsres' in slot) or (not is_free and 'fsres' not in slot):
                # 检查是否为第一个 slot
                if 'w' not in slot_data_list[key - 1] or (slot_data_list[key - 1].get('w') == '0.00'):
                    raw_data = slot['is'].split(',')
                    if(is_free and ("13" in raw_data or 13 in raw_data)):
                        continue
                    column_data.append(
                        [raw_data[i]
                            for i in range(len(raw_data)) if i % 6 == column_number]
                    )
    return column_data


def read_column_res(file_name: str, column_number: int, is_free: bool) -> list:
    with open(file_name, 'r') as f:
        slot_data_list = json.load(f)

    column_data = []
    column_data_res = []
    flag = 0
    for key, slot in enumerate(slot_data_list):
        if 'w' in slot:
            # 检查是否为免费旋转
            if (is_free and 'fsres' in slot) or (not is_free and 'fsres' not in slot):
                # 检查是否为第一个 slot
                if 'w' not in slot_data_list[key - 1] or (slot_data_list[key - 1].get('w') == '0.00'):
                    if 'trail' in slot and 'res~true' in slot['trail']:
                        flag = 1
                    raw_data = slot['is'].split(',')
                    if flag:
                        column_data_res.append(
                            [raw_data[i]
                                for i in range(len(raw_data)) if i % 6 == column_number]
                        )
                        flag = 0
                    else:
                        column_data.append(
                            [raw_data[i]
                                for i in range(len(raw_data)) if i % 6 == column_number]
                        )
                        flag = 0
    return column_data, column_data_res


def drop_unwanted_icons(column: list) -> list:
    for i, column_data in enumerate(column):
        column[i] = [icon for icon in column_data if icon != '23']
    return column


def get_frequency(column_data, convert_rule=None, offset=0):
    """
    Calculate the frequency of each unique row in the column data.

    Args:
        column_data (list): A list of rows, where each row is a list of values.
        convert_rule (function, optional): A function to convert each row before calculating frequency. Defaults to None.

    Returns:
        dict: A dictionary where the keys are unique rows and the values are lists containing the frequency count and zeros.

    Example:
        column_data = [[1, 2, 3], [4, 5, 6], [1, 2, 3], [7, 8, 9]]
        frequency_dict = get_frequency(column_data)
        # Output: {(1, 2, 3): [2, 0, 0], (4, 5, 6): [1, 0, 0], (7, 8, 9): [1, 0, 0]}
    """
    frequency_dict = {}
    length_dict = {}
    for row in column_data:
        if convert_rule:
            row = convert_rule(row)
        row_tuple = tuple(row)  # Convert the list to a tuple
        length = len(row_tuple)
        if length == 4:
            if row_tuple in frequency_dict:
                frequency_dict[row_tuple][offset] += 1
            else:
                frequency_dict[row_tuple] = [0] * len(row_tuple)
                frequency_dict[row_tuple][offset] = 1
        if str(length) in length_dict:
            length_dict[str(length)] += 1
        else:
            length_dict[str(length)] = 1
    return frequency_dict, length_dict


# 从列数据中获取随机项目出现的次数
def get_random_item(column_data, icon):
    icon_count = 0
    for row in column_data:
        for index in range(len(row)):
            if index == 0 or index == 4:
                continue
            if row[index] == icon:
                icon_count += 1
    return icon_count


# 使用中位数来将频率标准化
def standardize_freq_dict(frequency_dict, threshold=0.5):
    # 找到中位数频率
    med_freq = np.median([frequency_dict[key][0] for key in frequency_dict])

    # 更新字典中的频率为对中位数频率的比例
    for key in frequency_dict:
        frequency_dict[key][0] = frequency_dict[key][0]/med_freq

    # 标准化结果，且去除离群值
    for i in range(1, 10):
        for key in frequency_dict:
            if frequency_dict[key][0] > i - threshold and frequency_dict[key][0] < i + threshold:
                frequency_dict[key][0] = i
            elif frequency_dict[key][0] < threshold:
                logging.warning(
                    f"Frequency of {key} with its value {frequency_dict[key][0]} is too low, set to 0.")
                frequency_dict[key][0] = 0

    # 依据标准化后的频率频率返回一个新的数组
    res = []
    for key in frequency_dict:
        if frequency_dict[key][0] != 0:
            for i in range(frequency_dict[key][0]):
                res.append(list(key))

    return res


def transfromDict(frequency_dict, transDict):
    if transDict is None:
        return frequency_dict

    res_key = []
    res_value = []
    res_dict = {}
    for key, value in frequency_dict.items():
        if type(key) == str:
            res_key.append(transDict[key])
            res_value.append(value)
        else:
            for i in range(len(key)):
                res_key.append(transDict[str(key[i])])
                res_value.append(str(value[i]))

    res_dict[tuple(res_key)] = res_value

    return res_dict


def save_to_csv(frequency_dict, file_name='slot_log.csv', folder_path=None):
    """
    Save the frequency dictionary to a CSV file.

    Args:
        frequency_dict (dict): A dictionary containing frequency data.
        file_name (str, optional): The name of the CSV file to save. Defaults to 'slot_log.csv'.
    """
    if folder_path:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    full_path = os.path.join(
        folder_path, file_name) if folder_path else file_name

    with open(full_path, 'w', encoding='utf-8') as f:
        for key, value in frequency_dict.items():
            if type(key) == str:
                f.write(str(key) + ',')
                f.write(str(value) + '\n')
            else:
                for i in range(len(key)):
                    f.write(str(key[i]) + ',')
                    f.write(str(value[i]) + '\n')


def reconstruct_csv(file_prefix, column_range, file_name, folder_path=None, delete_files=True):
    if folder_path:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    full_path = os.path.join(
        folder_path, file_name) if folder_path else file_name

    with open(full_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        # Initialize a list to store the data for each column
        columns_data = []

        # Read data from each column file
        for i in column_range:
            col_file_name = file_prefix + str(i) + ".csv"
            column_file = os.path.join(
                folder_path, col_file_name) if folder_path else col_file_name
            with open(column_file, 'r', encoding='utf-8') as col_file:
                reader = csv.reader(col_file)
                col_data = [row for row in reader]
                columns_data.append(col_data)

            # Remove the column file after reading the data
            if delete_files:
                os.remove(column_file)

        # Determine the maximum number of rows
        max_rows = max(len(col) for col in columns_data)

        # Write data to the new CSV file
        for row_idx in range(max_rows):
            new_row = []
            for col_data in columns_data:
                if row_idx < len(col_data):
                    new_row.extend(col_data[row_idx])
                else:
                    # Add empty strings if the row is missing
                    new_row.extend(['', ''])
            writer.writerow(new_row)
