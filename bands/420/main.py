# %% -------------------------------------------- data_extract --------------------------------------------
from extract import extract_to_log
from preprocess import feature_inspector, get_frequency, read_column, save_to_csv, reconstruct_csv, get_free_seleted_frequency, transfromDict
from reconstruct import reconstruct_chip_unique_off,  self_reconstruct


# 读取原始数据
extract_to_log()

# f = feature_inspector("slot_log.json")
# print(f)


# %% -------------------------------------------- base_game_column --------------------------------------------
print("\n------开始对base_game的column进行处理...------\n")

# base_game的特征
base_feature_list = [
    "Scatter Mystery - startingMode - Mode 2",
    "Wild Mystery - startingMode - Mode 2",
    "Pick1 Mystery - startingMode - Mode 2",
    "Pic2 Mystery - startingMode - Mode 2",
    "Pic3 Mystery - startingMode - Mode 2",
    "Pic4 Mystery - startingMode - Mode 2",
    "Ace Mystery - startingMode - Mode 2",
    "King Mystery - startingMode - Mode 2",
    "Queen Mystery - startingMode - Mode 2",
    "Jack Mystery - startingMode - Mode 2",
    "Ten Mystery - startingMode - Mode 2"
]

transDict = {"0": "1101", "10": "1201",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008", "9": "1009", }

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
                'base_reconstruct_column_' + str(column) + '.csv', 'output')
    print("结束对第" + str(column) + "列的处理")

reconstruct_csv('base_reconstruct_column_',
                range(0, 5), 'base_reconstruct_column.csv', 'output')

print("\n------结束对base_game的column进行处理------\n")

# %% -------------------------------------------- free_game_random --------------------------------------------
print("\n------开始对free_game的random进行处理...------\n")
res_random = get_free_seleted_frequency("slot_log.json")

save_to_csv(res_random, 'free_game_random.csv', 'output')
print("\n------结束对free_game的random进行处理------\n")
# %% -------------------------------------------- free_game_column FG pic1 --------------------------------------------
print("\n------开始对free_game的column进行处理...------\n")

# free_game的特征
pic1_feature_list = [
    "FG Pic1 - startingMode - Mode 2"
]

offset = 0

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_pic1 = read_column(
        "slot_log.json", pic1_feature_list, column
    )

    frequency_dict_pic1 = get_frequency(column_data_pic1, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict_pic1)))

    # reconstruct frequency dictionary
    res_dict_pic1 = reconstruct_chip_unique_off(frequency_dict_pic1)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict_pic1)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict_pic1]) or len(res_dict_pic1) == 1:
            break
        res_dict_pic1 = reconstruct_chip_unique_off(res_dict_pic1, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict_pic1)}")

    self_improve_dict_pic1 = self_reconstruct(res_dict_pic1)

    final_dict_pic1 = transfromDict(self_improve_dict_pic1, transDict)
    save_to_csv(final_dict_pic1,
                'pic1_reconstruct_column_' + str(column) + '.csv', 'output')
    print("结束对第" + str(column) + "列的处理")

reconstruct_csv('pic1_reconstruct_column_',
                range(0, 5), 'pic1_reconstruct_column.csv', 'output')

print("\n------结束对pic1的column进行处理------\n")

# %% -------------------------------------------- free_game_column FG pic2 --------------------------------------------
print("\n------开始对free_game的column进行处理...------\n")

# free_game的特征
pic2_feature_list = [
    "FG Pic2 - startingMode - Mode 2"
]

offset = 0

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_pic2 = read_column(
        "slot_log.json", pic2_feature_list, column
    )

    frequency_dict_pic2 = get_frequency(column_data_pic2, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict_pic2)))

    # reconstruct frequency dictionary
    res_dict_pic2 = reconstruct_chip_unique_off(frequency_dict_pic2)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict_pic2)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict_pic2]) or len(res_dict_pic2) == 1:
            break
        res_dict_pic2 = reconstruct_chip_unique_off(res_dict_pic2, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict_pic2)}")

    self_improve_dict_pic2 = self_reconstruct(res_dict_pic2)

    final_dict_pic2 = transfromDict(self_improve_dict_pic2, transDict)
    save_to_csv(final_dict_pic2,
                'pic2_reconstruct_column_' + str(column) + '.csv', 'output')
    print("结束对第" + str(column) + "列的处理")

reconstruct_csv('pic2_reconstruct_column_',
                range(0, 5), 'pic2_reconstruct_column.csv', 'output')

print("\n------结束对pic2的column进行处理------\n")

# %% -------------------------------------------- free_game_column FG pic3 --------------------------------------------

print("\n------开始对free_game的column进行处理...------\n")

# free_game的特征
pic3_feature_list = [
    "FG Pic3 - startingMode - Mode 2"
]

offset = 0

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_pic3 = read_column(
        "slot_log.json", pic3_feature_list, column
    )

    frequency_dict_pic3 = get_frequency(column_data_pic3, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict_pic3)))

    # reconstruct frequency dictionary
    res_dict_pic3 = reconstruct_chip_unique_off(frequency_dict_pic3)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict_pic3)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict_pic3]) or len(res_dict_pic3) == 1:
            break
        res_dict_pic3 = reconstruct_chip_unique_off(res_dict_pic3, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict_pic3)}")

    self_improve_dict_pic3 = self_reconstruct(res_dict_pic3)

    final_dict_pic3 = transfromDict(self_improve_dict_pic3, transDict)
    save_to_csv(final_dict_pic3,
                'pic3_reconstruct_column_' + str(column) + '.csv', 'output')
    print("结束对第" + str(column) + "列的处理")

reconstruct_csv('pic3_reconstruct_column_',
                range(0, 5), 'pic3_reconstruct_column.csv', 'output')

print("\n------结束对pic3的column进行处理------\n")

# %% -------------------------------------------- free_game_column FG pic4 --------------------------------------------
print("\n------开始对free_game的column进行处理...------\n")

# free_game的特征
pic4_feature_list = [
    "FG Pic4 - startingMode - Mode 2"
]

offset = 0

for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_pic4 = read_column(
        "slot_log.json", pic4_feature_list, column
    )

    frequency_dict_pic4 = get_frequency(column_data_pic4, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict_pic4)))

    # reconstruct frequency dictionary
    res_dict_pic4 = reconstruct_chip_unique_off(frequency_dict_pic4)
    print("首次跳过重复后拼接后片段数量:" + str(len(res_dict_pic4)))

    # 逐步增加严格长度
    for strict_num in range(2, 100):
        # 如果严格长度大于最短片段长度，退出循环
        if strict_num > min([len(key) for key in res_dict_pic4]) or len(res_dict_pic4) == 1:
            break
        res_dict_pic4 = reconstruct_chip_unique_off(res_dict_pic4, strict_num)
    print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict_pic4)}")

    self_improve_dict_pic4 = self_reconstruct(res_dict_pic4)

    final_dict_pic4 = transfromDict(self_improve_dict_pic4, transDict)
    save_to_csv(final_dict_pic4,
                'pic4_reconstruct_column_' + str(column) + '.csv', 'output')
    print("结束对第" + str(column) + "列的处理")

reconstruct_csv('pic4_reconstruct_column_',
                range(0, 5), 'pic4_reconstruct_column.csv', 'output')

print("\n------结束对pic4的column进行处理------\n")
