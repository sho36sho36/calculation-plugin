PLUGIN_NAME = "超階乗"


def calculate(value):
    n = int(value)

    if n < 1:
        raise ValueError("1以上の数を指定してください。")

    result = 1

    for i in range(1, n + 1):
        result *= i ** i

    return result