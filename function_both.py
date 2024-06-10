from typing import Union
import pandas as pd
import math
"""
- 本文件包含的功能如下：
- check_tp() --> 查阅p=0.95时的置信系数tp
- read_excel_data() --> 读入excel数据，转化为列表
- data_info() --> 输入数据，输出基本信息
- s_cal() --> 计算合成标准不确定度
- delta_n() --> 计算扩展不确定度
"""
# LI Kele 2024/5/1 in Guangzhou


def check_tp(v0: Union[float, int]) -> float:
    """
    查阅p=0.95时的置信系数tp
    注：v0输入错误时，默认不考虑自由度
    :param v0: 有效自由度
    :return: 对应的置信系数tp
    """
    if int(v0) <= 0:
        tp = 1.96
    elif int(v0) == 1:
        tp = 12.71
    elif int(v0) == 2:
        tp = 4.30
    elif int(v0) == 3:
        tp = 3.18
    elif int(v0) == 4:
        tp = 2.78
    elif int(v0) == 5:
        tp = 2.57
    elif int(v0) == 6:
        tp = 2.45
    elif int(v0) == 7:
        tp = 2.36
    elif int(v0) == 8:
        tp = 2.31
    elif int(v0) == 9:
        tp = 2.26
    elif int(v0) == 10:
        tp = 2.23
    elif int(v0) == 11:
        tp = 2.20
    elif int(v0) == 12:
        tp = 2.18
    elif int(v0) == 13:
        tp = 2.16
    elif int(v0) == 14:
        tp = 2.14
    elif int(v0) < 20:
        tp = 2.13
    elif int(v0) < 25:
        tp = 2.09
    elif int(v0) < 30:
        tp = 2.06
    elif int(v0) < 40:
        tp = 2.04
    elif int(v0) < 50:
        tp = 2.02
    elif int(v0) < 60:
        tp = 2.01
    elif int(v0) < 80:
        tp = 2.00
    elif int(v0) < 100:
        tp = 1.99
    elif int(v0) == 100:
        tp = 1.98
    elif int(v0) > 100:
        tp = 1.96
    else:
        tp = 1.96
    return tp


def read_excel_data(io: str, header: str) -> list:
    """
    读入excel数据，转化为列表
    :param io: excel储存路径如：'新建 Microsoft Excel 工作表.xlsx'
    :param header: 所需数据标头：'标头'
    :return: 储存在列表中的数据
    """
    io = io.strip("'")
    io = io.strip('"')
    sheet = pd.read_excel(io)
    data = list(sheet[header])
    data = [0.0 if math.isnan(x) else x for x in data]
    num = data.count(0.0)
    while num > 0:
        data.remove(0.0)
        num -= 1
    for index in range(len(data)):
        if data[index] != 0.0:
            data[index] = float(data[index])
    return data


def data_info(data: list[Union[float, str]]) -> tuple:
    """
    输入数据，输出基本信息
    注：可以处理的data列表类型[1, 2, 3] ['1', '2', '3'] ['1,', '2,', '3,']
    :param data: 需要处理的数据
    :return: 元组（数据总和, 平均值, 数据个数, 标准数据列表）
    """
    data_sum = 0.0
    num = 0
    data_standard = []
    for f in range(len(data)):
        x = float(str(data[f]).strip(','))
        data_sum += x
        num += 1
        data_standard.append(x)
    data_aver = float(data_sum / num)
    return data_sum, data_aver, num, data_standard


def s_cal(sa: float, sb: float) -> float:
    """
    计算合成标准不确定度
    :param sa: A类标准不确定度
    :param sb: B类标准不确定度
    :return: 合成标准不确定度
    """
    s = ((sa ** 2) + (sb ** 2)) ** 0.5
    return s


def delta_n(v: float, s: float) -> tuple:
    """
    计算扩展不确定度
    :param v:有效自由度
    :param s:合成标准不确定度
    :return:扩展不确定度元组（不考虑自由度, 考虑自由度）
    """
    tp = check_tp(int(v))
    n1 = 1.96 * float(s)
    n2 = tp * s
    return n1, n2
