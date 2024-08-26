import pandas as pd
import os
from openpyxl import Workbook


def xlsx2excel(xlsx_path):
    # 判断文件是否存在
    if not os.path.exists(xlsx_path):
        print('文件不存在')
        return

    # 读取 XLSX 文件
    df = pd.read_excel(xlsx_path, index_col=None)

    # 获取 XLSX 所在的目录
    xlsx_dir = os.path.abspath(os.path.dirname(xlsx_path))

    # 创建 Excel 工作簿
    excel_path = os.path.join(xlsx_dir, 'output.xlsx')
    workbook = Workbook()

    # 按照第一列的值分别创建工作表
    for name, group in df.groupby(df.columns[0]):
        worksheet = workbook.create_sheet(str(name))
        for i, row in group.iterrows():
            worksheet.append(row.tolist())
        print(f'Sheet: {name} 已保存')

    # 删除默认的 'Sheet' 工作表
    del workbook['Sheet']

    # 保存 Excel 文件
    workbook.save(excel_path)
    print('转换完成')


xlsx2excel('test.xlsx')
