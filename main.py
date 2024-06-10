from function_control import menu
from equation import func
"""
- 本文件为运行文件
"""
# LI Kele 2024/5/3 in Guangzhou

delta = []
b_type = []
data_cor = []
data_un = []
index_all = 0
print('----------------------实验不确定度计算器----------------------')
menu(data_cor, data_un, delta, index_all, func, b_type)
