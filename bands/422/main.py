# %% -------------------------------------------- data_extract --------------------------------------------
from extract import extract_to_log
from preprocess import read_column


# 读取原始数据
extract_to_log(save_file_name='slot_log.json', endswith='000.har')
column_data = read_column("slot_log.json", 5)
print(column_data)