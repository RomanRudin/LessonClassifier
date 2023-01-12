if __name__ == "__main__":
    try:
        from window import Window
        from PyQt5.QtWidgets import QApplication
        from sys import argv, exit
        from json import load
    except ImportError:
        print('Файлы программы повреждены. Обратитесь к разработчику.')
        

    app = QApplication([argv]) 


    try:
        with open('data1.json', 'r', encoding='utf-8') as file:
            data = load(file)
        with open('style.qss', 'r', encoding='utf-8') as file:                     
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print('Файлы программы повреждены. Обратитесь к разработчику.')


    main = Window()
    main.setWindowTitle('')
    main.resize(1900, 1080)


    main.show()
    
    exit(app.exec_())