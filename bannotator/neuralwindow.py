from bannotator.ui.ui_neural_mainwindow import Ui_NeuralWindow
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
class NeuralWindow(QMainWindow, Ui_NeuralWindow):
    closed = Signal(bool)
    def __init__(self, state=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Neural data")
        self.setWindowIcon(QIcon(":/icon.ico"))
        self.state = state
        self.neural_records = dict()
        self.avg_traces = dict()
        # Setup actions
        self.actionImportNeuralRecord.triggered.connect(self.open_neural_record)
        self.actionResetNeuralRecording.triggered.connect(self.recet_neural_record)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit(False)



    
    


