from mainwindow import MainWindow
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
mainwindow = MainWindow()
app.installEventFilter(mainwindow)
app.setApplicationName("Bannotator")
mainwindow.show()


app.exec()
