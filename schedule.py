from json import dump, load

#
day_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Субботы']

#
try:
    with open('data.json', 'r', encoding='utf-8') as file:
        schedule = load(file)
except ImportError:
    print()

#
format_week = {'Понедельник': {
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' '
        },
        'Вторник': {
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' '
        },
        'Среда': {
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' '
        },
        'Четверг': {
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' '
        },
        'Пятница': {
            1: ' ',
            2: ' ',
            3: ' ',
            4: ' '
        },
        'Суббота': {
        }}

#
format = {5:  format_week.copy(),
          7:  format_week.copy(),
          8:  format_week.copy(),
          9:  format_week.copy(),
          10: format_week.copy(),
          11: format_week.copy()}

#
def save():
    with open('data.json', 'w', encoding='utf-8') as file:
        dump(schedule, file, sort_keys=True, ensure_ascii=False)