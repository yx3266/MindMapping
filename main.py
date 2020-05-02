from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QColor, QFont
from PyQt5.QtWidgets import *
import sys,time
import MainWindow

if __name__ == '__main__':           #程序入口
    app = QApplication(sys.argv)
    GUI_Window = MainWindow.MainWindow()
    GUI_Window.show()
    sys.exit(app.exec_())