

from calendar import c
import csv
from email.mime import base
import logging
import os
import re
import time
from unittest import result
import numpy as np
import json
from typing import Callable, Optional


def feature_inspector(file_name: str, filter=None) -> list:
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
                    if filter is not None:
                        if filter in feature["name"]:
                            if feature["name"] not in feature_list:
                                feature_list.append(feature["name"])
                    else:
                        if feature["name"] not in feature_list:
                            feature_list.append(feature["name"])

    return feature_list


def read_column(file_name: str, feature_list: list, column_number: int, convert_rule: Optional[Callable] = None) -> list:
    """
    Reads a specific column from the slot log data based on the given feature and column number.

    Args:
        feature (str): The name of the feature to filter the data by.
        column_number (int): The index of the column to retrieve the data from.
        convert_rule (function): A function to convert the data in the column.

    Returns:
        list: A list containing the data from the specified column.

    """

    base_feature_dict = {
        "Scatter Mystery - startingMode - Mode 2": "10",
        "Wild Mystery - startingMode - Mode 2": "0",
        "Pick1 Mystery - startingMode - Mode 2": "1",
        "Pic2 Mystery - startingMode - Mode 2": "2",
        "Pic3 Mystery - startingMode - Mode 2": "3",
        "Pic4 Mystery - startingMode - Mode 2": "4",
        "Ace Mystery - startingMode - Mode 2": "5",
        "King Mystery - startingMode - Mode 2": "6",
        "Queen Mystery - startingMode - Mode 2": "7",
        "Jack Mystery - startingMode - Mode 2": "8",
        "Ten Mystery - startingMode - Mode 2": "9",
        'FG Pic1 - startingMode - Mode 2': "1",
        'FG Pic2 - startingMode - Mode 2': "2",
        'FG Pic3 - startingMode - Mode 2': "3",
        'FG Pic4 - startingMode - Mode 2': "4",
    }

    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    column_data = []
    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["features"]:
                for feature_name in slot["features"]:
                    if feature_name.get("name") in feature_list:
                        feature = feature_name.get("name")
                        flag = 0
                        if slot["symbols"]:
                            if convert_rule:
                                column_data.append(convert_rule(
                                    slot["symbols"][column_number]))
                            else:
                                for icon in slot["symbols"][column_number]:
                                    if icon == base_feature_dict[feature]:
                                        flag = 1
                                if flag == 0:
                                    column_data.append(
                                        slot["symbols"][column_number])
                    else:
                        continue
    return column_data


def read_column_real(file_name: str, feature_list: list, column_number: int, convert_rule: Optional[Callable] = None) -> list:
    base_feature_dict = {
        "Scatter Mystery": "10",
        "Wild Mystery": "0",
        "Pick1 Mystery": "1",
        "Pic2 Mystery": "2",
        "Pic3 Mystery": "3",
        "Pic4 Mystery": "4",
        "Ace Mystery": "5",
        "King Mystery": "6",
        "Queen Mystery": "7",
        "Jack Mystery": "8",
        "Ten Mystery": "9",
        "FG Pic1": "1",
        "FG Pic2": "2",
        "FG Pic3": "3",
        "FG Pic4": "4",
    }

    with open(file_name, 'r') as f:
        slot_data_list = json.load(f)

    column_data = []
    trans_dict = {
        "Scatter Mystery-y": 0, "Scatter Mystery-n": 0,
        "Wild Mystery-y": 0, "Wild Mystery-n": 0,
        "Pick1 Mystery-y": 0, "Pick1 Mystery-n": 0,
        "Pic2 Mystery-y": 0, "Pic2 Mystery-n": 0,
        "Pic3 Mystery-y": 0, "Pic3 Mystery-n": 0,
        "Pic4 Mystery-y": 0, "Pic4 Mystery-n": 0,
        "Ace Mystery-y": 0, "Ace Mystery-n": 0,
        "King Mystery-y": 0, "King Mystery-n": 0,
        "Queen Mystery-y": 0, "Queen Mystery-n": 0,
        "Jack Mystery-y": 0, "Jack Mystery-n": 0,
        "Ten Mystery-y": 0, "Ten Mystery-n": 0,
        "FG Pic1-y": 0, "FG Pic1-n": 0,
        "FG Pic2-y": 0, "FG Pic2-n": 0,
        "FG Pic3-y": 0, "FG Pic3-n": 0,
        "FG Pic4-y": 0, "FG Pic4-n": 0,
    }
    for slot_data in slot_data_list:
        for slot in slot_data:
            round_feature = None  # 初始化 round_feature
            if slot["features"]:
                for feature_name in slot["features"]:
                    if feature_name.get("name") in feature_list:
                        feature = feature_name.get("name")
                        round_feature = feature.split(' - ')[0]
                        break  # 找到匹配的 feature 后跳出循环
            if round_feature and slot["process"]:
                for process in slot["process"]:
                    if process["round"] == round_feature:
                        column = []
                        if process.get("lastPlayInModeData"):
                            for action in process["lastPlayInModeData"]["slotsData"]["actions"]:
                                if action["ref"] == "spin":
                                    for transform in action["transforms"]:
                                        if transform["ref"] == "spin":
                                            for icon in transform["symbolUpdates"]:
                                                if icon["reelIndex"] == column_number:
                                                    if convert_rule:
                                                        column.append(
                                                            convert_rule(icon["symbol"]))
                                                    else:
                                                        column.append(
                                                            str(icon["symbol"]))

                                    if column:
                                        flag = 0
                                        for i in range(len(column)):
                                            if column[i] in ['11', '12', '13', '14', '15']:
                                                flag = 1
                                        for oringin, transed in zip(column, slot["symbols"][column_number]):
                                            if oringin != transed and transed != base_feature_dict[round_feature]:
                                                # print(f"oringin: {oringin}, transed: {transed}, should be: {
                                                #       base_feature_dict[round_feature]}")
                                                trans_dict[f"{
                                                    round_feature}-n"] += 1
                                                flag = 0
                                                break
                                        if flag == 1:
                                            trans_dict[f"{
                                                round_feature}-y"] += 1
                                        column_data.append(column)

    return column_data, trans_dict


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


def get_free_seleted_frequency(file_name: str):
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    res_dict = {"FG Pic1": 0, "FG Pic2": 0, "FG Pic3": 0, "FG Pic4": 0,
                "Spin times 7": 0, "Spin times 10": 0}
    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["features"]:
                for feature_name in slot["features"]:
                    if feature_name.get("name") == "pickFeature":
                        if feature_name.get("nrOfFreeSpinsTriggered") and feature_name["nrOfFreeSpinsTriggered"] in [7, 10]:
                            if feature_name["nrOfFreeSpinsTriggered"] == 7:
                                res_dict["Spin times 7"] += 1
                            elif feature_name["nrOfFreeSpinsTriggered"] == 10:
                                res_dict["Spin times 10"] += 1
                            res_dict[feature_name["featuresTriggered"][0]] += 1
                        else:
                            continue
    return res_dict


def get_base_seleted_frequency(file_name: str):
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    base_feature_dict = {
        "Scatter Mystery - startingMode - Mode 2": 0,
        "Wild Mystery - startingMode - Mode 2": 0,
        "Pick1 Mystery - startingMode - Mode 2": 0,
        "Pic2 Mystery - startingMode - Mode 2": 0,
        "Pic3 Mystery - startingMode - Mode 2": 0,
        "Pic4 Mystery - startingMode - Mode 2": 0,
        "Ace Mystery - startingMode - Mode 2": 0,
        "King Mystery - startingMode - Mode 2": 0,
        "Queen Mystery - startingMode - Mode 2": 0,
        "Jack Mystery - startingMode - Mode 2": 0,
        "Ten Mystery - startingMode - Mode 2": 0,
        'FG Pic1 - startingMode - Mode 2': 0,
        'FG Pic2 - startingMode - Mode 2': 0,
        'FG Pic3 - startingMode - Mode 2': 0,
        'FG Pic4 - startingMode - Mode 2': 0,
    }

    for slot_data in slot_data_list:
        for slot in slot_data:
            round_feature = None  # 初始化 round_feature
            if slot["features"]:
                for feature_name in slot["features"]:
                    if feature_name.get("name") in base_feature_dict.keys():
                        base_feature_dict[feature_name.get("name")] += 1
                        break  # 找到匹配的 feature 后跳出循环

    # update dict, change key from Scatter Mystery - startingMode - Mode 2 to Scatter Mystery
    base_feature_dict = {key.split(' - ')[0]: value for key,
                         value in base_feature_dict.items()}
    return base_feature_dict
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


def transfromDict(frequency_dict, transDict):
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
