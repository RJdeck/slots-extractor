

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
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    column_data = []
    for slot_data in slot_data_list:
        for slot in slot_data:
            if slot["features"]:
                for feature_name in slot["features"]:
                    if feature_name.get("name") in feature_list:
                        if slot["symbols"]:
                            if convert_rule:
                                column_data.append(convert_rule(
                                    slot["symbols"][column_number]))
                            else:
                                column_data.append(
                                    slot["symbols"][column_number])
                    else:
                        continue
    return column_data


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
