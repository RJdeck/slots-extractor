# %% -------------------------------------------- data_extract --------------------------------------------
from typing import final

from numpy import save
from extract import extract_to_log
from preprocess import get_frequency, read_column, save_to_csv, get_random_item, transfromDict, reconstruct_csv, read_free_linx_column
from reconstruct import reconstruct_chip_unique_off,  self_reconstruct

# 读取原始数据
extract_to_log()


# %% -------------------------------------------- base_game_column --------------------------------------------


print("\n------开始对base_game的column进行处理...------\n")

# base_game的特征
base_feature_list = ["BaseGame - startingMode - BaseGame",
                     "WildLinXFeature - startingMode - BaseGame"]

transDict = {"0": "1101", "11": "1201",  "10": "1202",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008"}

offset = 1


def convert_rule(lst):

    # 将不同倍率的箭头替换为11
    res = list(map(lambda x: '11' if int(x) in [
               18, 19, 20, 21, 22, 23, 24] else x, lst))

    # 替换不同倍率x图标为0
    res = list(map(lambda x: '0' if int(x) in [
               13, 14, 32, 15, 27, 28, 17, 29, 30, 36] else x, res))
    return res


for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column, convert_rule
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

reconstruct_csv('base_reconstruct_column_',
                range(0, 5), 'base_reconstruct_column.csv', 'output')

print("\n------结束对第" + str(column) + "列的处理------\n")

# %% -------------------------------------------- base_game_random_item --------------------------------------------

print("\n------开始对base_game的random_item进行处理...------\n")

final_random_item_dict = {}

# array出现的特征
array_base_feature_list = ["BaseGame - startingMode - BaseGame",
                           "WildLinXFeature - startingMode - BaseGame"]

# 统计array图标
array_icon_list = [18, 19, 20, 21, 22, 24]
array_random_item_dict = {(str(icon)): 0 for icon in array_icon_list}

for column in range(0, 5):
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", array_base_feature_list, column
    )
    for icon in array_icon_list:
        icon_count = get_random_item(column_data_base, str(icon))
        array_random_item_dict[str(icon)] += icon_count

print("base和linx中箭头项目出现次数:" + str(array_random_item_dict))


# linx中x出现的特征
x_linx_feature_list = ["WildLinXFeature - startingMode - BaseGame"]

# 统计x图标出现次数
x_icon_list = [0, 13, 14, 32, 15, 17, 27, 28, 29, 30]
x_linx_random_item_dict = {(str(icon)): 0 for icon in x_icon_list}

for column in range(0, 5):
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", x_linx_feature_list, column
    )
    for icon in x_icon_list:
        icon_count = get_random_item(column_data_base, str(icon))
        x_linx_random_item_dict[str(icon)] += icon_count
print("linx中x项目出现次数:" + str(x_linx_random_item_dict))


final_random_item_dict = {**array_random_item_dict, **x_linx_random_item_dict}


print("随机项目出现次数:" + str(final_random_item_dict))
save_to_csv(final_random_item_dict, 'base_random_item.csv', 'output')
print("\n------结束对base_game的random_item进行处理------\n")

# %% -------------------------------------------- free_game_column1 --------------------------------------------
print("\n------开始对free_game_1的column进行处理 LinX...------\n")

# base_game的特征
base_feature_list = ["FreeLinXFeature - startingMode - BaseGame"]

transDict = {"0": "1101", "11": "1201",  "10": "1202",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008"}

offset = 1


def convert_rule(lst):

    # 将不同倍率的箭头替换为11
    res = list(map(lambda x: '11' if int(x) in [
               18, 19, 20, 21, 22, 23, 24] else x, lst))

    # 替换不同倍率x图标为0
    res = list(map(lambda x: '0' if int(x) in [
               13, 14, 32, 15, 27, 28, 17, 29, 30, 36] else x, res))
    return res


for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column, convert_rule
    )

    frequency_dict = get_frequency(column_data_base, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict)))

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
                'free_linx_column_' + str(column) + '.csv', 'output')

reconstruct_csv('free_linx_column_',
                range(0, 5), 'free_linx_column.csv', 'output')

print("\n------结束对free_linx_column的处理------\n")
# %% -------------------------------------------- free_game_column1 --------------------------------------------
print("\n------开始对free_game_1的random进行处理 LinX...------\n")

final_random_item_dict = {}

# array出现的特征
array_base_feature_list = ["FreeLinXFeature - startingMode - BaseGame"]

# 统计array图标
array_icon_list = [18, 19, 20, 21, 22, 24]
array_random_item_dict = {(str(icon)): 0 for icon in array_icon_list}

for column in range(0, 5):
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", array_base_feature_list, column
    )
    for icon in array_icon_list:
        icon_count = get_random_item(column_data_base, str(icon))
        array_random_item_dict[str(icon)] += icon_count

print("free linx中箭头项目出现次数:" + str(array_random_item_dict))


# linx中x出现的特征
x_linx_feature_list = ["WildLinXFeature - startingMode - BaseGame"]

# 统计x图标出现次数
x_icon_list = [0, 13, 14, 32, 15, 17, 27, 28, 29, 30]
x_linx_random_item_dict = {(str(icon)): 0 for icon in x_icon_list}

for column in range(0, 5):
    # get base frequency dictionary
    column_data_base = read_free_linx_column(
        "slot_log.json", x_linx_feature_list, column
    )
    for icon in x_icon_list:
        icon_count = get_random_item(column_data_base, str(icon))
        x_linx_random_item_dict[str(icon)] += icon_count
print("free linx中x项目出现次数:" + str(x_linx_random_item_dict))


final_random_item_dict = {**array_random_item_dict, **x_linx_random_item_dict}


print("随机项目出现次数:" + str(final_random_item_dict))
save_to_csv(final_random_item_dict, 'free_linx_random_item.csv', 'output')
print("\n------结束对free_linx的random_item进行处理------\n")

# %% -------------------------------------------- free_game_column2 --------------------------------------------
print("\n------开始对free_game_2的column进行处理 Stacks...------\n")

# base_game的特征
base_feature_list = ["FreeStacksFeature - startingMode - BaseGame"]

#
transDict = {"0": "1101", "11": "1201",  "10": "1202", "31": "31",
             "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005", "6": "1006", "7": "1007", "8": "1008"}

offset = 1


def convert_rule(lst):

    # 将不同倍率的箭头替换为11
    res = list(map(lambda x: '11' if int(x) in [
               18, 19, 20, 21, 22, 23, 24] else x, lst))

    # 替换不同倍率x图标为0
    res = list(map(lambda x: '0' if int(x) in [
               13, 14, 32, 15, 27, 28, 17, 29, 30, 36] else x, res))

    # 替换31图标为4
    res = list(map(lambda x: '4' if int(x) in [31] else x, res))
    return res


for column in range(0, 5):
    print("开始对第" + str(column) + "列的处理")
    # get base frequency dictionary
    column_data_base = read_column(
        "slot_log.json", base_feature_list, column, convert_rule
    )

    frequency_dict = get_frequency(column_data_base, None, offset)

    print("原数据片段数量:" + str(len(frequency_dict)))

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

    final_length = 0
    for key in res_dict:
        final_length += len(res_dict[key])
    print(f"最终带子长度{final_length}")

    self_improve_dict = self_reconstruct(res_dict)

    final_dict = transfromDict(self_improve_dict, transDict)
    save_to_csv(final_dict,
                'free_stacks_column_' + str(column) + '.csv', 'output')

reconstruct_csv('free_stacks_column_',
                range(0, 5), 'free_stacks_column.csv', 'output')

print("\n------结束对free_stacks_column的处理------\n")
