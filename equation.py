import sympy as sp
"""
- 本代码【需填写】间接测量量与直接测量量的函数关系
- 初始格式见：equation - 副本.py
"""
# LI Kele 2024/5/2 in Guangzhou


def func(data: tuple) -> float:
    """
    计算间接测量量与直接测量量的关系。
    例如，元组(6.66, 2.33, x1, x2, x3)中前段储存变化的直接测量量，后段储存独立的直接测量量。
    """
    (n, theta, t) = data
    theta_radians = sp.rad(theta)
    wavelength = 632.8e-9
    speed = 1e-3 * t
    numerator = speed * (sp.sin(theta_radians) ** 2)
    denominator = (2 * speed * (1 - sp.cos(theta_radians)) - n * wavelength)
    term = 1 - sp.cos(theta_radians) - (n * wavelength) / (2 * speed)
    result = numerator / denominator
    result += term * 0.5
    return result.evalf()
