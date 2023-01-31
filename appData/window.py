from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from appData.schedule import save, schedule, format, format_week, day_order, form_order
from json import load     

class Window(QWidget):
    def __init__(self):
        super().__init__()
        '''
        
        '''

        #valuables
        self.selected = ''
        self.form = "11"
        self.day = 'Понедельник'
        self.space = 0

        with open(r'appData\lessons.json', 'r', encoding='utf-8') as file:
            self.lessons = load(file)

        #widgets
        #
        self.list_of_saved = QListWidget()
        self.list_of_saved.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for config in schedule.keys():
            self.list_of_saved.addItem(str(config))

        #
        self.edit_add = QLineEdit()
        self.edit_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #
        self.button_add = QPushButton('Добавить')
        self.button_delete = QPushButton('Удалить')
        self.button_add.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_add.setDisabled(True)

        #
        self.button_previous_form = QPushButton('Предыдущий класс')
        self.button_next_form = QPushButton('Следующий класс')
        self.button_previous_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_next_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #
        self.combo_form = QComboBox()
        self.combo_form.addItems(self.lessons.keys())
        self.combo_form.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #
        self.button_previous_day = QPushButton('Предыдущий день')
        self.button_next_day = QPushButton('Следующий день')
        self.button_previous_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_next_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #
        self.combo_day = QComboBox()
        self.combo_day.addItems(format_week["week"].keys())
        self.combo_day.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        #
        self.figure = plt.figure()
        
        # This is the Canvas Widget that displays the 'figure'. It takes the 'figure' instance as a parameter to __init__.
        self.canvas = FigureCanvas(self.figure)
  
        # This is the Navigation widget. Takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        #
        self.result = QLabel('0')
        self.result.setAlignment(Qt.AlignHCenter)
        self.result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result.setObjectName('result')


        # Layouts:
        layout_main = QVBoxLayout()
        layout_list = QHBoxLayout()
        layout_form = QHBoxLayout()
        layout_day = QHBoxLayout()
        self.layout_schedule = QVBoxLayout()


        # Adding wifgets to layouts
        layout_list.addWidget(self.button_add, stretch = 2)
        layout_list.addSpacing(60)
        layout_list.addWidget(self.button_delete, stretch = 2)
        
        layout_form.addWidget(self.button_previous_form, stretch=1)
        layout_form.addWidget(self.combo_form, stretch=5)
        layout_form.addWidget(self.button_next_form, stretch=1)

        layout_day.addWidget(self.button_previous_day, stretch=1)
        layout_day.addWidget(self.combo_day, stretch=5)
        layout_day.addWidget(self.button_next_day, stretch=1)

        # Layout_main.addWidget(label_main, stretch=1)
        layout_main.addWidget(self.list_of_saved, stretch=4)
        layout_main.addWidget(self.edit_add, stretch=2)
        layout_main.addLayout(layout_list, stretch=3)
        layout_main.addLayout(layout_form, stretch=4)
        layout_main.addLayout(layout_day, stretch=4)
        layout_main.addLayout(self.layout_schedule, stretch=25)
        layout_main.addWidget(self.result, stretch=1)
        layout_main.addWidget(self.toolbar, stretch=2)
        layout_main.addWidget(self.canvas, stretch=11)


        # Connectings events to methods
        self.list_of_saved.itemClicked.connect(self.__update)
        self.button_next_form.clicked.connect(lambda: self.__set_form('next'))
        self.button_previous_form.clicked.connect(lambda: self.__set_form('previous'))
        self.combo_form.activated[str].connect(lambda: self.__set_form('choose'))
        self.button_next_day.clicked.connect(lambda: self.__set_day('next'))
        self.button_previous_day.clicked.connect(lambda: self.__set_day('previous'))
        self.combo_day.activated[str].connect(lambda: self.__set_day('choose'))
        self.edit_add.editingFinished.connect(self.__set_visible)
        self.button_add.clicked.connect(self.__add_conffig)
        self.button_delete.clicked.connect(self.__delete_config)

        # Disabling all the buttons
        self.__enabling(False)

        # Setting main layout
        self.setLayout(layout_main)

    '''
    
    '''


    # Saves everything. Called when a new lesson is added or an existing lesson is deleted.
    def __saving(self, lesson_layout: QHBoxLayout) -> None:
        index, lesson_combo, difficulty = lesson_layout.itemAt(0).widget(), lesson_layout.itemAt(1).widget(), lesson_layout.itemAt(2).widget()
        schedule[self.selected][self.form]["week"][self.day][index.text()] = lesson_combo.currentText()
        schedule[self.selected][self.form]["result"] = self.result_data
        difficulty.setText(str(self.lessons[self.form][lesson_combo.currentText()]))
        save()
        self.__count_result()



    # Eneables and disables all the buttons.
    def __enabling(self, enabled: bool) -> None:
        self.button_next_day.setEnabled(enabled)
        self.combo_day.setEnabled(enabled)
        self.button_previous_day.setEnabled(enabled)
        self.button_next_form.setEnabled(enabled)
        self.combo_form.setEnabled(enabled)
        self.button_previous_form.setEnabled(enabled)
        self.button_delete.setEnabled(enabled)

    # Changes availability of the 'create configuration' button if the input line has been edited.
    def __set_visible(self) -> None:
        if self.edit_add.text() != '':
            self.button_add.setEnabled(True)

    # Updates the application when the configuration has been changed. Can be called when the user selects a configuration.
    def __update(self) -> None:
        self.selected = self.list_of_saved.selectedItems()[0].text()
        self.__enabling(True)
        self.__set_form('next')
        


    # Constructs the schedule layout. Called when a new schedule is displayed or when the schedule is updated.
    def __show_list(self) -> None:
        self.__hide_list()
        index = 0
        for index, lesson in schedule[self.selected][self.form]["week"][self.day].items():
            self.layout_schedule.addLayout(self.__lesson_in_list(int(index), lesson), stretch=1)
        self.__new_in_list()
        self.space = 8 - int(index)
        if self.space >= 1:
            self.layout_schedule.addWidget(QLabel(), stretch=self.space)
        self.__count_result()
        
    # Deletes everything from the schedule (to then update or close it). Called when a new schedule is displayed or when a selected configuration is deleted.
    def __hide_list(self) -> None:
        for i in reversed(range(self.layout_schedule.count())): 
            self.__delete_items_of_layout(self.layout_schedule.takeAt(i).layout())



    # Creates a layout with lesson information. Called inside __show_list() or when a new lesson is added to the schedule.
    def __lesson_in_list(self, index:int, lesson: str) -> QHBoxLayout:
        '''
        Items in list_schedule are horisontal layouts with three widgets: 
        the first one is QLabel with index (number) of lesson, 
        the second is QCOmboBox with all possible lessons as items and saved one as current
        the third is QLabel with difficulty of the chosen lesson
        '''
        # layout as item
        lesson_layout = QHBoxLayout()
        # Index of the lesson
        indexer = QLabel(str(index))
        # Difficulty of the lesson
        difficulty = QLabel()
        # QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        if lesson != ' ':
            lesson_combo.setCurrentText(lesson)
            difficulty.setText(str(self.lessons[self.form][lesson]))
        lesson_combo.currentIndexChanged[str].connect(lambda: self.__saving(lesson_layout))
        # Renaming and changing size policy of those widgets
        indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        difficulty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Adding widgets to layout
        lesson_layout.addWidget(indexer, stretch=1)
        lesson_layout.addWidget(lesson_combo, stretch=22)
        lesson_layout.addWidget(difficulty, stretch=2)
        #
        if index % 2 == 0:
            indexer.setStyleSheet('''
                background-color: rgb(255, 255, 255);
                border: 2px solid black''')
            lesson_combo.setStyleSheet('''
                background-color: rgb(255, 255, 255);
                border: 2px solid black''')
            difficulty.setStyleSheet('''
                background-color: rgb(255, 255, 255);
                border: 2px solid black;
                color: red''')
        else:
            indexer.setStyleSheet('''
                background-color: rgb(195, 195, 195);
                border: 2px solid black''')
            lesson_combo.setStyleSheet('''
                background-color: rgb(195, 195, 195);
                border: 2px solid black''')
            difficulty.setStyleSheet('''
                background-color: rgb(195, 195, 195);
                border: 2px solid black;
                color: red''')
        return lesson_layout

    # Creates a layout with tools for adding and removing lessons. Called by __show_list()
    def __new_in_list(self) -> None:
        # Getting data about how many lessons there already are
        index = self.__lessons_update()
        # Adding extra item
        lesson_layout = QHBoxLayout()
        # Index of lesson
        indexer = QLabel(str(index + 1))
        # Button of deleting item from list
        debutton = QPushButton()
        debutton.clicked.connect(lambda: self.__lesson_deleting(debutton, False))
        # QComboBox of available lessons with saved lesson as current
        lesson_combo = QComboBox()
        lesson_combo.addItems(self.lessons[self.form])
        lesson_combo.activated[str].connect(lambda: self.__add_lesson(lesson_layout))
        # Renaming and changing size policy of those widgets
        indexer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lesson_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        debutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Adding widgets to layout
        lesson_layout.addWidget(indexer, stretch=1)
        lesson_layout.addWidget(lesson_combo, stretch=15)
        lesson_layout.addWidget(debutton, stretch=9)
        self.layout_schedule.addLayout(lesson_layout, stretch=1)
        indexer.setStyleSheet('''
            background-color: rgb(174, 174, 174);
            border: 2px solid black''')
        lesson_combo.setStyleSheet('''
            background-color: rgb(174, 174, 174);
            border: 2px solid black''')
        debutton.setStyleSheet('''
            border: 2px solid red;
            background-color: rgb(247, 247, 247)''')



    # Changes the form that is currently displayed to the selected form. Can be called by form navigation buttons and combo boxes.
    def __set_form(self, mode) -> None:
        if mode == "next":
            self.form = form_order[(form_order.index(self.form) + 1) % len(form_order)]
        elif mode == 'previous':
            self.form = form_order[form_order.index(self.form) - 1]
        else:
            self.form = self.combo_form.currentText()
        self.combo_form.setCurrentText(str(self.form))
        self.result_data = schedule[self.selected][self.form]["result"]
        self.__show_list()

    # Changes the day currently displayed to the selected day. Can be invoked with the day navigation buttons and combo boxes.
    def __set_day(self, mode) -> None:
        if mode == "next":
            self.day = day_order[(day_order.index(self.day) + 1) % len(day_order)]
        elif mode == 'previous':
            self.day = day_order[day_order.index(self.day) - 1]
        else:
            self.day = self.combo_day.currentText()
        self.combo_day.setCurrentText(self.day)
        self.__show_list()

    

    # Returns the maximum index of the existing lessons. Called when the schedule bar is updated.
    def __lessons_update(self) -> int:
        key_crutch = list(map(int, schedule[self.selected][self.form]["week"][self.day].keys()))
        key_crutch.append(0)
        return max(key_crutch)

    # Adds a new lesson to the end of the schedule. Can be called by a QComboBox on the toolbar at the bottom of the schedule.
    def __add_lesson(self, lesson_layout: QHBoxLayout) -> None:
        label, lesson_combo, button = lesson_layout.itemAt(0).widget(), lesson_layout.itemAt(1).widget(), lesson_layout.itemAt(2).widget()
        index = self.__lessons_update()
        if index <= 8:
            new_lesson =  self.__lesson_in_list(index + 1, lesson_combo.currentText())
            self.__saving(new_lesson)
            self.layout_schedule.insertLayout(index, new_lesson, stretch=1)
            if self.space > 0:
                self.space -= 1
                self.layout_schedule.setStretch(index + 2, self.space)
            label.setText(str(index + 2))
            lesson_combo.setCurrentIndex(0)
            self.__lesson_deleting(button, just_check=True)
            self.__count_result()

    # Removes the last lesson from the schedule. Can be called with the "Delete" button on the schedule toolbar.
    def __lesson_deleting(self, button: QPushButton, just_check: bool) -> None:
        counter = self.layout_schedule.count() - 2
        if self.space > 0:
            counter -= 1
        if not just_check:
            if counter >= 0:
                deleted = self.layout_schedule.itemAt(counter).layout()
                schedule[self.selected][self.form]["week"][self.day].pop(deleted.itemAt(0).widget().text())
                self.__delete_items_of_layout(deleted)
                deleted.setParent(None)
                save()
            if counter < 0:
                button.setEnabled(False)
            self.__show_list()
        else:
            if counter >= 0:
                button.setEnabled(True)

    # Removes all widgets from the layout, setting their parent to None. Called by __hide_list()
    def __delete_items_of_layout(self, layout) -> None:
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.__delete_items_of_layout(item.layout())
    


    # Writes a summary of the difficulties of all the lessons. Called when a new schedule is displayed or when the schedule is updated.
    def __count_result(self) -> None:
        difficulty_of_the_day = 0
        for lesson in schedule[self.selected][self.form]["week"][self.day].values():
            difficulty_of_the_day += self.lessons[self.form][lesson]
        self.result.setText(str(difficulty_of_the_day))
        self.result_data[day_order.index(self.day)] = difficulty_of_the_day
        self.__plot()



    # Creates a new configuration. Can be called with the 'create configuration' button after editing the input line
    def __add_conffig(self) -> None:
        name = self.edit_add.text()
        if name != '':
            schedule[name] = format.copy()
            self.list_of_saved.addItem(name)
            save()

    # Deletes the configuration, called with the 'delete confiration' button.
    def __delete_config(self) -> None:
        schedule.pop(self.list_of_saved.selectedItems()[0].text())
        self.list_of_saved.takeItem(self.list_of_saved.selectedIndexes()[0].row())
        self.__enabling(False)
        self.__hide_list()
        save()



    # Creates a full-featured plot at the bottom of the application. Called when the schedule layout is updated.
    def __plot(self) -> None:
        # Clearing old figure
        self.figure.clear()
        # Creating an axis
        ax = self.figure.add_subplot(111)
        # Plot data
        ax.plot(day_order, self.result_data)
        # Refreshing canvas
        self.canvas.draw()