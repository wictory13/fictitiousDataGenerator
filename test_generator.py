from datetime import datetime, timedelta
from collections import defaultdict
from copy import deepcopy
from data_generators import *
import argparse
import generator


encoding = 'windows-1251'
json_data = generator.read_json_data('database.json', encoding)
data = generator.extract_all_data(json_data, encoding)


def check_distribution(names_list, frequency_names):
    test_frequencies = {}
    for name in names_list:
        for frequency in frequency_names.keys():
            if frequency not in test_frequencies.keys():
                test_frequencies[frequency] = []
            if name in frequency_names[frequency]:
                test_frequencies[frequency].append(name)
    assert len(test_frequencies[0.2]) <= len(
        test_frequencies[0.6]) <= len(test_frequencies[1])


class TestClass:
    def test_snils_control_number(self):
        assert jobs_data_generator.create_snils_control_number(
            '939440541') == 34
        assert jobs_data_generator.create_snils_control_number(
            '005995658') == 89
        assert jobs_data_generator.create_snils_control_number(
            '165708578') == 1
        assert jobs_data_generator.create_snils_control_number(
            '802861664') == 0
        assert jobs_data_generator.create_snils_control_number(
            '064713022') == 40

    def test_snils_length(self):
        assert len(jobs_data_generator.generate_snils()) == 14

    def test_generate_birth_date(self):
        birth_date = datetime.strptime(
            birth_date_data_generator.generate_birth_date(), '%d.%m.%Y')
        end = datetime.today()
        start = end - timedelta(100 * 365.2425)
        assert birth_date >= start <= end

    def test_generate_address(self):
        address = address_generator.generate_address(
            data['cities'], data['streets'])
        city = address.split(', ')[0]
        street = address.split(', ')[1].split(',')[0]
        house_number = int(address.split(', ')[1]
                           .split(',')[1].split(' - ')[0])
        flat_number = int(address.split('кв.')[1])
        assert city in data['cities']
        assert street in data['streets']
        assert house_number in range(1, 300)
        assert flat_number in range(1, 216)

    def test_generate_job_and_salary(self):
        job, salary = jobs_data_generator.generate_job_and_salary(
            data['jobs']).split(': ')
        jobs = list(data['jobs'].keys())
        start = int(data['jobs'][job][0])
        end = int(data['jobs'][job][1])
        salary = int(salary[:-2])
        assert job in jobs
        assert salary in range(start, end)

    def test_weighted(self):
        test_dict = {'a': 3, 'b': 4, 'c': 3}
        test = initials_generator.Weighted(test_dict)
        assert test.frequency_names == {0.75: ['a', 'c'], 1: ['b']}
        assert test() in test_dict.keys()

    def test_generate_initials_for_all(self):
        initials = initials_generator.generate_initials(
            data, 'all', False).split()
        assert initials[0] in data['female_surname'] or\
            initials[0] in data['male_surname']
        assert initials[1] in data['female_names'] or\
            initials[1] in data['male_names']
        assert initials[2] in data['female_patronymic'] or\
            initials[2] in data['male_patronymic']

    def test_generate_female_initials(self):
        initials = initials_generator.generate_initials(
            data, 'female', False).split()
        assert initials[0] in data['female_surname']
        assert initials[1] in data['female_names']
        assert initials[2] in data['female_patronymic']
        initials = initials_generator.generate_initials(
            data, 'f', False).split()
        assert initials[0] in data['female_surname']
        assert initials[1] in data['female_names']
        assert initials[2] in data['female_patronymic']

    def test_generate_male_initials(self):
        initials = initials_generator.generate_initials(
            data, 'male', False).split()
        assert initials[0] in data['male_surname']
        assert initials[1] in data['male_names']
        assert initials[2] in data['male_patronymic']
        initials = initials_generator.generate_initials(
            data, 'm', False).split()
        assert initials[0] in data['male_surname']
        assert initials[1] in data['male_names']
        assert initials[2] in data['male_patronymic']

    def test_female_names_distribution(self):
        test_names_list = [format_data_generator.generate_format_data(
            data, 'female', '{name}', True) for _ in range(1000)]
        frequency_names = initials_generator.Weighted(
            data['female_names']).frequency_names
        check_distribution(test_names_list, frequency_names)
        assert test_names_list.count('Анна') > test_names_list.count('Анжела')
        assert test_names_list.count('Алена') > test_names_list.count('Агата')

    def test_male_names_distribution(self):
        test_names_list = [format_data_generator.generate_format_data(
            data, 'male', '{name}', True) for _ in range(1000)]
        frequency_names = initials_generator.Weighted(
            data['male_names']).frequency_names
        check_distribution(test_names_list, frequency_names)
        assert test_names_list.count('Петр') > test_names_list.count('Юрий')
        assert test_names_list.count('Никита') > test_names_list.count('Эрик')

    def test_all_names_distribution(self):
        test_names_list = [format_data_generator.generate_format_data(
            data, 'all', '{name}', True) for _ in range(1000)]
        names = deepcopy(data['female_names'])
        names.update(data['male_names'])
        frequency_names = initials_generator.Weighted(names).frequency_names
        check_distribution(test_names_list, frequency_names)
        assert test_names_list.count('Мария') > test_names_list.count('Лев')
        assert test_names_list.count('Максим') > test_names_list.count('Ия')

    def test_generate_format_data_for_all(self):
        human_data = format_data_generator.generate_format_data(
            data, 'all', '{name} {age}', False).split()
        assert human_data[0] in data['female_names'] \
            or human_data[0] in data['male_names']
        assert int(human_data[1]) <= 100

    def test_generate_female_format_data(self):
        human_data = format_data_generator.generate_format_data(
            data, 'female', '{surname},{patronymic}', False).split(',')
        assert human_data[0] in data['female_surname']\
            and human_data[1] in data['female_patronymic']

    def test_generate_male_format_data(self):
        human_data = format_data_generator.generate_format_data(
            data, 'male', '{name} {patronymic} '
                          '{snils} {birth_date}', False).split()
        assert human_data[0] in data['male_names']\
            and human_data[1] in data['male_patronymic']
        assert len(human_data[2] + human_data[3]) == 13
        birth_date = datetime.strptime(human_data[4], '%d.%m.%Y')
        end = datetime.today()
        start = end - timedelta(100 * 365.2425)
        delta = (end - start).days/365.2425
        assert delta <= 100
        assert start <= birth_date <= end

    def test_generate_int(self):
        assert type(sequence_generator.generate_int()) is int
        assert 10 <= sequence_generator.generate_int(10, 15) <= 15
        assert -100 <= sequence_generator.generate_int(100, -100) <= 100
        assert sequence_generator.generate_int(1, 1) == 1

    def test_generate_float(self):
        assert type(sequence_generator.generate_float()) is float
        assert sequence_generator.generate_float(10.5, 10.6, 0) == 11.0
        assert -10 <= sequence_generator.generate_float(10, -10, 9) <= 10
        assert sequence_generator.generate_float(end=10) <= 10

    def test_alphanum_str(self):
        assert len(sequence_generator.generate_alphanum_str(10)) == 10

    def test_extract_jobs(self):
        jobs = generator.extract_jobs('jobs.csv', encoding)
        assert type(jobs) is defaultdict
        assert 'Программист' in list(jobs.keys())
        assert jobs['Портье'] == (17000, 37000)

    def test_extract_names(self):
        female_names = generator.extract_names('female_names.csv', encoding)
        assert type(female_names) is defaultdict
        assert 'Михаил' not in list(female_names.keys())
        assert 'Глафира' in list(female_names.keys())
        assert female_names['Дарья'] == 5
        assert female_names['Виктория'] == 4
        male_names = generator.extract_names('male_names.csv', encoding)
        assert 'Михаил' in list(male_names.keys())
        assert 'Глафира' not in list(male_names.keys())
        assert male_names['Александр'] == 5
        assert male_names['Ильнур'] == 3

    def test_extract_cities_data(self):
        test_data = {}
        generator.extract_data(test_data, 'cities.csv', 'cities', encoding)
        assert len(test_data['cities']) == 322
        assert 'Екатеринбург' in test_data['cities']

    def test_extract_data_error(self):
        test_data = {}
        try:
            generator.extract_data(test_data, 'README.md', 'cities', encoding)
        except ValueError as e:
            assert str(e) == 'File must have extension CSV'

    def test_generate_human(self):
        man = generator.generate_human(data, 'male', False).split(' ')
        assert man[0] in data['male_surname']
        assert man[1] in data['male_names']
        assert man[2] in data['male_patronymic']

    def test_create_parser(self):
        parser = generator.create_parser()
        assert parser.parse_known_args(
            ['database.json', '-f', '{name}', '-n', '10',
             '-w'])[0] == argparse.Namespace(
            count=10, database='database.json', encoding=encoding,
            format='{name}', gender='all', weights=True)
        assert parser.description == 'Generate fictious data'
        assert parser.epilog == '(c) Piskunova Victoria 2018'
