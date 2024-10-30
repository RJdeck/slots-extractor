from calendar import c
from extract import extract_to_log
from preprocess import (
    feature_inspector, get_frequency, read_column, save_to_csv,
    reconstruct_csv, get_free_seleted_frequency, transfromDict, read_column_real, get_base_seleted_frequency
)
from reconstruct import reconstruct_chip_unique_off, self_reconstruct


def process_columns(features, prefix, transDict, offset=0):
    for column in range(5):
        print(f"开始对第{column}列的处理")

        # Read and process column data
        column_data, trans_random = read_column_real(
            "slot_log.json", features, column)

        save_to_csv(trans_random, f'{prefix}_random_column_{
                    column}.csv', 'output')
        frequency_dict = get_frequency(column_data, None, offset)
        save_to_csv(transfromDict(frequency_dict, transDict),
                    f'{prefix}_original_column_{column}.csv', 'output')

        # Reconstruct frequency dictionary
        res_dict = reconstruct_chip_unique_off(frequency_dict)
        print(f"首次跳过重复后拼接后片段数量: {len(res_dict)}")

        # Increase strict length
        for strict_num in range(2, 100):
            if strict_num > min(len(key) for key in res_dict) or len(res_dict) == 1:
                break
            res_dict = reconstruct_chip_unique_off(res_dict, strict_num)

        print(f"最终严格长度{strict_num}, 拼接后片段数量: {len(res_dict)}")

        # Final transformation and saving
        self_improve_dict = self_reconstruct(res_dict)
        final_dict = transfromDict(self_improve_dict, transDict)
        save_to_csv(final_dict, f'{prefix}_reconstruct_column_{
                    column}.csv', 'output')

        print(f"结束对第{column}列的处理")

    reconstruct_csv(f'{prefix}_original_column_', range(
        5), f'{prefix}_original_column.csv', 'output')

    reconstruct_csv(f'{prefix}_reconstruct_column_', range(
        5), f'{prefix}_reconstruct_column.csv', 'output')


# Main execution
# extract_to_log()
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

feature_list = [
    "FG Pic1 - startingMode - Mode 2",
    "FG Pic2 - startingMode - Mode 2",
    "FG Pic3 - startingMode - Mode 2",
    "FG Pic4 - startingMode - Mode 2"
]

transDict = {
    "0": "1101", "10": "1201",
    "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005",
    "6": "1006", "7": "1007", "8": "1008", "9": "1009",
    # icon need to be replaced
    "11": "1401", "12": "1401", "13": "1401", "14": "1401", "15": "1401",
}

print("\n------开始对base_game的column进行处理...------\n")
process_columns(base_feature_list, 'base', transDict)
print("\n------结束对base_game的column进行处理------\n")

# Free game random processing
print("\n------开始对free_game的random进行处理...------\n")
res_random = get_free_seleted_frequency("slot_log.json")
save_to_csv(res_random, 'free_game_random.csv', 'output')
print("\n------结束对free_game的random进行处理------\n")

# Base game random processing
print("\n------开始对free_game的random进行处理...------\n")
res_random_b = get_base_seleted_frequency("slot_log.json")
save_to_csv(res_random_b, 'base_game_random.csv', 'output')
print("\n------结束对free_game的random进行处理------\n")

# Free game column processing
print(f"\n------开始对free_game的column FG pic进行处理...------\n")
process_columns(feature_list, 'free', transDict)
print(f"\n------结束对pic的column进行处理------\n")
