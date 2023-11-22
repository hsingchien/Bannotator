from bannotator.mainwindow import MainWindow
import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    app.installEventFilter(mainwindow)
    app.setApplicationName("Bannotator")
    app.setWindowIcon(QIcon(":/icon.ico"))
    mainwindow.show()
    print("Happy annotating!")
    app.exec()


if __name__ == "__main__":
    main()
