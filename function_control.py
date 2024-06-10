import sys
from function_both import read_excel_data, check_tp
from function_direct import sa_direct_cal, sb_direct_cal, s_cal, v_direct_cal
from function_indirect import aver_indirect, sa_indirect_cal, sb_indirect_cal, delta_n, v_indirect_cal
"""
- 本文件包含功能如下：
- direct_show() -> 打印直接测量量信息面板
- direct() -> 打印直接测量量输入面板
- indirect_show() -> 打印间接测量量信息面板
- menu() -> 打印菜单界面
"""
# LI Kele 2024/5/3 in Guangzhou


def direct_show(data: list, index_all, delta_x, b_type_x) -> None:
    """
    打印直接测量量信息面板
    :param data: 当前转存的数据
    :param index_all: 当前对应的index
    :param delta_x: 当前对应的仪器最小分度值
    :param b_type_x: 当前对应的测量仪器误差分布类型
    :return: 无返回值
    """
    print(f'-----------------------直接测量量{index_all + 1}信息------------------------')
    print(f'实验数据个数为：{len(data)}')
    print(f'实验数据平均值为：{sum(data) / len(data)}')
    print(f'A类标准不确定度为：{sa_direct_cal(data)}')
    print(f'B类标准不确定度为：{sb_direct_cal(delta_x, b_type_x)}')
    print(f'合成标准不确定度为：{s_cal(sa_direct_cal(data), sb_direct_cal(delta_x, b_type_x))}')
    print(f'①当不考虑自由度时(p=0.95)，置信系数为1.96')
    delta_ans = 1.96 * s_cal(sa_direct_cal(data), sb_direct_cal(delta_x, b_type_x))
    print(f'对应的扩展不确定度为：{delta_ans}')
    print(f'测量结果记为： {sum(data) / len(data)} ± {delta_ans} ')
    v = v_direct_cal(data, sa_direct_cal(data), sb_direct_cal(delta_x, b_type_x))[0]
    print(f'②当考虑自由度时(p=0.95)，有效自由度为：{v}')
    print(f'保守取值{int(v)}，置信系数为{check_tp(int(v))}')
    tp = check_tp(int(v))
    delta_n2 = tp * s_cal(sa_direct_cal(data), sb_direct_cal(delta_x, b_type_x))
    print(f'对应的扩展不确定度为：{delta_n2}')
    print(f'测量结果记为： {sum(data) / len(data)} ± {delta_n2} ')
    return None


def direct(data_cor: list, data_un: list, delta: list, index_all: int, func, b_type: list = 4) -> None:
    """
    打印直接测量量输入面板
    :param data_cor: main.py 中的data_cor储存列表
    :param data_un: main.py 中的data_un储存列表
    :param delta: main.py 中的delta储存列表
    :param b_type: main.py 中的b_type储存列表
    :param func: main.py 中导入的func函数
    :param index_all: main.py 中的index储存列表
    :return: 无返回值
    """
    print(f'-----------------------输入直接测量量{index_all + 1}------------------------')
    de = float(input('请输入测量仪器的最小分度值：'))
    delta.append('Placeholder')
    delta[index_all] = de
    print('[1] 测量仪器的误差满足【均匀分布】')
    print('[2] 测量仪器的误差满足【三角分布】')
    print('[3] 测量仪器的误差满足【正态分布】')
    print('[4] 测量仪器的误差分布【无法获知】')
    b_type_input = int(input('请在此输入对应标号'))
    if b_type_input not in [1, 2, 3, 4]:
        print('//////////////////////ERROR! 输入错误！//////////////////////')
        direct(data_cor, data_un, delta, index_all, func, b_type)
    else:
        b_type.append('Placeholder')
        b_type[index_all] = b_type_input
    print('[1] 直接测量量独立')
    print('[2] 直接测量量非独立')
    print('注：按照 func 函数中顺序输入')
    input_type = int(input('请在此输入对应标号：'))
    if input_type == 1:
        print('[1] 手动输入数据')
        print('[2] 导入Excel文件')
        input_type2 = int(input('请在此输入对应标号：'))
        if input_type2 == 1:
            data_input = None
            index = 1
            data: list[str | float] = []
            while data_input != '结束':
                data_input = input(f'请输入第{index}个数据（输入‘结束’结束循环）：')
                data.append(data_input)
                index += 1
            del data[-1]
            for index1 in range(len(data)):
                data[index1] = float(data[index1])
            data_un.append(data)
            direct_show(data, index_all, delta[index_all], b_type[index_all])
            index_all += 1
            menu(data_cor, data_un, delta, index_all, b_type)
        elif input_type2 == 2:
            io = str(input('请输入Excel文件的储存路径：'))
            header = str(input('请输入对应数据的标头：')).strip()
            data_un.append(read_excel_data(io, header))
            direct_show(read_excel_data(io, header), index_all, delta[index_all], b_type[index_all])
            index_all += 1
            menu(data_cor, data_un, delta, index_all, func, b_type)
        else:
            print('//////////////////////ERROR! 输入错误！//////////////////////')
            direct(data_cor, data_un, delta, index_all, func, b_type)
    elif input_type == 2:
        print('[1] 手动输入数据')
        print('[2] 导入Excel文件')
        input_type2 = int(input('请在此输入对应标号：'))
        if input_type2 == 1:
            data_input = None
            index = 1
            data: list[str | float] = []
            while data_input != '结束':
                data_input = input(f'请输入第{index}个数据（输入‘结束’结束循环）：')
                data.append(data_input)
                index += 1
            del data[-1]
            for index1 in range(len(data)):
                data[index1] = float(data[index1])
            data_cor.append(data)
            index_all += 1
            menu(data_cor, data_un, delta, index_all, func, b_type)
        elif input_type2 == 2:
            io = str(input('请输入Excel文件的储存路径：'))
            header = str(input('请输入对应数据的标头：')).strip()
            data_cor.append(read_excel_data(io, header))
            index_all += 1
            menu(data_cor, data_un, delta, index_all, func, b_type)
        else:
            print('//////////////////////ERROR! 输入错误！//////////////////////')
            direct(data_cor, data_un, delta, index_all, func, b_type)
    else:
        print('//////////////////////ERROR! 输入错误！//////////////////////')
        direct(data_cor, data_un, delta, index_all, func, b_type)
    return None


def indirect_show(data_cor: list, data_un: list, delta: list, func, b_type: list) -> None:
    """
    打印间接测量量信息面板
    :param data_cor: main.py 中的data_cor储存列表
    :param data_un: main.py 中的data_un储存列表
    :param delta: main.py 中的delta储存列表
    :param b_type: main.py 中的b_type储存列表
    :param func: main.py 中导入的func函数
    :return: 无返回值
    """
    print(f'-----------------------间接测量量信息-------------------------')
    ave = aver_indirect(data_cor, data_un, func)
    print(f'实验数据平均值为：{ave}')
    sa = sa_indirect_cal(data_cor, data_un, func)
    print(f'A类标准不确定度为：{sa}')
    sb = sb_indirect_cal(data_cor, data_un, func, delta, b_type)
    print(f'B类标准不确定度为：{sb}')
    s = s_cal(sa, sb)
    print(f'合成标准不确定度为：{s}')
    print(f'①当不考虑自由度时(p=0.95)，置信系数为1.96')
    v = v_indirect_cal(data_cor, data_un, func, delta, b_type)[0]
    delta_ans = delta_n(v, s)[0]
    print(f'对应的扩展不确定度为：{delta_ans}')
    print(f'测量结果记为： {ave} ± {delta_ans} ')
    print(f'②当考虑自由度时(p=0.95)，有效自由度为：{v}')
    print(f'保守取值{int(v)}，置信系数为{check_tp(int(v))}')
    delta_n2 = delta_n(v, s_cal(sa, sb))[1]
    print(f'对应的扩展不确定度为：{delta_n2}')
    print(f'测量结果记为： {ave} ± {delta_n2} ')
    print('-------------------------计算器运行结束------------------------')
    sys.exit(0)


def menu(data_cor: list, data_un: list, delta: list, index_all: int, func, b_type: list = 4) -> None:
    """
    打印菜单界面
    :param data_cor: main.py 中的data_cor储存列表
    :param data_un: main.py 中的data_un储存列表
    :param delta: main.py 中的delta储存列表
    :param b_type: main.py 中的b_type储存列表
    :param func: main.py 中导入的func函数
    :param index_all: main.py 中的index储存列表
    :return: 无返回值
    """
    print('------------------------输入直接测量量------------------------')
    print('注：请对照 equation.py 中 func 函数参数顺序依次选择，并自行统一单位')
    print(f'[1] 输入直接测量量{index_all + 1}')
    print('[2] 输入完成')
    data_type = int(input('请在此输入对应标号：'))
    if data_type == 1:
        direct(data_cor, data_un, delta, index_all, func, b_type)
    elif data_type == 2:
        indirect_show(data_cor, data_un, delta, func, b_type)
    else:
        print('//////////////////////ERROR! 输入错误！//////////////////////')
        menu(data_cor, data_un, delta, index_all, func, b_type)
    return None
