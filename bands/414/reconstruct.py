
import logging
import copy
import os

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


def reconstruct_chip(frequency_dict, stict_num=1):
    """
    Reconstructs a chip based on a frequency dictionary.

    Args:
        frequency_dict (dict): A dictionary containing frequencies for each key.
        stict_num (int, optional): The number of characters to match strictly. Defaults to 1.

    Returns:
        dict: The reconstructed frequency dictionary.

    """
    # 对输入字典进行深拷贝
    freq_dict = copy.deepcopy(frequency_dict)

    def get_match_length(key1, key2):
        return min(len(key1), len(key2))-stict_num

    def merge_keys(key1, key2, match_length):
        logging.info(f"Starting merge: {key1} + {key2} ({match_length})")
        combined_key = key1 + key2[match_length:]
        combined_frequency = freq_dict[key1][:-match_length] + [x + y for x, y in zip(
            freq_dict[key1][-match_length:], freq_dict[key2][:match_length])] + freq_dict[key2][match_length:]
        return combined_key, combined_frequency

    def find_match(key1, target_dict):
        res = None
        multiple_matches = False
        match_length = 0

        for key2 in target_dict:
            if key1 == key2:
                continue
            current_match_length = get_match_length(key1, key2)

            if key1[-current_match_length:] == key2[:current_match_length]:
                if res is None:
                    res = key2
                    match_length = current_match_length
                    logging.info(f"Match found: {
                                 key1} + {res} ({current_match_length})")
                    # check if key2 also matches with another key
                    for key3 in target_dict:
                        if key2 == key3 or key1 == key3:
                            continue
                        if key3[-current_match_length:] == key2[:current_match_length]:
                            logging.info(f"Multiple matches found: {key2} also matches with {
                                         key3} ({current_match_length})")
                            multiple_matches = True
                            res = None
                            break
                else:
                    logging.info(f"Multiple matches found: {key1} also matches with {
                                 key2} ({current_match_length})")
                    multiple_matches = True
                    break

        if multiple_matches:
            logging.info(f"Multiple matches for {key1}, returning None")
            return None, 0

        return res, match_length

    def reconstruct(freq_dict):
        # 使用字典的副本进行操作
        temp_dict = freq_dict.copy()
        match_found = False

        for key1 in temp_dict:
            matching_key2, match_length = find_match(key1, temp_dict)

            if matching_key2 is not None:
                logging.info(
                    f"Combining: {key1} + {matching_key2} ({match_length})")
                combined_key, combined_frequency = merge_keys(
                    key1, matching_key2, match_length)
                freq_dict[combined_key] = combined_frequency

                del freq_dict[key1]
                del freq_dict[matching_key2]
                logging.info(f"Reconstructed: {
                             key1} + {matching_key2} -> {combined_key} ({match_length})" + "\n")

                match_found = True
                break
            else:
                if match_length == 0:
                    logging.info(f"No unique match found for: {key1}" + "\n")

        if match_found:
            reconstruct(freq_dict)

    reconstruct(freq_dict)

    return freq_dict


def reconstruct_chip_unique_off(frequency_dict, stict_num=1):
    """
    Reconstructs a chip based on a frequency dictionary.

    Args:
        frequency_dict (dict): A dictionary containing frequencies for each key.
        stict_num (int, optional): The number of characters to match strictly. Defaults to 1.

    Returns:
        dict: The reconstructed frequency dictionary.

    """
    # 对输入字典进行深拷贝
    freq_dict = copy.deepcopy(frequency_dict)

    def get_match_length(key1, key2):
        return max(min(len(key1), len(key2))-stict_num, 1)

    def merge_keys(key1, key2, match_length):
        logging.info(f"Starting merge: {key1} + {key2} ({match_length})")
        combined_key = key1 + key2[match_length:]
        combined_frequency = freq_dict[key1][:-match_length] + [x + y for x, y in zip(
            freq_dict[key1][-match_length:], freq_dict[key2][:match_length])] + freq_dict[key2][match_length:]
        return combined_key, combined_frequency

    def find_match(key1, target_dict):
        res = None
        match_length = 0

        for key2 in target_dict:
            if key1 == key2:
                continue
            current_match_length = get_match_length(key1, key2)

            if key1[-current_match_length:] == key2[:current_match_length]:
                if res is None:
                    res = key2
                    match_length = current_match_length
                    logging.info(f"Match found: {
                                 key1} + {res} ({match_length})")
                    break  # 先到先得，找到第一个匹配就退出循环

        return res, match_length

    def reconstruct(freq_dict):
        # 使用字典的副本进行操作
        temp_dict = freq_dict.copy()
        match_found = False

        for key1 in temp_dict:
            matching_key2, match_length = find_match(key1, temp_dict)

            if matching_key2 is not None:
                logging.info(
                    f"Combing: {key1} + {matching_key2} ({match_length})")
                combined_key, combined_frequency = merge_keys(
                    key1, matching_key2, match_length)
                freq_dict[combined_key] = combined_frequency

                del freq_dict[key1]
                del freq_dict[matching_key2]
                logging.info(f"Reconstructed: {
                             key1} + {matching_key2} -> {combined_key} ({match_length})" + "\n")

                match_found = True
                break
            else:
                if match_length == 0:
                    logging.info(f"No unique match found for: {key1}" + "\n")

        if match_found:
            reconstruct(freq_dict)

    reconstruct(freq_dict)

    return freq_dict


def reconstruct_chip_multi(frequency_dict, stict_num=1):
    """
    Reconstructs a chip based on a frequency dictionary.

    Args:
        frequency_dict (dict): A dictionary containing frequencies for each key.
        stict_num (int, optional): The number of characters to match strictly. Defaults to 1.

    Returns:
        dict: The reconstructed frequency dictionary.

    """
    # 对输入字典进行深拷贝
    freq_dict = copy.deepcopy(frequency_dict)

    def get_match_length(key1, key2):
        return min(len(key1), len(key2)) - stict_num

    def merge_keys(key1, key2, match_length, devide_value=1):
        logging.info(f"Starting merge: {
                     key1} + {key2} ({match_length}) frequency divided by {devide_value} {freq_dict[key2]}")

        combined_key = key1 + key2[match_length:]

        divided_freq = [x // devide_value for x in freq_dict[key1]]
        combined_frequency = divided_freq[:-match_length] + [x + y for x, y in zip(
            divided_freq[-match_length:], freq_dict[key2][:match_length])] + freq_dict[key2][match_length:]
        return combined_key, combined_frequency

    def find_match(key1, target_dict):
        res = {}

        for key2 in target_dict:
            if key1 == key2:
                continue
            current_match_length = get_match_length(key1, key2)

            if key1[-current_match_length:] == key2[:current_match_length]:
                res.update({key2: current_match_length})
                logging.info(f"Match found: {
                             key1} + {key2} ({current_match_length})")
        if len(res) > 1:
            logging.info(
                f"Match completed, multiple matches found for {key1}: {res}")
        return res

    def reconstruct(freq_dict):
        # 使用字典的副本进行操作
        temp_dict = freq_dict.copy()
        match_found = False

        keys_to_delete = []

        for key1 in temp_dict:
            if key1 in keys_to_delete:
                continue
            matching_key2_dict = find_match(key1, temp_dict)

            if matching_key2_dict:
                dict_length = len(matching_key2_dict)

                for matching_key2, match_length in matching_key2_dict.items():
                    logging.info(
                        f"Combing: {key1} + {matching_key2} ({match_length})")
                    combined_key, combined_frequency = merge_keys(
                        key1, matching_key2, match_length, devide_value=dict_length)
                    freq_dict[combined_key] = combined_frequency

                    keys_to_delete.append(matching_key2)
                    logging.info(f"Reconstructed: {
                        key1} -> {matching_key2} -> {combined_key} ({freq_dict[combined_key]})")

                keys_to_delete.append(key1)
                match_found = True

                logging.info(f"Reconstruct finished: {
                    key1} + {matching_key2_dict}" + "\n")

            else:
                if get_match_length(key1, '') == 0:
                    logging.info(f"No unique match found for: {key1}" + "\n")

        for key in keys_to_delete:
            if key in freq_dict:
                del freq_dict[key]

        if match_found:
            reconstruct(freq_dict)

    reconstruct(freq_dict)

    return freq_dict


def self_reconstruct(frequency_dict):
    icon_list = [item for sublist in frequency_dict.keys() for item in sublist]
    freq_list = [item for sublist in frequency_dict.values()
                 for item in sublist]

    for index, freq in enumerate(freq_list[:-4]):
        if freq == 0:
            target_icon_list = icon_list[index:index+5]
            for self_matching_index in range(0, len(freq_list)-4):
                if target_icon_list == icon_list[self_matching_index:self_matching_index+5] and index != self_matching_index:
                    freq_list[index] = freq_list[self_matching_index] // 2
                    freq_list[self_matching_index] = freq_list[index]
                    break
    res_dict = {}
    res_dict[tuple(icon_list)] = freq_list

    return res_dict
