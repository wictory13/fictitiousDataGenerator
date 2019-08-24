from datetime import datetime, timedelta
import random


def calculate_age(birth_date):
    date = datetime.strptime(birth_date, '%d.%m.%Y')
    return int((datetime.today() - date).days/365.2425)


def generate_birth_date():
    end = datetime.today()
    start = end - timedelta(100*365.2425)
    delta = end - start
    random_days = random.randrange(delta.days)
    date = start + timedelta(days=random_days)
    return datetime.strftime(date, '%d.%m.%Y')
