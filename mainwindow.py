from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
      