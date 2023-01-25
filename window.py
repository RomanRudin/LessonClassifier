from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from schedule import save, schedule, format, format_week, day_order, form_order
from json import load
#TODO from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#TODO from matplotlib.figure import Figure


#TODO class MplCanvas(FigureCanvasQTAgg):
#TODO 
#TODO     def __init__(self, parent=None, width=5, height=4, dpi=100):
#TODO         fig = Figure(figsize=(width, height), dpi=dpi)
#TODO         self.axes = fig.add_subplot(111)
#TODO         
class Window(QWidget):
    def __init__(self):
        super().__init__()
        '''
        
        '''

        #valuables
        self.selected = ''
        self.form = "5"
        self.day = 'Понедельник'
        self.space = 0

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
        self.button_delete = QPushButton('Удалить')
        self.button_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_add.setObjectName('button_list')
        self.button_delete.setObjectName('button_list')
        self.button_add.setDisabled(True)

        #
        label_form = QLabel('Выберите класс:')
        label_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label_form.setObjectName('label_form')

        #
        self.button_previous_form = QPushButton('Предыдущий класс')
        self.button_next_form = QPushButton('Следующий класс')
        self.button_previous_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_next_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_previous_form.setObjectName('button_day')
        self.button_next_form.setObjectName('button_day')

        #
        self.combo_form = QComboBox()
        self.combo_form.addItems(self.lessons.keys())
        self.combo_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_form.setObjectName('combo_form')

        #
        self.button_previous_day = QPushButton('Предыдущий день')
        self.button_next_day = QPushButton('Следующий день')
        self.button_previous_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_next_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_previous_day.setObjectName('button_day')
        self.button_next_day.setObjectName('button_day')

        #
        self.combo_day = QComboBox()
        self.combo_day.addItems(format_week["week"].keys())
        self.combo_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_day.setObjectName('combo_day')
        
        #
        self.label_day = QLabel('')
        self.label_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_day.setObjectName('label_day')
        


        self.figure = plt.figure()
        
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
  
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)


        self.result = QLabel('0')
        self.result.setAlignment(Qt.AlignHCenter)
        self.result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result.setObjectName('result')


        #layouts
        layout_main = QVBoxLayout()
        layout_list = QHBoxLayout()
        layout_form = QHBoxLayout()
        layout_day = QHBoxLayout()
        #
        self.layout_schedule = QVBoxLayout()


        #adding wifgets to layouts
        layout_list.addWidget(self.button_add, stretch = 2)
        layout_list.addSpacing(60)
        layout_list.addWidget(self.button_delete, stretch = 2)
        
        layout_form.addWidget(self.button_previous_form, stretch=1)
        layout_form.addWidget(self.combo_form, stretch=5)
        layout_form.addWidget(self.button_next_form, stretch=1)

        layout_day.addWidget(self.button_previous_day, stretch=1)
        layout_day.addWidget(self.combo_day, stretch=5)
        layout_day.addWidget(self.button_next_day, stretch=1)

        layout_main.addWidget(label_main, stretch=1)
        layout_main.addWidget(self.list_of_saved, stretch=3)
        layout_main.addWidget(self.edit_add, stretch=1)
        layout_main.addLayout(layout_list, stretch=1)
        layout_main.addLayout(layout_form, stretch=2)
        layout_main.addLayout(layout_day, stretch=2)
        layout_main.addLayout(self.layout_schedule, stretch=10)
        layout_main.addWidget(self.result, stretch=1)
        layout_main.addWidget(self.toolbar, stretch=1)
        layout_main.addWidget(self.canvas, stretch=5)


        #connectings
        self.list_of_saved.itemClicked.connect(self.update)
        self.button_next_form.clicked.connect(lambda: self.set_form('next'))
        self.button_previous_form.clicked.connect(lambda: self.set_form('previous'))
        self.combo_form.activated[str].connect(lambda: self.set_form('choose'))
        self.button_next_day.clicked.connect(lambda: self.set_day('next'))
        self.button_previous_day.clicked.connect(lambda: self.set_day('previous'))
        self.combo_day.activated[str].connect(lambda: self.set_day('choose'))
        self.edit_add.editingFinished.connect(self.set_visible)
        self.button_add.clicked.connect(self.add_conffig)
        self.button_delete.clicked.connect(self.delete_config)

        #disabling all the buttons
        self.enabling(False)

        #setting main layout
        self.setLayout(layout_main)

    '''
    
    '''

    #
    def plot(self) -> None:
        # clearing old figure
        self.figure.clear()
  
        # create an axis
        ax = self.figure.add_subplot(111)
  
        # plot data
        ax.plot(day_order, self.result_data)
  
        # refresh canvas
        self.canvas.draw()

    #Method eneables and disables all the buttons
    def enabling(self, enabled: bool) -> None:
        self.button_next_day.setEnabled(enabled)
        self.combo_day.setEnabled(enabled)
        self.button_previous_day.setEnabled(enabled)
        self.button_next_form.setEnabled(enabled)
        self.combo_form.setEnabled(enabled)
        self.button_previous_form.setEnabled(enabled)
        self.button_delete.setEnabled(enabled)
        
    
    #
    def lesson_in_list(self, index:int, lesson: str) -> QHBoxLayout:
        '''
        Items in list_schedule are horisontal layouts with two widgets: 
        first one is QLabel with index (number) of lesson, 
        the second is QCOmboBox with all possible lessons as items and saved one as current
        '''
        #layout as item
        lesson_layout = QHBoxLayout()
        #Index of lesson
        indexer = QLabel(str(index))
        #
        difficulty = QLabel()
        #QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        if lesson != ' ':
            lesson_combo.setCurrentText(lesson)
            difficulty.setText(str(self.lessons[self.form][lesson]))
        lesson_combo.currentIndexChanged[str].connect(lambda: self.saving(lesson_layout))
        #
        indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        indexer.setObjectName('indexer')
        lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lesson_combo.setObjectName('lesson_combo')
        difficulty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        difficulty.setObjectName('difficulty')
        #
        lesson_layout.addWidget(indexer, stretch=1)
        lesson_layout.addWidget(lesson_combo, stretch=22)
        lesson_layout.addWidget(difficulty, stretch=2)
        return lesson_layout

    def new_in_list(self) -> None:
        #Getting data about how many lessons there already are
        index = self.lessons_update()
        #Adding extra item
        lesson_layout = QHBoxLayout()
        #Index of lesson
        indexer = QLabel(str(index + 1))
        #Button of deleting item from list
        debutton = QPushButton()
        debutton.clicked.connect(lambda: self.lesson_deleting(debutton, False))
        #QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        lesson_combo.activated[str].connect(lambda: self.add_lesson(lesson_layout))
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
        lesson_layout.addWidget(debutton, stretch=9)
        self.layout_schedule.addLayout(lesson_layout, stretch=1)
    
    #
    def lessons_update(self) -> None:
        key_crutch = list(map(int, schedule[self.selected][self.form]["week"][self.day].keys()))
        key_crutch.append(0)
        return max(key_crutch)

    #
    def saving(self, lesson_layout: QHBoxLayout) -> None:
        index, lesson_combo, difficulty = lesson_layout.itemAt(0).widget(), lesson_layout.itemAt(1).widget(), lesson_layout.itemAt(2).widget()
        schedule[self.selected][self.form]["week"][self.day][index.text()] = lesson_combo.currentText()
        schedule[self.selected][self.form]["result"] = self.result_data
        difficulty.setText(str(self.lessons[self.form][lesson_combo.currentText()]))
        save()
        self.count_result()

    #
    def add_lesson(self, lesson_layout: QHBoxLayout) -> None:
        label, lesson_combo, button = lesson_layout.itemAt(0).widget(), lesson_layout.itemAt(1).widget(), lesson_layout.itemAt(2).widget()
        index = self.lessons_update()
        new_lesson =  self.lesson_in_list(index + 1, lesson_combo.currentText())
        self.saving(new_lesson)
        self.layout_schedule.insertLayout(index, new_lesson, stretch=1)
        if self.space > 0:
            self.space -= 1
            self.layout_schedule.setStretch(index + 2, self.space)
        label.setText(str(index + 2))
        lesson_combo.setCurrentIndex(0)
        self.lesson_deleting(button, just_check=True)
        self.count_result()

    #
    def lesson_deleting(self, button: QPushButton, just_check: bool) -> None:
        counter = self.layout_schedule.count() - 2
        if self.space > 0:
            counter -= 1
        if not just_check:
            if counter >= 0:
                deleted = self.layout_schedule.itemAt(counter).layout()
                schedule[self.selected][self.form]["week"][self.day].pop(deleted.itemAt(0).widget().text())
                self.deleteItemsOfLayout(deleted)
                deleted.setParent(None)
                save()
            if counter < 0:
                button.setEnabled(False)
            self.show_list()
        else:
            if counter >= 0:
                button.setEnabled(True)

    #
    def deleteItemsOfLayout(self, layout) -> None:
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    #
    def update(self) -> None:
        self.selected = self.list_of_saved.selectedItems()[0].text()
        self.enabling(True)
        self.set_form("previous")
        self.set_form("next")
        self.show_list()

    #
    def show_list(self) -> None:
        self.hide_list()
        index = 0
        for index, lesson in schedule[self.selected][self.form]["week"][self.day].items():
            self.layout_schedule.addLayout(self.lesson_in_list(int(index), lesson), stretch=1)
        self.new_in_list()
        self.space = 8 - int(index)
        if self.space >= 1:
            self.layout_schedule.addWidget(QLabel(), stretch=self.space)
        self.count_result()
    
    #
    def count_result(self) -> None:
        difficulty_of_the_day = 0
        for lesson in schedule[self.selected][self.form]["week"][self.day].values():
            difficulty_of_the_day += self.lessons[self.form][lesson]
        self.result.setText(str(difficulty_of_the_day))
        self.result_data[day_order.index(self.day)] = difficulty_of_the_day
        self.plot()
        
    #
    def hide_list(self) -> None:
        for i in reversed(range(self.layout_schedule.count())): 
            self.deleteItemsOfLayout(self.layout_schedule.takeAt(i).layout())

    #
    def add_conffig(self) -> None:
        name = self.edit_add.text()
        if name != '':
            schedule[name] = format.copy()
            self.list_of_saved.addItem(name)
            save()

    #
    def delete_config(self) -> None:
        schedule.pop(self.list_of_saved.selectedItems()[0].text())
        self.list_of_saved.takeItem(self.list_of_saved.selectedIndexes()[0].row())
        self.enabling(False)
        self.hide_list()
        save()

    #
    def set_form(self, mode) -> None:
        if mode == "next":
            self.form = form_order[(form_order.index(self.form) + 1) % len(form_order)]
        elif mode == 'previous':
            self.form = form_order[form_order.index(self.form) - 1]
        else:
            self.form = self.combo_form.currentText()
        self.combo_form.setCurrentText(str(self.form))
        self.result_data = schedule[self.selected][self.form]["result"]
        self.show_list()
        

    #
    def set_day(self, mode) -> None:
        if mode == "next":
            self.day = day_order[(day_order.index(self.day) + 1) % len(day_order)]
        elif mode == 'previous':
            self.day = day_order[day_order.index(self.day) - 1]
        else:
            self.day = self.combo_day.currentText()
        self.combo_day.setCurrentText(self.day)
        self.show_list()

    #
    def set_visible(self) -> None:
        if self.edit_add.text() != '':
            self.button_add.setEnabled(True)
    