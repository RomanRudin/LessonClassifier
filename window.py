from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy
import matplotlib
from schedule import save, schedule, format, format_week, day_order
#from module import 

class Window(QWidget):
    def __init__(self):
        super().__init__()
        '''
        
        '''

        #valuables
        self.selected = ''
        self.form = ''
        self.day = 'Понедельник'
        with open('lessons.txt', 'r', encoding='utf-8') as file:
            self.lessons = file.read().splitlines().strip()

        #widgets
        #
        label_main = QLabel('')
        label_main.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_main.setObjectName('label')

        #
        self.list_of_saved = QListWidget()
        self.list_of_saved.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_of_saved.setObjectName('list_of_saved')

        #
        button_add = QPushButton('Добавить')
        button_delete = QPushButton('Удалить')
        button_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_add.setObjectName('button_list')
        button_delete.setObjectName('button_list')

        #
        label_form = QLabel('Выберите класс:')
        label_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_form.setObjectName('label_form')

        #
        self.form_buttons = []
        for form in range(5, 11 + 1):
            button_form = QPushButton(form)
            button_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button_form.setObjectName('button_form')
            button_form.clicked.connect(self.choose_form)
            self.form_buttons.append(button_form)

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
        self.combo_day.setObjectName('button_previous')
        
        #
        self.label_day = QLabel('')
        self.label_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_day.setObjectName('label_day')

        #
        self.list_schedule = QListWidget()
        self.list_schedule.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_schedule.setObjectName('list_schedule')

        #
        self.plot = QLabel('')
        self.plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot.setObjectName('plot')


        #layouts
        layout_main = QVBoxLayout()
        layout_list = QHBoxLayout()
        layout_form = QHBoxLayout()
        layout_day = QHBoxLayout()


        #adding wifgets to layouts
        layout_list.addWidget(button_add)
        layout_list.addWidget(button_delete)

        for button in button_form:
            layout_form.addWidget(button)
        
        layout_day.addWidget(button_previous)
        layout_day.addWidget(self.combo_day)
        layout_day.addWidget(button_next)

        layout_main.addWidget(label_main)
        layout_main.addWidget(self.list_of_saved)
        layout_main.addLayout(layout_list)
        layout_main.addLayout(layout_form)
        layout_main.addLayout(layout_day)
        layout_main.addWidget(self.list_schedule)


        #connectings
        self.combo_day.activated[str].connect(self.choose_day)

    '''
    
    '''
    
    #
    def update(self) -> None:
        self.selected = self.list_of_saved.selectedItems()[0].text()

    #
    def show(self) -> None:
        self.list_schedule.clear()
        '''
        Items in list_schedule are horisontal layouts with two widgets: 
        first one is QLabel with index (number) of lesson, 
        the second is QCOmboBox with all possible lessons as items and saved one as current
        '''
        for index, lesson in schedule[self.selected][self.form][self.day].items():
            #layout as item
            lesson_layout = QHBoxLayout()
            #Index of lesson
            indexer = QLabel(index)
            #QComboBox of available lessons with saved lesson as current
            lesson_combo = QComboBox()
            lesson_combo.addItems(self.lessons)
            if lesson != '':
                lesson_combo.setCurrentText(lesson)
            #Button of deleting item from list
            debutton = QPushButton()
            debutton.clicked.connect(self.lesson_deleting)
            
            indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            indexer.setObjectName('indexer')
            lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lesson_combo.setObjectName('debutton')
            debutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            debutton.setObjectName('debutton')

            lesson_layout.addWidget(indexer)
            lesson_layout.addWidget(lesson_combo)
            lesson_layout.addWidget(debutton)
            self.list_schedule.addItem(lesson_layout)
        #Adding extra item
            lesson_layout = QHBoxLayout()
            indexer = QLabel(len(schedule[self.selected][self.form][self.day]))
            lesson_combo = QComboBox()
            lesson_combo.addItems(self.lessons)
            debutton = QPushButton()
            debutton.clicked.connect(self.lesson_deleting)
            indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            indexer.setObjectName('indexer')
            lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            lesson_combo.setObjectName('debutton')
            debutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            debutton.setObjectName('debutton')
            lesson_layout.addWidget(indexer)
            lesson_layout.addWidget(lesson_combo)
            lesson_layout.addWidget(debutton)
            self.list_schedule.addItem(lesson_layout)

    #
    def choose_form(self) -> None:
        for index, button in enumerate(self.form_buttons):
            if button.clicked:
                self.form = index + 5

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
    
    #
    def lesson_deleting(self):
        pass