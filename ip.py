import ipinfo
import pandas as pd
import os
from openpyxl import Workbook


def file2excel(file_path, ip='ip'):
    # const BLACK_REGION  = [
    #     'WA',//Washington
    #     'NV',//Nevada
    #     'ID',//Idaho
    #     'FL',//Florida
    #     //            'HI',
    #     'GA',//Georgia
    #     'AL',//Alabama
    #     'KY',//Kentucky
    #     'MI',//Michigan
    #     'SC',//South Carolina
    #     'MN',//Minnesota
    #     //            'WV',
    #     'QC',//Quebec
    # ];
    black_region = ['Washington', 'Nevada', 'Idaho', 'Florida',
                    'Georgia', 'Alabama', 'Kentucky', 'Michigan',
                    'South Carolina', 'Minnesota', 'Quebec']

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
    if ip not in df.columns:
        print('分组列不存在')
        return

    # 初始化 ipinfo 的处理器
    handler = ipinfo.getHandler('e09838276e0339')

    # 定义一个函数，用于从 IP 地址获取城市信息
    def get_city(ip):
        try:
            details = handler.getDetails(ip)
            return details.region
        except Exception as e:
            print(f"无法查询 IP {ip}: {e}")
            return None

    # 创建一个新的列，存储城市信息
    df['region'] = df[ip].apply(get_city)
    df['is_black'] = df['region'].isin(black_region)

    # 保存结果到新的 Excel 文件
    output_file = 'output_with_region.xlsx'
    df.to_excel(output_file, index=False)
    print(f'处理完成，结果已保存到 "{output_file}"')


# 调用函数
file_path = '无标题.xlsx'  # 替换为你的文件路径
file2excel(file_path, ip='ip')  # 替换为你的 IP 列名
