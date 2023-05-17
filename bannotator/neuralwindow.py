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
        self.length = 0
        # Setup actions
        self.import_recording.clicked.connect(self._import_neural_record)
        self.reset_recording.clicked.connect(self._reset_neural_record)
        # Setup widgets
        self.trace_stream_combobox.currentTextChanged.connect(
            self.trace_view.refresh_plot
        )
        self.space_spinbox.valueChanged.connect(self._update_space)
        self.full_trace_push_button.toggled.connect(self._set_viewbox)
        self.full_trace_push_button.toggled.connect(self._set_view_button_text)
        self.cluster_button.clicked.connect(self._cluster_neural)
        # Connect state
        self.state.connect("current_frame", self._set_frame_stick)
        self.state.connect("slider_box", self._set_viewbox)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit(False)

    def _import_neural_record(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        neural_path, _ = fileDialog.getOpenFileName(
            self,
            caption="Load neural recording",
            filter="Neural recording (*.json *.mat *.csv)",
        )
        if not neural_path:
            return False
        nrecord = NeuralRecording()
        nrecord.load_from_file(neural_path)
        current_stream_id = int(self.trace_stream_combobox.currentText())
        self.neural_records[current_stream_id] = nrecord
        if nrecord.shape[0] > self.length:
            self.length = nrecord.shape[0]
        self.plot_neural_record()

    def _reset_neural_record(self):
        print("reset")
        pass

    def plot_neural_record(self):
        id = int(self.trace_stream_combobox.currentText())
        current_neural_record = self.neural_records[id]
        self.trace_view.set_data(id, current_neural_record.data)

    def update_streams(self):
        annot = self.state["annot"]
        if annot is not None and self.trace_stream_combobox.count() == 0:
            id_list = [str(k) for k in annot.get_streams().keys()]
            self.trace_stream_combobox.addItems(id_list)
        elif annot is None:
            self.trace_stream_combobox.clear()

    def _set_frame_stick(self, frame):
        self.trace_view.update_frame_stick(frame)

    def _update_space(self, value):
        for id, nrecord in self.neural_records.items():
            nrecord.update_space(value)
            self.trace_view.set_data(id, nrecord.data)
        self.trace_view.refresh_plot(self.trace_stream_combobox.currentText())

    def _set_viewbox(self):
        checked = self.full_trace_push_button.isChecked()
        if checked:
            xleft, xright = self.state["slider_box"]
            self.trace_view.setXRange(xleft, xright)
        else:
            self.trace_view.setXRange(0, self.length)

    def _set_view_button_text(self, checked):
        if checked:
            self.full_trace_push_button.setText("Window")
        else:
            self.full_trace_push_button.setText("Full trace")

    def _cluster_neural(self):
        current_stream_id = int(self.trace_stream_combobox.currentText())
        nrecord = self.neural_records[current_stream_id]
        nrecord.cluster()
        self.trace_view.set_data(current_stream_id, nrecord.data)