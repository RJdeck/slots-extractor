

import csv
from curses import raw
from email.mime import base
import logging
import os
import re
import time
from unittest import result
import numpy as np
import json
from typing import Callable, Optional


def feature_inspector(file_name: str, filter="startingMode - BaseGame") -> list:
    """
    Count the number of features in the slot log data.

    Args:
        file_name (str): The name of the JSON file containing the slot log data.

    Returns:
        list: A list containing the names of the features in the slot log data.

    """
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    feature_list = []
    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["features"]:
                for feature in slot["features"]:
                    if filter in feature["name"]:
                        if feature["name"] not in feature_list:
                            feature_list.append(feature["name"])
    return feature_list


def read_column(file_name: str, column_number: int, is_free: bool) -> list:
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    column_data = []
    for key, slot in enumerate(slot_data_list):
        if 'w' in slot:
            # check if is free spin or not
            if is_free:
                if 'fsres' in slot:
                    # check if is the first slot
                    if ('w' not in slot_data_list[key - 1]):
                        raw_data = slot['s'].split(',')
                        column_data.append(
                            [raw_data[i] for i in range(len(raw_data)) if i % 6 == column_number])
                    if ('w' in slot_data_list[key - 1] and slot_data_list[key - 1]['w'] == '0.00'):
                        raw_data = slot['s'].split(',')
                        column_data.append(
                            [raw_data[i] for i in range(len(raw_data)) if i % 6 == column_number])
            else:
                if 'fsres' not in slot:
                    # check if is the first slot
                    if ('w' not in slot_data_list[key - 1]):
                        raw_data = slot['s'].split(',')
                        column_data.append(
                            [raw_data[i] for i in range(len(raw_data)) if i % 6 == column_number])
                    if ('w' in slot_data_list[key - 1] and slot_data_list[key - 1]['w'] == '0.00'):
                        raw_data = slot['s'].split(',')
                        column_data.append(
                            [raw_data[i] for i in range(len(raw_data)) if i % 6 == column_number])
    return column_data

def get_boom_random(file_name: str) -> dict:
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    result_dict = {}
    for slot_data in slot_data_list:
        if 'rmul' in slot_data:
            raw_list = slot_data['rmul'].split(';')
            for boom in raw_list:
                multipule = boom.split('~')[2]
                if multipule not in result_dict:
                    result_dict[multipule] = 1
                else:
                    result_dict[multipule] += 1
    return result_dict

def get_red_random(file_name: str) -> dict:
    result_dict = {"MINI": 0, "MINOR": 0, "MAJOR": 0, "GRAND": 0}

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["round"] == "Match3":
                if slot.get("lastPlayInModeData"):
                    for payoutResult in slot["lastPlayInModeData"]["listPickData"]["payoutResults"]:
                        if payoutResult["context"].get("name"):
                            result_dict[payoutResult["context"]["name"]] += 1
    return result_dict


def get_green_random(file_name: str) -> dict:
    shape_dict = {"Free4x5": 0, "Free5x5": 0}
    times_dict = {"6": 0, "8": 0, "10": 0}

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["round"] == "FGs":
                if slot.get("lastPlayInModeData"):
                    for payoutResult in slot["lastPlayInModeData"]["listPickData"]["payoutResults"]:
                        for payoutFreePlayResultsData in payoutResult["payoutData"]["payoutFreePlayResultsData"]:
                            if payoutFreePlayResultsData.get("round") and payoutFreePlayResultsData.get("playCount"):
                                shape_dict[payoutFreePlayResultsData["round"]] += 1
                                times_dict[str(
                                    payoutFreePlayResultsData["playCount"])] += 1
    return shape_dict, times_dict


def get_blue_random(file_name: str) -> dict:
    feature_dict = {}
    multi_dict = {}

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["round"] == "Wheel":
                # print the index of this slot
                if slot.get("lastPlayInModeData"):
                    for payoutResult in slot["lastPlayInModeData"]["listPickData"]["payoutResults"]:
                        for payoutFreePlayResultsData in payoutResult["payoutData"]["payoutFreePlayResultsData"]:
                            if payoutFreePlayResultsData.get("round") and payoutFreePlayResultsData.get("playCount"):
                                if payoutFreePlayResultsData["round"] not in feature_dict:
                                    feature_dict[payoutFreePlayResultsData["round"]] = 1
                                else:
                                    feature_dict[payoutFreePlayResultsData["round"]] += 1
            if slot["round"] == "WheelMultiplier":
                if slot.get("lastPlayInModeData"):
                    # get the betCost through the previous slot
                    pre_slot_data = slot_data_list[slot_data_list.index(
                        slot_data)-1]
                    for pre_slot in pre_slot_data:
                        if pre_slot["round"] == "Wheel":
                            bet_cost = pre_slot["betCost"]
                            if bet_cost == 0:
                               # here we know the wrong data comes from the betCost = 1000
                                bet_cost = 1000
                    if str(slot["lastPlayInModeData"]["playWinAmount"]/bet_cost) not in multi_dict:
                        multi_dict[str(slot["lastPlayInModeData"]
                                       ["playWinAmount"]/bet_cost)] = 1
                    else:
                        multi_dict[str(slot["lastPlayInModeData"]
                                       ["playWinAmount"]/bet_cost)] += 1
    return {**feature_dict, **multi_dict}


def get_hammer_random(file_name: str) -> dict:
    feature_dict = {"h_Match3": 0, "h_Wheel": 0, "h_FGs": 0}

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["round"] == "FeaturePick":
                if slot.get("lastPlayInModeData"):
                    for payoutResult in slot["lastPlayInModeData"]["listPickData"]["payoutResults"]:
                        for payoutFreePlayResultsData in payoutResult["payoutData"]["payoutFreePlayResultsData"]:
                            if payoutFreePlayResultsData.get("round"):
                                feature_dict["h_" +
                                             payoutFreePlayResultsData["round"]] += 1
    return feature_dict


# weather using flags meaing count the same icon only once in one spin or not
def get_table_icons_count(file_name: str) -> dict:
    icons_count_dict = {"green": 0, "blue": 0, "red": 0}

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["round"] in "BaseGame":
                if slot.get("lastPlayInModeData"):
                    for action in slot["lastPlayInModeData"]["slotsData"]["actions"]:
                        if action["ref"] == "spin":
                            for transform in action["transforms"]:
                                if transform["ref"] == "spin":
                                    for icon in transform["symbolUpdates"]:
                                        green_flag = False
                                        blue_flag = False
                                        red_flag = False
                                        if icon["symbol"] == 12 and not green_flag:
                                            icons_count_dict["green"] += 1
                                            # green_flag = True
                                        if icon["symbol"] == 13 and not blue_flag:
                                            icons_count_dict["blue"] += 1
                                            # blue_flag = True
                                        if icon["symbol"] == 14 and not red_flag:
                                            icons_count_dict["red"] += 1
                                            # red_flag = True

    return icons_count_dict


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
    for row in column_data:
        if convert_rule:
            row = convert_rule(row)
        row_tuple = tuple(row)  # Convert the list to a tuple
        if row_tuple in frequency_dict:
            frequency_dict[row_tuple][offset] += 1
        else:
            frequency_dict[row_tuple] = [0] * len(row_tuple)
            frequency_dict[row_tuple][offset] = 1
    return frequency_dict


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
