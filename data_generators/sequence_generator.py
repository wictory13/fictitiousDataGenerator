import random
import string


def generate_alphanum_str(length=0):
    length = length or random.randint(1, 20)
    all_symbols = string.ascii_letters + string.digits
    return ''.join(random.choice(all_symbols) for _ in range(length))


def generate_int(start=0, end=1000):
    return random.randint(min(start, end), max(start, end))


def generate_float(start=0, end=1000, number_after_dot=12):
    return round(
        random.uniform(min(start, end), max(start, end)),
        number_after_dot)
