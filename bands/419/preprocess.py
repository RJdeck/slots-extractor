

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


def read_with_index(file_name: str, feature_list: list, convert_rule: Optional[Callable] = None):
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    column_data = {}
    for slot_data in slot_data_list:
        if slot_data.get("generations"):
            for generation in slot_data["generations"]:
                if generation.get("grid"):
                    if generation["grid"] in feature_list:
                        if convert_rule:
                            column_data[tuple(generation["stops"])
                                        ] = convert_rule(generation["symbols"])
                        else:
                            column_data[tuple(generation["stops"])
                                        ] = generation["symbols"]
    return column_data


def read_free_with_index(file_name: str, feature_list: list, convert_rule: Optional[Callable] = None):
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    column_data = {}
    for slot_data in slot_data_list:
        if slot_data.get("freespins"):
            for freespin in slot_data["freespins"]:
                if freespin.get("generations"):
                    for generation in freespin["generations"]:
                        if generation.get("grid"):
                            if generation["grid"] in feature_list:
                                if convert_rule:
                                    column_data[tuple(generation["stops"])
                                                ] = convert_rule(generation["symbols"])
                                else:
                                    column_data[tuple(generation["stops"])
                                                ] = generation["symbols"]
    return column_data


def reel_completion(reels):
    res_reels = {i: ['0', 0] for i in range(300)}

    for reel in reels:
        for index, (symbol, count) in reel.items():
            res_reels[index][0] = symbol
            res_reels[index][1] += int(count)

    return res_reels


def save_reels2csv(reels, file_prefix='base_log', folder_path=None):
    if folder_path:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    for i in range(len(reels)):
        reels[i] = dict(sorted(reels[i].items()))
        # reels[i][0][1] = int(reels[i][0][1]) + \
        #     int(reels[i][len(reels[i])-2][1])
        # reels[i][1][1] = int(reels[i][1][1]) + \
        #     int(reels[i][len(reels[i])-1][1])

        file_name = file_prefix + str(i) + '.csv'
        full_path = os.path.join(
            folder_path, file_name) if folder_path else file_name
        with open(full_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for _, value in list(reels[i].items())[0:len(reels[i])-3]:
                writer.writerow([value[0], value[1]])
    return


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


def wheel_feature_count(file_name: str):
    f = open(file_name, 'r')
    slot_data_list = json.load(f)

    wheel_feature_list = [{} for _ in range(5)]
    for slot_data in slot_data_list:
        if slot_data.get("wheelFeature"):
            for index, item in enumerate(slot_data["wheelFeature"]):
                if item not in wheel_feature_list[index]:
                    wheel_feature_list[index][item] = 1
                else:
                    wheel_feature_list[index][item] += 1

    return wheel_feature_list


def wheel_feature_save2csv(wheel_feature_list, file_name, folder_path=None):
    for i in range(len(wheel_feature_list)):
        file_name = "wheelFeature_" + str(i) + '.csv'
        with open(file_name, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            for key, value in wheel_feature_list[i].items():
                writer.writerow([key, value])
    return
