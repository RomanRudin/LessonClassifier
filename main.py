if __name__ == "__main__":
    from appData.window import Window
    from appData.schedule import save, schedule
    from sys import argv, exit
    from PyQt5.QtWidgets import QApplication
        

    app = QApplication([argv]) 

    
    with open(r'appData\style.qss', 'r', encoding='utf-8') as file:                     
        app.setStyleSheet(file.read())


    main = Window()
    main.setWindowTitle('')
    main.resize(1900, 1080)


    main.show()
    main.showMaximized()
    
    exit(app.exec_())