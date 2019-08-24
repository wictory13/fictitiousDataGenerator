import random


def create_snils_control_number(snils):
    sum_ = 0
    for i in range(9):
        sum_ += int(snils[i]) * (9 - i)
    if sum_ < 100:
        control_number = sum_
    elif sum_ == 100 or sum_ == 101:
        control_number = 0
    else:
        control_number = sum_ % 101
        if control_number == 100:
            control_number = 0
    return control_number


def generate_job_and_salary(jobs):
    job = random.choice(list(jobs.keys()))
    salary = random.randint(int(jobs[job][0]), int(jobs[job][1]))
    return '{}: {}р.'.format(job, salary)


def generate_snils():
    first = random.randrange(1, 10**3)
    second = random.randrange(1, 10**3)
    third = random.randrange(1, 10**3)
    number = '{:03}{:03}{:03}'.format(first, second, third)
    control_number = create_snils_control_number(number)
    return '{:03}-{:03}-{:03} {:02}'.format(
        first, second, third, control_number)
