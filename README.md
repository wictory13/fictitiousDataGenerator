﻿# Генератор фиктивных данных

Версия 1.0
Автор: Пискунова Виктория (victory13.99@gmail.com)

## Описание
Генерирует фиктивные данные о человеке в формате: 
Фамилия Имя (с возможностью получить наиболее популярное) Отчество Адрес проживания (город, улица, дом, квартира) Дата рождения Профессия Доход Номер СНИЛС Случайное число с плавающей точкой Случайное целое число Случайная алфавитно-цифровая строка

#### Запуск приложения
На вход приложению подаётся база данных: json-файл со ссылками на csv-файлы, в которых хранятся данные

CLI: py generator.py database.json -w
или: py generator.py database.jsom --count 5 --gender male  

Более подробную информацию можно узнать в справке по ключу -h или --help.

## Состав
#### Модули приложения
- generator.py - главный файл запуска
- test_generator.py - файл с тестами на модули приложения
Пакет data_generators:
 - address_generator.py - генератор случайного адреса
 - birth_date_data_generator.py - генератор случайной даты рождения
 - format_data_generator.py - генератор данных, заданных в строке
 - initials_generator.py - генератор случайных инициалов человека (в том числе имён с "весами")
 - jobs_data_generator.py - генератор случайной профессии, зарплаты и номера СНИЛС
 - sequence_generator.py - генератор случайного числа (целого или вещественного) и случайной алфавитно-цифровой строки
#### Базы данных
- Файл со ссылками на базу данных: database.json
 - Города: cities.csv
 - Женские имена с указанием частоты: female_names.csv
 - Женские отчества: female_patronymic.csv
 - Женские фамилии: female_surname.csv
 - Мужские имена с указанием частоты: male_names.csv
 - Мужские отчества: male_patronymic.csv
 - Мужские фамилии: male_surname.csv
 - Улицы: streets.csv
 - Профессии с указанием заработной платы: jobs.csv


## Ссылки на источники
 - данные об улицах: http://mapdata.ru/sverdlovskaya-oblast/ekaterinburg/ulicy/
 - данные о городах: http://города-россия.рф/alphabet.php
 - данные о фамилиях: https://ru.wikipedia.org/wiki/Список_общерусских_фамилий
 - данные о профессиях: http://www.examen.ru/add/manual/spisok-professiy/
