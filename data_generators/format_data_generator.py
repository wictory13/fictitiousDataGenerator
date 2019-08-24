import data_generators.address_generator as ga
import data_generators.birth_date_data_generator as gb
import data_generators.initials_generator as gi
import data_generators.jobs_data_generator as gjd
import data_generators.sequence_generator as gs
import re


def create_format_dict(data, gender, weights):
    initials = gi.generate_initials(data, gender, weights)
    job_data = gjd.generate_job_and_salary(data['jobs']).split(': ')
    birth_date = gb.generate_birth_date()
    format_dict = {
        r'{initials}': initials, r'{surname}': initials.split()[0],
        r'{name}': initials.split()[1], r'{patronymic}': initials.split()[2],
        r'{job}': job_data[0], r'{salary}': job_data[1],
        r'{birth_date}': birth_date, '{age}':
            str(gb.calculate_age(birth_date)), r'{address}':
            ga.generate_address(data['cities'], data['streets']),
        r'{randint}': str(gs.generate_int()),
        r'{randflt}': str(gs.generate_float()),
        r'{alphanum}': gs.generate_alphanum_str(),
        r'{snils}': gjd.generate_snils()}
    return format_dict


def generate_format_data(data, gender, format_str, weights):
    format_dict = create_format_dict(data, gender, weights)
    for key in format_dict:
        format_str = re.sub(key, format_dict[key], format_str)
    return format_str
