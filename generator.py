from collections import defaultdict
from data_generators import *
import argparse
import csv
import json


def create_parser():
    parser = argparse.ArgumentParser(description='Generate fictious data',
                                     epilog='(c) Piskunova Victoria 2018')
    parser.add_argument('database', type=str, help='file with data links')
    parser.add_argument('-e', '--encoding', type=str,
                        help='encoding of input data', default='windows-1251')
    parser.add_argument('-f', '--format', type=str, metavar='format',
                        help='could create a format string with data, '
                             'string must be in double quotes, '
                             'choose data types from this list: '
                             '{name}, {surname}, {patronymic}, '
                             '{initials}, {birth_date}, {age}, '
                             '{job}, {salary}, {address}, {snils},'
                             '{randint}, {randflt}, {alphanum}', default='')
    parser.add_argument('-g', '--gender', type=str,
                        choices=['f', 'female', 'm', 'male'],
                        help='could generate people with the same gender',
                        default='all')
    parser.add_argument('-n', '--count', type=int,
                        help='count of fictious people to generate', default=1)
    parser.add_argument('-w', '--weights', action='store_true',
                        help='can generate peoples '
                             'names with more really frequency')
    return parser


def extract_all_data(json_data, encoding):
    data = {}
    for key in json_data:
        if isinstance(json_data[key], list):
            for file in json_data[key]:
                if key == 'jobs':
                    data[key] = extract_jobs(file, encoding)
                else:
                    extract_data(data, file, key, encoding)
        if isinstance(json_data[key], dict):
            for gender in json_data[key]:
                for file in json_data[key][gender]:
                    new_key = gender + '_' + key
                    if key == 'names':
                        data[new_key] = extract_names(
                            file, encoding)
                    else:
                        extract_data(data, file, new_key, encoding)
    return data


def extract_data(data, link, key, encoding):
    file = link.split('.')
    if len(file) >= 2:
        file_extension = file[-1].lower()
        if file_extension != 'csv':
            raise ValueError('File must have extension CSV')
    with open(link, 'r', encoding=encoding) as f:
        data[key] = [row[0] for row in csv.reader(f)]


def extract_jobs(link, encoding):
    jobs = defaultdict(tuple)
    with open(link, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            job, min_salary, max_salary = row
            jobs[job] = (int(min_salary), int(max_salary))
    return jobs


def extract_names(link, encoding):
    names = defaultdict(int)
    with open(link, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            name, frequency = row
            names[name] = int(frequency)
    return names


def generate_human(data, gender, weights):
    data_list = [
        initials_generator.generate_initials(data, gender, weights),
        address_generator.generate_address(data['cities'], data['streets']),
        birth_date_data_generator.generate_birth_date(),
        jobs_data_generator.generate_job_and_salary(data['jobs']),
        jobs_data_generator.generate_snils(),
        str(sequence_generator.generate_float()),
        str(sequence_generator.generate_int()),
        sequence_generator.generate_alphanum_str()]
    return ' '.join(data_list)


def read_json_data(path, encoding):
    with open(path, 'r', encoding=encoding) as f:
        json_data = json.loads(f.read())
    return json_data


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    json_data = read_json_data(namespace.database, namespace.encoding)
    data = extract_all_data(json_data, namespace.encoding)
    if namespace.format != '':
        for _ in range(namespace.count):
            print(format_data_generator.generate_format_data(
                data, namespace.gender, namespace.format, namespace.weights))
    else:
        for _ in range(namespace.count):
            print(generate_human(data, namespace.gender, namespace.weights))
