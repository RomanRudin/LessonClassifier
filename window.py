from copy import copy
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy, QLineEdit
import matplotlib
from schedule import save, schedule, format, format_week, day_order
from json import load
#from module import 

class Window(QWidget):
    def __init__(self):
        super().__init__()
        '''
        
        '''

        #valuables
        self.selected = ''
        self.form = "5"
        self.day = 'Понедельник'
        with open('lessons.json', 'r', encoding='utf-8') as file:
            self.lessons = load(file)

        #widgets
        #
        label_main = QLabel('')
        label_main.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_main.setObjectName('label')

        #
        self.list_of_saved = QListWidget()
        self.list_of_saved.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_of_saved.setObjectName('list_of_saved')
        for config in schedule.keys():
            self.list_of_saved.addItem(str(config))

        #
        self.edit_add = QLineEdit()
        self.edit_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.edit_add.setObjectName('button_list')

        #
        self.button_add = QPushButton('Добавить')
        button_delete = QPushButton('Удалить')
        self.button_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_add.setObjectName('button_list')
        button_delete.setObjectName('button_list')
        self.button_add.setDisabled(True)

        #
        label_form = QLabel('Выберите класс:')
        label_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_form.setObjectName('label_form')

        #
        self.combo_form = QComboBox()
        self.combo_form.addItems(self.lessons.keys())
        self.combo_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_form.setObjectName('combo_form')

        #
        button_previous = QPushButton('Предыдущий день')
        button_next = QPushButton('Следующий день')
        button_previous.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_next.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_previous.setObjectName('button_day')
        button_next.setObjectName('button_day')

        #
        self.combo_day = QComboBox()
        self.combo_day.addItems(format_week.keys())
        self.combo_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_day.setObjectName('combo_day')
        
        #
        self.label_day = QLabel('')
        self.label_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_day.setObjectName('label_day')

        #
        self.plot = QLabel('')
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot.setObjectName('plot')


        #layouts
        layout_main = QVBoxLayout()
        layout_list = QHBoxLayout()
        layout_day = QHBoxLayout()
        #
        self.layout_schedule = QVBoxLayout()


        #adding wifgets to layouts
        layout_list.addWidget(self.button_add)
        layout_list.addSpacing(2)
        layout_list.addWidget(button_delete)
        
        layout_day.addWidget(button_previous, stretch=1)
        layout_day.addWidget(self.combo_day, stretch=5)
        layout_day.addWidget(button_next, stretch=1)

        layout_main.addSpacing(2)
        layout_main.addWidget(label_main, stretch=1)
        layout_main.addWidget(self.list_of_saved, stretch=6)
        layout_main.addWidget(self.edit_add, stretch=2)
        layout_main.addLayout(layout_list, stretch=2)
        layout_main.addWidget(self.combo_form, stretch=2)
        layout_main.addLayout(layout_day, stretch=2)
        layout_main.addLayout(self.layout_schedule, stretch=10)
        layout_main.addWidget(self.plot, stretch=5)


        #connectings
        self.list_of_saved.itemClicked.connect(self.update)
        self.combo_day.activated[str].connect(self.choose_day)
        self.combo_form.activated[str].connect(self.choose_form)
        button_next.clicked.connect(self.next_day)
        button_previous.clicked.connect(self.previous_day)
        self.edit_add.editingFinished.connect(self.set_visible)
        self.button_add.clicked.connect(self.add_conffig)
        button_delete.clicked.connect(self.delete_config)

        #setting main layout
        self.setLayout(layout_main)

    '''
    
    '''

    #
    def _lesson_in_list(self, index, lesson):
        #layout as item
        lesson_layout = QHBoxLayout()
        #Index of lesson
        indexer = QLabel(index)
        #QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        if lesson != ' ':
            lesson_combo.setCurrentText(lesson)
        lesson_combo.activated[str].connect(lambda: self._saving(index, lesson_combo))
        #?#Button of deleting item from list
        #?debutton = QPushButton()
        #?debutton.clicked.connect(self.lesson_deleting)
        #
        indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        indexer.setObjectName('indexer')
        lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lesson_combo.setObjectName('lesson_combo')
        #
        lesson_layout.addWidget(indexer, stretch=1)
        lesson_layout.addWidget(lesson_combo, stretch=16)
        self.layout_schedule.addLayout(lesson_layout, stretch=1)
    #
    def _saving(self, index: int, lesson_combo: QComboBox, is_new=False, *qwidgets) -> None:
        schedule[self.selected][self.form][self.day][str(index)] = lesson_combo.currentText()
        save()
        if is_new:
            self._new_in_list()
            #qwidgets[0].removeWidget(qwidgets[1])
            qwidgets[1].setParent(None)
            self.show_list()

    def _new_in_list(self):
        key_crutch = list(map(int, schedule[self.selected][self.form][self.day].keys()))
        key_crutch.append(1)
        max_index = max(key_crutch)
        spacer_stretch = max(0, 7 - max_index)
        #Adding extra item
        lesson_layout = QHBoxLayout()
        #Index of lesson
        indexer = QLabel(str(max_index))
        #QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        lesson_combo.activated[str].connect(lambda: self._saving(max_index + 1, lesson_combo, True, lesson_layout, debutton))
        #Button of deleting item from list
        debutton = QPushButton()
        debutton.clicked.connect(self.lesson_deleting)
        #
        indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        indexer.setObjectName('indexer')
        lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lesson_combo.setObjectName('debutton')
        debutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        debutton.setObjectName('debutton')
        #
        lesson_layout.addWidget(indexer, stretch=1)
        lesson_layout.addWidget(lesson_combo, stretch=15)
        lesson_layout.addWidget(debutton, stretch=4)
        self.layout_schedule.addLayout(lesson_layout, stretch=1)
        self.layout_schedule.addSpacing(spacer_stretch)
    
    #
    def update(self) -> None:
        self.selected = self.list_of_saved.selectedItems()[0].text()
        self.show_list()

    #
    def show_list(self) -> None:
        print(self.layout_schedule.count())
        print()
        for i in range(self.layout_schedule.count() - 2, -1, -1):
            print(self.layout_schedule.itemAt(i))
        print()
        print()
        for i in range(self.layout_schedule.count() - 2, -1, -1): #The last element of layout is spacer, so I need -2 here
            print(i)
            print(self.layout_schedule.itemAt(i))
            self.layout_schedule.itemAt(i).layout().setParent(None) 
        '''
        Items in list_schedule are horisontal layouts with two widgets: 
        first one is QLabel with index (number) of lesson, 
        the second is QCOmboBox with all possible lessons as items and saved one as current
        '''
        for index, lesson in schedule[self.selected][self.form][self.day].items():
            self._lesson_in_list(index, lesson)
        self._new_in_list()
    #
    def add_conffig(self) -> None:
        name = self.edit_add.text()
        if name != '':
            schedule[name] = format.copy()
            self.list_of_saved.addItem(name)
            self.list_of_saved.setCurrentItem(self.list_of_saved.item(-1))
            save()

    #
    def delete_config(self) -> None:
        schedule.pop(self.list_of_saved.selectedItems()[0].text())
        self.list_of_saved.takeItem(self.list_of_saved.selectedIndexes()[0].row())
        save()

    #
    def choose_form(self) -> None:
        self.form = int(self.combo_form.currentText())

    #
    def next_day(self) -> None:
        self.day = day_order[(day_order.index(self.day) + 1) % len(day_order)]
        self.update_day()
    def previous_day(self) -> None:
        self.day = day_order[(day_order.index(self.day) - 1) % len(day_order)]
        self.update_day()
    def choose_day(self) -> None:
        self.day = self.combo_day.currentText()
        self.update_day()
    #
    def update_day(self):
        self.label_day.setText(self.day)
        self.show_list()

    #
    def set_visible(self) -> None:
        if self.edit_add.text() != '':
            self.button_add.setEnabled(True)
    
    #
    def lesson_deleting(self):
        counter = self.layout_schedule.count() - 3
        if counter >= 0:
            deleted = self.layout_schedule.itemAt(counter).layout()
            print(deleted)
            deleted.setParent(None)
            schedule[self.selected][self.form][self.day].pop(deleted.itemAt(0).widget().text())
            del deleted
            save()
            self.show_list()