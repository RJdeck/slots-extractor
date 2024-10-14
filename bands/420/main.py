from extract import extract_to_log
from preprocess import (
    feature_inspector, get_frequency, read_column, save_to_csv,
    reconstruct_csv, get_free_seleted_frequency, transfromDict
)
from reconstruct import reconstruct_chip_unique_off, self_reconstruct


def process_columns(features, prefix, transDict, offset=0):
    for column in range(5):
        print(f"开始对第{column}列的处理")

        # Read and process column data
        column_data = read_column("slot_log.json", features, column)
        frequency_dict = get_frequency(column_data, None, offset)
        print(f"原数据片段数量: {len(frequency_dict)}")

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

    reconstruct_csv(f'{prefix}_reconstruct_column_', range(
        5), f'{prefix}_reconstruct_column.csv', 'output')


# Main execution
extract_to_log()

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

transDict = {
    "0": "1101", "10": "1201",
    "1": "1001", "2": "1002", "3": "1003", "4": "1004", "5": "1005",
    "6": "1006", "7": "1007", "8": "1008", "9": "1009"
}

print("\n------开始对base_game的column进行处理...------\n")
process_columns(base_feature_list, 'base', transDict)
print("\n------结束对base_game的column进行处理------\n")

# Free game random processing
print("\n------开始对free_game的random进行处理...------\n")
res_random = get_free_seleted_frequency("slot_log.json")
save_to_csv(res_random, 'free_game_random.csv', 'output')
print("\n------结束对free_game的random进行处理------\n")

# Free game column processing
for pic in range(1, 5):
    print(f"\n------开始对free_game的column FG pic{pic}进行处理...------\n")
    feature_list = [f"FG Pic{pic} - startingMode - Mode 2"]
    process_columns(feature_list, f'pic{pic}', transDict)
    print(f"\n------结束对pic{pic}的column进行处理------\n")
