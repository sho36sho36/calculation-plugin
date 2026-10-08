PLUGIN_NAME = "累乗階乗"
PLUGIN_DESCRIPTION = "n↑↑n の累乗塔を計算します。"


def calculate(value):
    n = int(value)

    if n < 1:
        raise ValueError("1以上の整数を指定してください。")

    if n > 5:
        raise ValueError("大きすぎるため、5以下にしてください。")

    result = 1

    for _ in range(n):
        result = n ** result

    return result