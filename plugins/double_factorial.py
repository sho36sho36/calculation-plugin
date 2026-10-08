import math

PLUGIN_NAME = "二重階乗"


def calculate(value):
    n = int(value)

    if n < 0:
        raise ValueError("負の数には対応していません。")

    if n == 0 or n == 1:
        return 1

    # 偶数二重階乗
    #
    # n!! = 2^(n/2) × (n/2)!
    if n % 2 == 0:
        k = n // 2
        return (2 ** k) * math.factorial(k)

    # 奇数二重階乗
    #
    # n!! = n! / (2^k × k!)
    k = (n - 1) // 2

    return math.factorial(n) // (
        (2 ** k) * math.factorial(k)
    )