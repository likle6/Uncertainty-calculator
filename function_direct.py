from function_both import *
"""
- 本文件包含的功能如下：
- sa_direct_cal() --> 计算直接测量量的A类标准不确定度
- sb_direct_cal() --> 计算直接测量量的B类标准不确定度
- v_direct_cal() --> 计算直接测量量有效自由度
"""
# LI Kele 2024/5/1 in Guangzhou


def sa_direct_cal(data: list) -> float:
    """
    计算直接测量量的A类标准不确定度
    :param data: 直接测量量的数据(list)
    :return: 对应的A类不确定度
    """
    # ①当len(data) == 1时，结果为0
    # ②当data中数据完全一样时，结果为0
    if len(set(data)) <= 1:
        ans = 0.0
    # ③当data中数据不完全一样且len(data) != 1时，完成以下计算
    else:
        (a, b, c, d) = data_info(data)
        terms = 0.0
        for element in d:
            term = element - b
            terms += term ** 2
        ans = (terms / (c * (c - 1))) ** 0.5
    return ans


def sb_direct_cal(delta: float, b_type: Union[str, int] = 4) -> float:
    """
    计算直接测量量的B类标准不确定度,默认无法获知误差分布
    :param delta: 测量仪器的最小分度值
    :param b_type: 测量仪器误差分布类型
    :return: 对应的B类不确定度
    """

    """
    在该函数中：
    1.测量仪器的误差满足【均匀分布】
    2.测量仪器的误差满足【三角分布】
    3.测量仪器的误差满足【正态分布】
    4.测量仪器的误差分布【无法获知】
    """

    b_type = int(b_type)
    if b_type == 1 or b_type == 4:
        ans = delta / (3 ** 0.5)
    elif b_type == 2:
        ans = delta / 2
    elif b_type == 3:
        ans = delta / (6 ** 0.5)
    else:
        print('Error! Not recognized in sb_direct_cal()!')
        return 0.0
    return ans


def v_direct_cal(data: list, sa: float, sb: float) -> tuple:
    """
    计算有效自由度
    :param data: 直接测量量的数据(list)
    :param sa: A类标准不确定度
    :param sb: B类标准不确定度
    :return: 元组(有效自由度, A类自由度, B类自由度)
    """
    (a, b, c, d) = data_info(data)
    if len(set(d)) <= 1:
        if len(d) == 1:
            v_a = float(1)
        else:
            v_a = float(len(d) - 1)
    else:
        v_a = float(len(d) - 1)
    v_b = float(1)
    v = (s_cal(sa, sb) ** 4) / (((sa ** 4) / v_a) + ((sb ** 4) / v_b))
    return v, v_a, v_b
