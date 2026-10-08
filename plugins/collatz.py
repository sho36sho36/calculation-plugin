PLUGIN_NAME = "コラッツ予想"
PLUGIN_DESCRIPTION = "数が1になるまでのコラッツ操作を計算します。"


def calculate(value):
    n = int(value)

    if n < 1:
        raise ValueError("1以上の整数を指定してください。")

    sequence = [n]

    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1

        sequence.append(n)

    steps = len(sequence) - 1

    return " → ".join(map(str, sequence)) + f"\n\nステップ数: {steps}"