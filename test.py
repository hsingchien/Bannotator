from PySide6.QtWidgets import QVBoxLayout, QWidget, QApplication
from widgets import TrackBar
from PySide6.QtCore import Qt
app = QApplication()
data = [0, 1, 2, 3, 4]
color_dict = {0: Qt.red, 1: Qt.green, 2: Qt.blue, 3: Qt.yellow, 4: Qt.cyan}

bar_widget = TrackBar(data, color_dict)
layout = QVBoxLayout()
layout.addWidget(bar_widget)

# Set the layout on a visible parent widget
parent_widget = QWidget()
parent_widget.setLayout(layout)

parent_widget.show()
app.exec()

