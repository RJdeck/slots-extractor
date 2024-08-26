# %% -------------------------------------------- data_extract --------------------------------------------
from extract import extract_to_log
from preprocess import get_frequency, read_column, save_to_csv, reconstruct_csv, get_random_item, transfromDict, get_blue_random, get_green_random, get_red_random, get_hammer_random, get_table_icons_count
from reconstruct import reconstruct_chip_unique_off,  self_reconstruct


# 读取原始数据
# extract_to_log()

# extract sample log
# extract_to_log('slot_log_sample.json', endswith="416 010 10.har")


# %% -------------------------------------------- base_game_column --------------------------------------------
print("\n------开始对base_game的column进行处理...------\n")

# base_game的特征
base_feature_list = ["BaseGame"]

transDict = {"0": "1101", "11": "1201", "12": "1202", "13": "1203", "14": "1204",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008", "9": "1009", "10": "1010"}

offset = 1

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column
    )

    frequency_dict = get_frequency(column_data_base, None, offset)

    # 删除出现次数小于10的片段
    keys_to_delete = [
        key for key in frequency_dict if frequency_dict[key][offset] < 10]
    for key in keys_to_delete:
        print("删除片段:" + str(key))
        del frequency_dict[key]

    print("原数据片段数量:" + str(len(frequency_dict)))
    # save_to_csv(transfromDict(frequency_dict, transDict),
    #             'base_original_column_' + str(column) + '.csv', 'output')
    save_to_csv(frequency_dict,
                'base_original_column_' + str(column) + '.csv', 'output')

    # reconstruct frequency dictionary
    res_dict = reconstruct_chip_unique_off(frequency_dict)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict]) or len(res_dict) == 1:
            break
        res_dict = reconstruct_chip_unique_off(res_dict, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict)}")

    self_improve_dict = self_reconstruct(res_dict)

    final_dict = transfromDict(self_improve_dict, transDict)
    save_to_csv(final_dict,
                'base_reconstruct_column_' + str(column) + '.csv', 'output')


reconstruct_csv('base_original_column_',
                range(0, 5), 'base_original_column.csv', 'output')

reconstruct_csv('base_reconstruct_column_',
                range(0, 5), 'base_reconstruct_column.csv', 'output')

print("\n------结束对base_game的column的处理------\n")

# %% -------------------------------------------- base_game_random_item --------------------------------------------
print("\n------开始对base_game的random_item进行处理...------\n")
# TODO: fix blue piggy!!!!!!

red_jackpot_dict = get_red_random("slot_log.json")
green_shape_dict, green_times_dict = get_green_random("slot_log.json")
blue_wheel_dict = get_blue_random("slot_log.json")
hammer_dict = get_hammer_random("slot_log.json")
table_icons_count = get_table_icons_count("slot_log.json")


print("红色random items:" + str(red_jackpot_dict))
print("绿色的shape random items:" + str(green_shape_dict))
print("绿色的times random items:" + str(green_times_dict))
print("蓝色random items:" + str(blue_wheel_dict))
print("锤子random items:" + str(hammer_dict))
print("金币出现频率" + str(table_icons_count))

# here we get icons trigger probability
red_trigger_prob = (sum([red_jackpot_dict[key] for key in red_jackpot_dict]
                        ) - hammer_dict['h_Match3'] - blue_wheel_dict["Match3"]) / table_icons_count['red']
green_trigger_prob = (sum([green_shape_dict[key] for key in green_shape_dict]
                          ) - hammer_dict['h_FGs'] - blue_wheel_dict["FGs"]) / table_icons_count['green']
blue_trigger_prob = (blue_wheel_dict["BluePigGameEvent"]
                     - hammer_dict['h_Wheel']) / table_icons_count['blue']

coin_trigger_dict = {"red_coin_trigger": red_trigger_prob,
                     "green_coin_trigger": green_trigger_prob, "blue_coin_trigger": blue_trigger_prob}

print("红色的触发概率:" + str(red_trigger_prob))
print("绿色的触发概率:" + str(green_trigger_prob))
print("蓝色的触发概率:" + str(blue_trigger_prob))
save_to_csv({**red_jackpot_dict, **green_shape_dict, **green_times_dict,
            **blue_wheel_dict, **hammer_dict, **coin_trigger_dict}, 'slots_random_items.csv', 'output')

print("\n------结束对base_game的random_item进行处理------\n")

# %% -------------------------------------------- free_game_column1 --------------------------------------------
print("\n------开始对free_game_1的column进行处理 Free4x5...------\n")

# base_game的特征
base_feature_list = ["Free4x5"]

transDict = {"0": "1101", "11": "1201", "12": "1202", "13": "1203", "14": "1204",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008", "9": "1009", "10": "1010"}

offset = 1

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column
    )

    frequency_dict = get_frequency(column_data_base, None, offset)

    # # 删除出现次数小于10的片段
    # keys_to_delete = [
    #     key for key in frequency_dict if frequency_dict[key][offset] < 10]
    # for key in keys_to_delete:
    #     print("删除片段:" + str(key))
    #     del frequency_dict[key]

    print("原数据片段数量:" + str(len(frequency_dict)))
    # save_to_csv(transfromDict(frequency_dict, transDict),
    #             'base_original_column_' + str(column) + '.csv', 'output')

    # reconstruct frequency dictionary
    res_dict = reconstruct_chip_unique_off(frequency_dict)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict]) or len(res_dict) == 1:
            break
        res_dict = reconstruct_chip_unique_off(res_dict, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict)}")

    self_improve_dict = self_reconstruct(res_dict)

    final_dict = transfromDict(self_improve_dict, transDict)
    save_to_csv(final_dict,
                'free4_reconstruct_column_' + str(column) + '.csv', 'output')


# reconstruct_csv('base_original_column_',
#                 range(0, 5), 'base_original_column.csv', 'output')

reconstruct_csv('free4_reconstruct_column_',
                range(0, 5), 'free4_reconstruct_column.csv', 'output')

print("\n------结束对free_game_1的column Free4x5 进行的处理------\n")

# %% -------------------------------------------- free_game_column2 --------------------------------------------
print("\n------开始对free_game_2的column进行处理 Free5x5...------\n")

# base_game的特征
base_feature_list = ["Free5x5"]

transDict = {"0": "1101", "11": "1201", "12": "1202", "13": "1203", "14": "1204",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008", "9": "1009", "10": "1010"}

offset = 0

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column
    )

    frequency_dict = get_frequency(column_data_base, None, offset)

    # # 删除出现次数小于10的片段
    # keys_to_delete = [
    #     key for key in frequency_dict if frequency_dict[key][offset] < 10]
    # for key in keys_to_delete:
    #     print("删除片段:" + str(key))
    #     del frequency_dict[key]

    print("原数据片段数量:" + str(len(frequency_dict)))
    # save_to_csv(transfromDict(frequency_dict, transDict),
    #             'base_original_column_' + str(column) + '.csv', 'output')

    # reconstruct frequency dictionary
    res_dict = reconstruct_chip_unique_off(frequency_dict)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict]) or len(res_dict) == 1:
            break
        res_dict = reconstruct_chip_unique_off(res_dict, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict)}")

    self_improve_dict = self_reconstruct(res_dict)

    final_dict = transfromDict(self_improve_dict, transDict)
    save_to_csv(final_dict,
                'free5_reconstruct_column_' + str(column) + '.csv', 'output')


# reconstruct_csv('base_original_column_',
#                 range(0, 5), 'base_original_column.csv', 'output')

reconstruct_csv('free5_reconstruct_column_',
                range(0, 5), 'free5_reconstruct_column.csv', 'output')

print("\n------结束对free_game_1的column Free5x5 进行的处理------\n")
# %%

# %%
