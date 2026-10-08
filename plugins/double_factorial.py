PLUGIN_NAME = "二重階乗"
PLUGIN_DESCRIPTION = "n × (n-2) × (n-4) × … を計算します。"


def calculate(value):
    n = int(value)

    if n < 0:
        raise ValueError("負の数には対応していません。")

    result = 1

    while n > 0:
        result *= n
        n -= 2

    return result