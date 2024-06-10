from function_both import *
from sympy import diff, symbols
from function_direct import sa_direct_cal, sb_direct_cal, v_direct_cal
"""
- 本文件包含的功能如下：
- data_tuple() --> 将数据打包为元组
- aver_indirect() --> 计算间接测量量的平均值
- sa_indirect_cal() --> 计算间接测量量的A类不确定度
- sb_indirect_cal() --> 计算间接测量量的B类不确定度
- v_indirect_cal() --> 计算间接测量量有效自由度
"""
# LI Kele 2024/5/2 in Guangzhou


def data_tuple(data_cor: list[list], data_un: list[list]) -> tuple:
    """
    将数据打包为6个元素构成的元组
    :param data_cor: 嵌套列表，【变化】的不同直接测量量
    :param data_un: 嵌套列表，【独立】的不同直接测量量
    :return: 元组(data_cor, data_un, data_list, cor_len, cor_num, un_num)
    """
    data_list = []  # 【变化】测量量在前，【独立】测量量在后
    cor_len = 0
    cor_num = len(data_cor)
    un_num = len(data_un)
    if data_cor:
        for index in range(len(data_cor)):
            (a, b, c, d) = data_info(data_cor[index])
            data_list.append(d)
        cor_len = len(data_cor[0])
    if data_un:
        for index in range(len(data_un)):
            (a, b, c, d) = data_info(data_un[index])
            data_list.append(d)
    data_combin = tuple(data_list)
    return data_cor, data_un, data_combin, cor_len, cor_num, un_num


def aver_indirect(data_cor: list[list], data_un: list[list], func) -> float:
    """
    计算间接测量量的平均值
    注：data_cor 以及 data_un 为先后顺序，合在一起为 func 函数规定的元组顺序
    :param data_cor: 嵌套列表，【变化】的不同直接测量量
    :param data_un: 嵌套列表，【独立】的不同直接测量量
    :param func:间接测量量与直接测量量的函数关系，参数为元组
    :return: 间接测量量的平均值
    """
    data_cor, data_un, data_combin, cor_len, cor_num, un_num = data_tuple(data_cor, data_un)
    ave = None
    if cor_num:
        data_sum = 0.0
        for element in range(cor_len):
            data_cal = []
            for index in range(cor_num):
                data_cal.append(data_combin[index][element])
            if un_num:
                for index in range(un_num):
                    index += cor_num
                    (a, b, c, d) = data_info(data_combin[index])
                    data_cal.append(b)
            data_cal = tuple(data_cal)
            data_sum += func(data_cal)
            ave = data_sum / cor_len
    else:
        if un_num:
            data_cal = []
            for index in range(un_num):
                (a, b, c, d) = data_info(data_combin[index])
                data_cal.append(b)
            data_cal = tuple(data_cal)
            ave = func(data_cal)
    return ave


def sa_indirect_cal(data_cor: list[list], data_un: list[list], func) -> float:
    """
    计算间接测量量的A类不确定度
    :param data_cor: 嵌套列表，【变化】的不同直接测量量
    :param data_un: 嵌套列表，【独立】的不同直接测量量
    :param func: 间接测量量与直接测量量的函数关系，参数为元组
    :return: 间接测量量的A类不确定度
    """
    data_cor, data_un, data_combin, cor_len, cor_num, un_num = data_tuple(data_cor, data_un)
    string = 'x1:' + str(un_num + 1)
    variables = symbols(string)
    if cor_num:
        sa_list = []
        for index in range(cor_len):
            tuple_cal = []
            for index2 in range(cor_num):
                tuple_cal.append(data_cor[index2][index])
            subs_dict = dict()
            for index3 in range(len(variables)):
                tuple_cal.append(variables[index3])
                (a, b, c, d) = data_info(data_un[index3])
                subs_dict[variables[index3]] = b
            tuple_cal = tuple(tuple_cal)
            data_sum = 0.0
            for index4 in range(un_num):
                ans = diff(func(tuple_cal), variables[index4]).subs(subs_dict)
                ans *= sa_direct_cal(data_un[index4])
                ans = ans ** 2
                data_sum += ans
            sa = data_sum  # sa 是 xi 对应的 sa 值
            sa_list.append(sa)
        sa_indirect = (sum(sa_list) ** 0.5) / len(sa_list)
    else:
        subs_dict = dict()
        tuple_cal = []
        for index in range(len(variables)):
            tuple_cal.append(variables[index])
            (a, b, c, d) = data_info(data_un[index])
            subs_dict[variables[index]] = b
        tuple_cal = tuple(tuple_cal)
        data_sum = 0.0
        for index in range(un_num):
            ans = diff(func(tuple_cal), variables[index]).subs(subs_dict)
            ans *= sa_direct_cal(data_un[index])
            data_sum += ans ** 2
        sa_indirect = data_sum ** 0.5
    return sa_indirect


def sb_indirect_cal(data_cor: list[list], data_un: list[list], func, delta: list, b_type: list) -> float:
    """
    计算间接测量量的B类不确定度
    :param data_cor: 嵌套列表，【变化】的不同直接测量量
    :param data_un: 嵌套列表，【独立】的不同直接测量量
    :param func: 间接测量量与直接测量量的函数关系，参数为元组
    :param delta: 测量仪器的最小分度值按顺序构成的列表
    :param b_type: 测量仪器误差分布类型构成的列表
    :return:间接测量量的B类不确定度
    """
    data_cor, data_un, data_combin, cor_len, cor_num, un_num = data_tuple(data_cor, data_un)
    num = un_num + cor_num
    string = 'x1:' + str(num + 1)
    variables = symbols(string)
    if cor_num:
        sb_list = []
        for index in range(cor_len):
            tuple_cal = []
            subs_dict = dict()
            for index2 in range(len(variables)):
                tuple_cal.append(variables[index2])
            for index3 in range(cor_num):
                subs_dict[variables[index3]] = data_cor[index3][index]
            for index4 in range(un_num):
                (a, b, c, d) = data_info(data_un[index4])
                subs_dict[variables[cor_num + index4]] = b
            tuple_cal = tuple(tuple_cal)
            data_sum = 0.0
            for index5 in range(num):
                ans = diff(func(tuple_cal), variables[index5])
                ans = ans.subs(subs_dict).evalf()
                ans *= sb_direct_cal(delta[index5], b_type[index5])
                data_sum += (ans ** 2)
            sb = data_sum
            sb_list.append(sb)
        sb_indirect = (sum(sb_list) ** 0.5) / len(sb_list)
    else:
        subs_dict = dict()
        tuple_cal = []
        for index in range(len(variables)):
            tuple_cal.append(variables[index])
            (a, b, c, d) = data_info(data_un[index])
            subs_dict[variables[index]] = b
        tuple_cal = tuple(tuple_cal)
        data_sum = 0.0
        for index in range(un_num):
            ans = diff(func(tuple_cal), variables[index])
            ans = ans.subs(subs_dict).evalf()
            ans *= sb_direct_cal(delta[index], b_type[index])
            data_sum += (ans ** 2)
        sb_indirect = data_sum ** 0.5
    return sb_indirect


def v_indirect_cal(data_cor: list[list], data_un: list[list], func, delta: list, b_type: list) -> tuple:
    """
    计算间接测量量有效自由度
    :param data_cor:嵌套列表，【变化】的不同直接测量量
    :param data_un:嵌套列表，【独立】的不同直接测量量
    :param func:间接测量量与直接测量量的函数关系，参数为元组
    :param delta:测量仪器的最小分度值按顺序构成的列表
    :param b_type:测量仪器误差分布类型构成的列表
    :return:元组（v_indirect, va_indirect, vb_indirect）
    """
    # 先计算A类不确定度分量的自由度
    data_cor, data_un, data_combin, cor_len, cor_num, un_num = data_tuple(data_cor, data_un)
    num = un_num + cor_num
    string = 'x1:' + str(num + 1)
    variables = symbols(string)
    if cor_num:
        va_list = []
        sa_list = []
        for index in range(cor_len):
            tuple_cal = []
            subs_dict = dict()
            for index2 in range(len(variables)):
                tuple_cal.append(variables[index2])
            for index3 in range(cor_num):
                subs_dict[variables[index3]] = data_cor[index3][index]
            for index4 in range(un_num):
                (a, b, c, d) = data_info(data_un[index4])
                subs_dict[variables[cor_num + index4]] = b
            tuple_cal = tuple(tuple_cal)
            data_sum = 0.0
            data_sum2 = 0.0
            for index5 in range(num):
                ans = diff(func(tuple_cal), variables[index5])
                ans = ans.subs(subs_dict).evalf()
                if index5 < cor_num:
                    sa = 0.0
                else:
                    sa = sa_direct_cal(data_combin[index5])
                ans *= sa
                ans2 = ans
                ans2 = ans2 ** 2
                sb = sb_direct_cal(delta[index5], b_type[index5])
                (v, v1, v2) = v_direct_cal(data_combin[index5], sa, sb)
                data_sum += (ans ** 4) / v1
                data_sum2 += ans2
            sa = data_sum2 ** 0.5
            sa_list.append(sa)
            va = (sa_indirect_cal(data_cor, data_un, func) ** 4) / data_sum
            va_list.append(va)
        temp_sum = 0.0
        for element in range(len(sa_list)):
            temp = sa_list[element] / len(sa_list)
            temp = temp ** 4
            temp = temp / va_list[element]
            temp_sum += temp
        va_indirect = sa_indirect_cal(data_cor, data_un, func) / temp_sum
    else:
        subs_dict = dict()
        tuple_cal = []
        for index in range(len(variables)):
            tuple_cal.append(variables[index])
            (a, b, c, d) = data_info(data_un[index])
            subs_dict[variables[index]] = b
        tuple_cal = tuple(tuple_cal)
        data_sum = 0.0
        for index in range(un_num):
            ans = diff(func(tuple_cal), variables[index])
            ans = ans.subs(subs_dict).evalf()
            sa = sa_direct_cal(data_un[index])
            ans *= sa
            sb = sb_direct_cal(delta[index], b_type[index])
            (v, v1, v2) = v_direct_cal(data_un[index], sa, sb)
            data_sum += (ans ** 4) / v1
        va_indirect = (sa_indirect_cal(data_cor, data_un, func) ** 4) / data_sum

    # 再计算B类不确定度分量的自由度
    data_cor, data_un, data_combin, cor_len, cor_num, un_num = data_tuple(data_cor, data_un)
    num = un_num + cor_num
    string = 'x1:' + str(num + 1)
    variables = symbols(string)
    if cor_num:
        vb_list = []
        sb_list = []
        for index in range(cor_len):
            tuple_cal = []
            subs_dict = dict()
            for index2 in range(len(variables)):
                tuple_cal.append(variables[index2])
            for index3 in range(cor_num):
                subs_dict[variables[index3]] = data_cor[index3][index]
            for index4 in range(un_num):
                (a, b, c, d) = data_info(data_un[index4])
                subs_dict[variables[cor_num + index4]] = b
            tuple_cal = tuple(tuple_cal)
            data_sum = 0.0
            data_sum2 = 0.0
            for index5 in range(num):
                ans = diff(func(tuple_cal), variables[index5])
                ans = ans.subs(subs_dict).evalf()
                ans *= sb_direct_cal(delta[index5], b_type[index5])
                ans2 = ans ** 2
                if index5 < cor_num:
                    sa = 0.0
                else:
                    sa = sa_direct_cal(data_combin[index5])
                sb = sb_direct_cal(delta[index5], b_type[index5])
                (v, v1, v2) = v_direct_cal(data_combin[index5], sa, sb)
                data_sum += (ans ** 4) / v2
                data_sum2 += ans2
            sb = data_sum2 ** 0.5
            vb = (sb_indirect_cal(data_cor, data_un, func, delta, b_type) ** 4) / data_sum
            vb_list.append(vb)
            sb_list.append(sb)
        temp_sum = 0.0
        for element in range(len(sb_list)):
            temp = sb_list[element] / len(sb_list)
            temp = temp ** 4
            temp = temp / vb_list[element]
            temp_sum += temp
        vb_indirect = sb_indirect_cal(data_cor, data_un, func, delta, b_type) / temp_sum
    else:
        subs_dict = dict()
        tuple_cal = []
        for index in range(len(variables)):
            tuple_cal.append(variables[index])
            (a, b, c, d) = data_info(data_un[index])
            subs_dict[variables[index]] = b
        tuple_cal = tuple(tuple_cal)
        data_sum = 0.0
        for index in range(un_num):
            ans = diff(func(tuple_cal), variables[index])
            ans = ans.subs(subs_dict).evalf()
            ans *= sb_direct_cal(delta[index], b_type[index])
            sa = sa_direct_cal(data_un[index])
            sb = sb_direct_cal(delta[index], b_type[index])
            (v, v1, v2) = v_direct_cal(data_un[index], sa, sb)
            data_sum += (ans ** 4) / v2
        vb_indirect = (sb_indirect_cal(data_cor, data_un, func, delta, b_type) ** 4) / data_sum

    # 最后计算有效自由度
    sa_indirect = sa_indirect_cal(data_cor, data_un, func)
    sb_indirect = sb_indirect_cal(data_cor, data_un, func, delta, b_type)
    s = s_cal(sa_indirect, sb_indirect)
    v_indirect = (s ** 4) / (((sa_indirect ** 4) / va_indirect) + ((sb_indirect ** 4) / vb_indirect))
    return v_indirect, va_indirect, vb_indirect
