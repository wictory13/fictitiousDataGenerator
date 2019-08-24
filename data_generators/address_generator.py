import random


def generate_address(cities, streets):
    city = random.choice(cities)
    street = random.choice(streets)
    house = random.randint(1, 300)
    flat = random.randint(1, 216)
    return '{}, {},{} - кв.{}'.format(city, street, house, flat)
