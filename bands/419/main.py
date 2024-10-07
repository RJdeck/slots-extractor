# %% -------------------------------------------- data_extract --------------------------------------------
from extract import extract_to_log
from preprocess import read_with_index, save_reels2csv, reconstruct_csv, reel_completion, wheel_feature_count, read_free_with_index, wheel_feature_save2csv
from reconstruct import reconstruct_with_index


# 读取原始数据
extract_to_log()

# extract sample log
# extract_to_log('slot_log_sample.json', endswith="419 002.har")


# %% -------------------------------------------- base_game_column --------------------------------------------
print("\n------开始对baseReels进行处理...------\n")

transDict = {"Z": "1101", "S": "1201",
             "B": "1001", "C": "1002", "D": "1003", "E": "1004", "A": "1005", "K": "1006", "Q": "1007", "J": "1008", "T": "1009", "N": "1010"}
base_feature_list = ["baseReels"]


def convert_rule(lst):
    return [[transDict[symbol] for symbol in item] for item in lst]


column_data = read_with_index("slot_log.json", base_feature_list, convert_rule)
reels = reconstruct_with_index(column_data)

# print("reels:", reels)

save_reels2csv(reels, "baseReels_", "output")


reconstruct_csv('baseReels_',
                range(0, 3), 'baseReels.csv', 'output')

print("\n------结束对baseReels的处理------\n")

# %% -------------------------------------------- base_infinity_game_column --------------------------------------------
print("\n------开始对baseInfinityReels进行处理...------\n")

transDict = {"Z": "1101", "S": "1201",
             "B": "1001", "C": "1002", "D": "1003", "E": "1004", "A": "1005", "K": "1006", "Q": "1007", "J": "1008", "T": "1009", "N": "1010"}
base_feature_list = ["baseInfinityReels"]


def convert_rule(lst):
    return [[transDict[symbol] for symbol in item] for item in lst]


column_data = read_with_index("slot_log.json", base_feature_list, convert_rule)
reels = reconstruct_with_index(column_data)

# here we need to complete the reels and set unseen symbols to 0
for i in range(len(reels)):
    reels[i] = reel_completion([reels[i]])


save_reels2csv(reels, "baseInfinityReels_", "output")


reconstruct_csv('baseInfinityReels_',
                range(0, len(reels)), 'baseInfinityReels.csv', 'output')

print("\n------结束对baseInfinityReels的处理------\n")

# %% -------------------------------------------- wheel_game--------------------------------------------
print("\n------开始对wheelFeature进行处理...------\n")

wheel_feature_list = wheel_feature_count("slot_log.json")

print("wheel_feature_list:", wheel_feature_list)


print("\n------结束对wheelFeature的处理------\n")
# %% -------------------------------------------- free_base_column --------------------------------------------
print("\n------开始对freeReels进行处理...------\n")

transDict = {"Z": "1101", "S": "1201",
             "B": "1001", "C": "1002", "D": "1003", "E": "1004", "A": "1005", "K": "1006", "Q": "1007", "J": "1008", "T": "1009", "N": "1010"}
base_feature_list = ["freeReels"]


def convert_rule(lst):
    return [[transDict[symbol] for symbol in item] for item in lst]


column_data = read_free_with_index(
    "slot_log.json", base_feature_list, convert_rule)
reels = reconstruct_with_index(column_data)

# print("reels:", reels)

save_reels2csv(reels, "freeReels_", "output")


reconstruct_csv('freeReels_',
                range(0, 3), 'freeReels.csv', 'output')

print("\n------结束对freeReels的处理------\n")

# %% -------------------------------------------- free_infinity_column --------------------------------------------
print("\n------开始对freeInfinityReels进行处理...------\n")

transDict = {"Z": "1101", "S": "1201",
             "B": "1001", "C": "1002", "D": "1003", "E": "1004", "A": "1005", "K": "1006", "Q": "1007", "J": "1008", "T": "1009", "N": "1010"}
base_feature_list = ["freeInfinityReels"]


def convert_rule(lst):
    return [[transDict[symbol] for symbol in item] for item in lst]


column_data = read_free_with_index(
    "slot_log.json", base_feature_list, convert_rule)
reels = reconstruct_with_index(column_data)

# here we need to complete the reels and set unseen symbols to 0
for i in range(len(reels)):
    reels[i] = reel_completion([reels[i]])


save_reels2csv(reels, "freeInfinityReels_", "output")


reconstruct_csv('freeInfinityReels_',
                range(0, len(reels)), 'freeInfinityReels.csv', 'output')

print("\n------结束对freeInfinityReels的处理------\n")
