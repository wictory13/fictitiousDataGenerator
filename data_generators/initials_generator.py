import random
from copy import deepcopy


class Weighted:
    def __init__(self, names):
        self.frequency_names = {}
        max_frequency = max(list(names.values()))
        for name in names:
            frequency = names[name]/max_frequency
            if frequency not in list(self.frequency_names.keys()):
                self.frequency_names[frequency] = []
            self.frequency_names[frequency].append(name)

    def __call__(self):
        random_number = random.random()
        choose_list = []
        for frequency in self.frequency_names:
            if frequency >= random_number:
                choose_list.extend(self.frequency_names[frequency])
        return random.choice(choose_list)


def generate_name(weights, names):
    if weights:
        w = Weighted(names)
        return w()
    else:
        return random.choice(list(names.keys()))


def generate_initials(data, gender, weights):
    if gender == 'all':
        names = deepcopy(data['female_names'])
        names.update(data['male_names'])
        name = generate_name(weights, names)
    elif gender in ('f', 'female'):
        name = generate_name(weights, data['female_names'])
    else:
        name = generate_name(weights, data['male_names'])
    if name in data['female_names']:
        surname = random.choice(data['female_surname'])
        patronymic = random.choice(data['female_patronymic'])
    else:
        surname = random.choice(data['male_surname'])
        patronymic = random.choice(data['male_patronymic'])
    return '{} {} {}'.format(surname, name, patronymic)
