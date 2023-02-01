from genericpath import exists
from json import dump, load
from os import listdir, remove, path

#
format_week = {'week': {
            'Понедельник': {
                1: '',
                2: '',
                3: '',
                4: ''
            },
            'Вторник': {
                1: '',
                2: '',
                3: '',
                4: ''
            },
            'Среда': {
                1: '',
                2: '',
                3: '',
                4: ''
            },
            'Четверг': {
                1: '',
                2: '',
                3: '',
                4: ''
            },
            'Пятница': {
                1: '',
                2: '',
                3: '',
                4: ''
            },
            'Суббота': {
            }
        },
        'result': [0] * 6
    }

#
format = {"5":  format_week.copy(),
          "6":  format_week.copy(),
          "7":  format_week.copy(),
          "8":  format_week.copy(),
          "9":  format_week.copy(),
          "10": format_week.copy(),
          "11": format_week.copy()}

#
day_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
form_order = ["5", "6", "7", "8", "9", "10", "11"]

#
userdir = r'appData\userData'


#
def files():
    direct = list(file[:-5] for file in listdir(userdir))
    return direct

#
def upload(file):
    try:
        with open(rf'{userdir}\{file}.json', 'r', encoding='utf-8') as file:
            return load(file)
    except ImportError:
        pass

#
def delete_file(file):
    try:
        remove(rf'{userdir}\{file}.json')
    except FileNotFoundError:
        pass

#
def create_file(name):
    if not path.exists(rf'{userdir}\{name}.json'):
        save(name, format)

#
def save(file, schedule):
    with open(rf'{userdir}\{file}.json', 'w', encoding='utf-8') as file:
        dump(schedule, file, sort_keys=False, ensure_ascii=False, indent=4)