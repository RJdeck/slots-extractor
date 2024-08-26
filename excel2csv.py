import pandas as pd
import os


def excel2csv(excel_path):
    # 判断文件是否存在
    if not os.path.exists(excel_path):
        print('文件不存在')
        return
    # 读取excel文件
    sheet_names = pd.ExcelFile(excel_path, engine='openpyxl').sheet_names
    for sheet_name in sheet_names:
        # 读取每个sheet的数据
        sheet_data = pd.read_excel(excel_path, sheet_name, index_col=None)
        # 获取excel当前目录
        excel_dir = os.path.abspath(os.path.dirname(excel_path))
        # 转换并保存到excel所在的csv文件夹下
        csv_path = os.path.join(excel_dir, 'csv')
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
        sheet_data.to_csv(os.path.join(csv_path, sheet_name +
                          '.csv'), index=False, encoding='utf-8')
        print('sheet:', sheet_name, ' 转换成功')


excel2csv('bands/416/winner_416.xlsx')
