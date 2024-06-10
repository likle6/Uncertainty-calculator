import sympy
"""
- 本代码【需填写】间接测量量与直接测量量的函数关系
"""
# LI Kele 2024/5/2 in Guangzhou


def func(data: tuple) -> float:
    (a, b, c) = data[0::]
    x = (a + b + c) * sympy.pi  # 在此修改函数关系，使得x代表间接测量量

    # 实现 func 函数后，删除下面的 raise 语句
    raise NotImplementedError("func 函数还未实现")
    return x.evalf()
