import pandas as pd
import os
from openpyxl import Workbook


def file2excel(file_path, output_path="output.xlsx", group_by='App ID', sheet_name='App Name'):
    # 判断文件是否存在
    if not os.path.exists(file_path):
        print('文件不存在')
        return

    # 根据文件后缀名读取文件
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, index_col=None)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, index_col=None)
    else:
        print('不支持的文件格式')
        return

    # 判断是否存在指定列
    if group_by not in df.columns:
        print('分组列不存在')
        return
    if sheet_name not in df.columns:
        print('表名列不存在')
        return

    # 获取文件所在的目录
    file_dir = os.path.abspath(os.path.dirname(file_path))

    # 创建 Excel 工作簿
    excel_path = os.path.join(file_dir, output_path)
    workbook = Workbook()

    # 按照指定列分组
    for _, group in df.groupby(df.columns[df.columns.get_loc(group_by)]):
        # 获取分组名为group中列名为sheet_name的值
        package_name = group.iloc[0][sheet_name]

        # 创建工作表
        worksheet = workbook.create_sheet(str(package_name))
        # 添加表头
        worksheet.append(df.columns.tolist())

        # 添加数据
        for _, row in group.iterrows():
            worksheet.append(row.tolist())
        print(f'Sheet: {package_name} 已保存')

    # 删除默认的 'Sheet' 工作表
    del workbook['Sheet']

    # 保存 Excel 文件
    workbook.save(excel_path)
    print('转换完成')


file2excel('每月抽水.csv')
