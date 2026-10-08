PLUGIN_NAME = "素数階乗"
PLUGIN_DESCRIPTION = "2からnまでの素数をすべて掛け合わせます。"


def calculate(value):
    n = int(value)

    if n < 2:
        raise ValueError("2以上の整数を指定してください。")

    result = 1

    for number in range(2, n + 1):
        is_prime = True

        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

        if is_prime:
            result *= number

    return result