
import random
from collections import Counter
import itertools
import logging
import copy
import os
import re

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建日志文件的路径
log_file_path = os.path.join(current_dir, 'chip_reconstruction.log')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='w'  # 'w' 模式会覆盖已存在的日志文件，如果想要追加使用 'a' 模式
)

#  def reconstruct(target_list):
#         # 使用列表的副本进行操作
#         temp_list = target_list.copy()
#         res_list = []
#         nonused_list = []
#         for chip1 in temp_list:
#             matching_chip2, match_length = find_match(chip1, temp_list)
#             if matching_chip2:
#                 combined_chip = merge_keys(chip1, matching_chip2, match_length)
#                 res_list.append(combined_chip)
#             else:
#                 if chip1 not in nonused_list:
#                     nonused_list.append(chip1)


def simple_reconstruct_chip(chips_list, stict_num=1):
    """
    单次拼接，传入列表，返回拼接后的列表
    """
    # 对输入字典进行深拷贝
    chips_list_copy = copy.deepcopy(chips_list)

    def get_match_length(chip1, chip2):
        return min(len(chip1), len(chip2))-stict_num

    def merge_keys(chip1, chip2, match_length):
        logging.info(f"Starting merge: {chip1} + {chip2} ({match_length})")
        combined_chip = chip1 + chip2[match_length:]
        return combined_chip

    def find_match(chip1, target_list, offset=0):
        match_length = 0
        match_count = 0  # 记录匹配次数

        for chip2 in target_list:
            if chip1 == chip2:
                continue
            current_match_length = get_match_length(chip1, chip2)

            if chip1[-current_match_length:] == chip2[:current_match_length]:
                match_count += 1  # 匹配次数加一
                if match_count > offset:  # 如果匹配次数大于偏移量,则返回匹配结果
                    match_length = current_match_length
                    logging.info(f"Match found: {
                        chip1} + {chip2} ({match_length})")
                    return chip2, match_length

        return None, match_length

    def reconstruct(target_list):
        # 使用列表的副本进行操作
        temp_list = target_list.copy()
        res_list = []
        nonused_list = []

        # while temp_list:
        #     chip1 = temp_list[0]
        #     matching_chip2, match_length = find_match(chip1, temp_list)
        #     if matching_chip2:
        #         combined_chip = merge_keys(chip1, matching_chip2, match_length)
        #         temp_list.remove(chip1)
        #         temp_list.remove(matching_chip2)
        #         res_list.append(combined_chip)
        #     else:
        #         nonused_list.append(chip1)
        #         temp_list.remove(chip1)
        for chip1 in temp_list:
            matching_chip2, match_length = find_match(chip1, temp_list)
            if matching_chip2:
                combined_chip = merge_keys(chip1, matching_chip2, match_length)
                res_list.append(combined_chip)
            else:
                if chip1 not in nonused_list:
                    nonused_list.append(chip1)
        return res_list, nonused_list

    res_list = []
    nonused_list = []
    res_list, nonused_list = reconstruct(chips_list_copy)

    return res_list, nonused_list


def find_valid_pairs(fragments):
    if len(fragments) != 100:
        raise ValueError("The input must contain exactly 100 fragments.")

    def backtrack(pairs, remaining_indices):
        if len(pairs) == 50:
            return pairs

        for _ in range(300):  # 尝试300次，可以根据需要调整
            if len(remaining_indices) < 2:
                return None

            idx1, idx2 = random.sample(remaining_indices, 2)
            pair = (fragments[idx1], fragments[idx2])
            if validator_func(pair):
                new_pairs = pairs + [pair]
                new_remaining = [
                    idx for idx in remaining_indices if idx not in (idx1, idx2)]
                result = backtrack(new_pairs, new_remaining)
                if result:
                    return result

        return None

    for _ in range(1000):  # 尝试1000次，可以根据需要调整
        all_indices = list(range(100))
        random.shuffle(all_indices)
        result = backtrack([], all_indices)
        if result:
            return result

    return None


def validator_func(pair):
    match_length = min(len(pair[0]), len(pair[1]))
    if pair[0][-match_length:] != pair[1][:match_length] or pair[1][-match_length:] != pair[0][:match_length]:
        return False
    return True


def reconstruct_chip_all(chips_list, stict_num=1):
    """
    单次拼接，传入列表，返回拼接后的列表
    """
    # 对输入字典进行深拷贝
    chips_list_copy = copy.deepcopy(chips_list)

    # 看下两个片段匹配的长度
    def get_match_length(chip1, chip2):
        return min(len(chip1), len(chip2))-stict_num

    # 将chip2拼接到chip1后面
    def merge_keys(chip1, chip2, match_length):
        logging.info(f"Starting merge: {chip1} + {chip2} ({match_length})")
        combined_chip = chip1 + chip2[match_length:]
        return combined_chip

    # 返回能接在chip1后面的chip2列表
    def find_match(chip1, target_list):
        match_length = 0
        match_list = []

        for chip2 in target_list:
            if chip1 == chip2 or chip2 in match_list:
                continue
            current_match_length = get_match_length(chip1, chip2)

            if chip1[-current_match_length:] == chip2[:current_match_length]:
                logging.info(f"Match found: {
                    chip1} + {chip2} ({match_length})")
                match_list.append(chip2)

        return match_list

    def reconstruct(target_list):
        # 使用列表的副本进行操作
        temp_list = target_list.copy()
        res_list = []
        nonused_list = []
        loop_list = []

        # 找到所有能接在chip1后面的chip2，并且拼接
        for chip1 in temp_list:
            matching_chip_list = find_match(chip1, temp_list)
            if matching_chip_list:
                for matching_chip in matching_chip_list:
                    match_length = get_match_length(chip1, matching_chip)
                    combined_chip = merge_keys(
                        chip1, matching_chip, match_length)
                    if combined_chip not in res_list:
                        if check_loop(combined_chip):
                            loop_list.append(combined_chip)
                        else:
                            res_list.append(combined_chip)

            # 如果没有匹配的chip2，则将chip1加入nonused_list，这代表上一轮传下来的这个chip1有错，在这一轮匹配中被淘汰
            else:
                if chip1 not in nonused_list:
                    nonused_list.append(chip1)
        return res_list, nonused_list, loop_list

    res_list = []
    nonused_list = []
    res_list, nonused_list, loop_list = reconstruct(chips_list_copy)

    return res_list, nonused_list, loop_list


def check_loop(chip_list):
    """
    检查是否有环
    """
    if chip_list[:4] == chip_list[-4:]:
        return True
    return False
