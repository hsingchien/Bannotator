from bannotator.ui.ui_neural_mainwindow import Ui_NeuralWindow
from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from bannotator.data import NeuralRecording
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
        self.actionImportNeuralRecord.triggered.connect(self.import_neural_record)
        self.actionResetNeuralRecording.triggered.connect(self.reset_neural_record)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit(False)
        
    def import_neural_record(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        neural_path, _ = fileDialog.getOpenFileName(self, caption="Load neural recording", filter="Neural recording (*.json *.mat *.csv)")
        if not neural_path:
            return False
        nrecord = NeuralRecording()
        nrecord.load_from_file(neural_path)
        current_stream_id = int(self.trace_stream_combobox.currentText())
        self.neural_records[current_stream_id] = nrecord
        
    def reset_neural_record(self):
        print("reset")
        pass



    
    


