PLUGIN_NAME = "素数"


def calculate(value):
    count = int(value)

    if count < 1:
        raise ValueError("1以上の数を指定してください。")

    primes = []
    number = 2

    while len(primes) < count:
        is_prime = True

        for p in primes:
            if p * p > number:
                break
            if number % p == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(number)

        number += 1

    return ", ".join(map(str, primes))