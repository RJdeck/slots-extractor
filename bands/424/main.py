# %% -------------------------------------------- data_extract --------------------------------------------
from typing import final
from extract import extract_to_log, extrac_to_log_double
from preprocess import read_column, read_column_res
from extract import extract_to_log
from preprocess import (
    feature_inspector, get_frequency, read_column, save_to_csv,
    reconstruct_csv,  transfromDict, drop_unwanted_icons
)
from reconstruct import reconstruct_chip_unique_off, self_reconstruct

# 读取原始数据
# extract_to_log(save_file_name='slot_log.json', endswith='.har')
res = feature_inspector('slot_log.json')
print(res)
save_to_csv(res, 'random.csv', 'output')



# %% -------------------------------------------- base_game_column --------------------------------------------
print("\n------开始对base_game的column进行处理...------\n")

transDict = {
    "1": "1401", "2": "1101", "13": "1202",
    "3": "1001", "4": "1002", "5": "1003", "6": "1004", "7": "1005", "8": "1006", "9": "1007", "10": "1008", "11": "1009", "12": "1010",
}

offset = 0

for column in range(0, 6):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", column, False
    )

    column_data_base = drop_unwanted_icons(column_data_base)

    frequency_dict, length_dict = get_frequency(column_data_base, None, offset)

    # 删除出现次数小于10的片段
    keys_to_delete = [
        key for key in frequency_dict if frequency_dict[key][offset] < 5]
    for key in keys_to_delete:
        print("删除片段:" + str(key))
        del frequency_dict[key]

    print("原数据片段数量:" + str(len(frequency_dict)))
    save_to_csv(transfromDict(frequency_dict, transDict),
                'base_original_column_' + str(column) + '.csv', 'output')
    # save_to_csv(frequency_dict,
    #             'base_original_column_' + str(column) + '.csv', 'output')
    save_to_csv(length_dict,
                'base_length_column_' + str(column) + '.csv', 'output')

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
                range(0, 6), 'base_original_column.csv', 'output')
reconstruct_csv('base_length_column_',
                range(0, 6), 'base_length_column.csv', 'output')

reconstruct_csv('base_reconstruct_column_',
                range(0, 6), 'base_reconstruct_column.csv', 'output')

print("\n------结束对base_game的column的处理------\n")

# %% -------------------------------------------- free_game_column --------------------------------------------
print("\n------开始对free_game的column进行处理...------\n")

transDict = {
    "1": "1401", "2": "1101", "13": "1202",
    "3": "1001", "4": "1002", "5": "1003", "6": "1004", "7": "1005", "8": "1006", "9": "1007", "10": "1008", "11": "1009", "12": "1010",
}

offset = 0

for column in range(0, 6):
    print("开始对第" + str(column) + "列的处理")
    # get free frequency dictionary
    column_data_free = read_column(
        "slot_log.json", column, False
    )
    column_data_free = drop_unwanted_icons(column_data_free)

    frequency_dict, length_dict = get_frequency(column_data_free, None, offset)

    # # 删除出现次数小于10的片段
    # keys_to_delete = [
    #     key for key in frequency_dict if frequency_dict[key][offset] < 5]
    # for key in keys_to_delete:
    #     print("删除片段:" + str(key))
    #     del frequency_dict[key]

    print("原数据片段数量:" + str(len(frequency_dict)))
    save_to_csv(transfromDict(frequency_dict, transDict),
                'free_original_column_' + str(column) + '.csv', 'output')
    # save_to_csv(frequency_dict,
    #             'base_original_column_' + str(column) + '.csv', 'output')
    save_to_csv(length_dict,
                'free_length_column_' + str(column) + '.csv', 'output')

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
                'free_reconstruct_column_' + str(column) + '.csv', 'output')


reconstruct_csv('free_original_column_',
                range(0, 6), 'free_original_column.csv', 'output')
reconstruct_csv('free_length_column_',
                range(0, 6), 'free_length_column.csv', 'output')

reconstruct_csv('free_reconstruct_column_',
                range(0, 6), 'free_reconstruct_column.csv', 'output')

print("\n------结束对base_game的column的处理------\n")

# %% -------------------------------------------- random --------------------------------------------
# print("\n------开始对random进行处理...------\n")
# random_res = get_boom_random("slot_log.json")
# save_to_csv(random_res, 'random.csv', 'output')
# print("\n------结束对random的处理------\n")
# # %% -------------------------------------------- double_game_column --------------------------------------------
# print("\n------开始对double_game的column进行处理...------\n")

# extrac_to_log_double(save_file_name='slot_log.json', endswith='double.har')

# transDict = {
#     "1": "1201", "12": "1202",
#     "3": "1001", "4": "1002", "5": "1003", "6": "1004", "7": "1005", "8": "1006", "9": "1007", "10": "1008", "11": "1009",
# }

# offset = 4

# for column in range(0, 6):
#     print("开始对第" + str(column) + "列的处理")
#     # get base frequency dictionary
#     column_data_base = read_column(
#         "slot_log.json", column, False
#     )

#     frequency_dict = get_frequency(column_data_base, None, offset)

#     # 删除出现次数小于10的片段
#     keys_to_delete = [
#         key for key in frequency_dict if frequency_dict[key][offset] < 10]
#     for key in keys_to_delete:
#         print("删除片段:" + str(key))
#         del frequency_dict[key]

#     print("原数据片段数量:" + str(len(frequency_dict)))
#     # save_to_csv(transfromDict(frequency_dict, transDict),
#     #             'base_original_column_' + str(column) + '.csv', 'output')
#     save_to_csv(transfromDict(frequency_dict, transDict),
#                 'double_original_column_' + str(column) + '.csv', 'output')

#     # reconstruct frequency dictionary
#     res_dict = reconstruct_chip_unique_off(frequency_dict)
#     print("首次跳过重复后拼接后片段数量:" + str(len(res_dict)))

#     # 逐步增加严格长度
#     for strict_num in range(2, 100):
#         # 如果严格长度大于最短片段长度，退出循环
#         if strict_num > min([len(key) for key in res_dict]) or len(res_dict) == 1:
#             break
#         res_dict = reconstruct_chip_unique_off(res_dict, strict_num)
#     print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict)}")

#     self_improve_dict = self_reconstruct(res_dict)

#     final_dict = transfromDict(self_improve_dict, transDict)
#     save_to_csv(final_dict,
#                 'double_reconstruct_column_' + str(column) + '.csv', 'output')


# reconstruct_csv('double_original_column_',
#                 range(0, 6), 'double_original_column.csv', 'output')

# reconstruct_csv('double_reconstruct_column_',
#                 range(0, 6), 'double_reconstruct_column.csv', 'output')

# print("\n------结束对double_game的column的处理------\n")


11

22

33