from bannotator.mainwindow import MainWindow
import sys
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    app.installEventFilter(mainwindow)
    app.setApplicationName("Bannotator")
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()