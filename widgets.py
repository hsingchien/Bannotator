from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QTabWidget,
    QWidget,
    QScrollBar,
    QStyleOptionTabWidgetFrame,
    QStackedLayout,
)
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtCore import Signal, Slot, QSize, Qt
import numpy as np
from pyqtgraph import GraphicsLayoutWidget
from typing import Dict


class PlaySpeedSpinBox(QDoubleSpinBox):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.cutoff_low = -2.0
        self.cutoff_high = 2.0
        self.step_ratio = 10.0

    def stepBy(self, steps: int) -> None:
        if (
            np.ceil(self.value()) == self.cutoff_low
            and steps > 0
            and self.value() < self.cutoff_low - 0.00001
        ):
            return super().setValue(self.cutoff_low)
        if (
            np.floor(self.value()) == self.cutoff_high
            and steps < 0
            and self.value() > self.cutoff_high + 0.00001
        ):
            return super().setValue(self.cutoff_high)

        if (self.value() >= self.cutoff_high and steps > 0) or (
            self.value() <= self.cutoff_low and steps < 0
        ):
            return super().stepBy(steps * self.step_ratio)
        elif (self.value() >= self.cutoff_high + 1 and steps < 0) or (
            self.value() <= self.cutoff_low - 1 and steps > 0
        ):
            return super().stepBy(steps * self.step_ratio)
        else:
            return super().stepBy(steps)


class VideoScrollBar(QScrollBar):
    @Slot(int)
    def changePageStep(self, pagestep):
        self.setPageStep(pagestep)


class TrackPlotView(GraphicsLayoutWidget):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)


class TrackBar(QWidget):
    def __init__(self, data: np.ndarray = None, color_dict: Dict = None, parent=None):
        super().__init__(parent)
        self.data = data
        self.color_dict = color_dict

    def set_data(self, data: np.ndarray):
        self.data = data
        if self.color_dict:
            self.update()

    def set_color_dict(self, color_dict: Dict = None):
        self.color_dict = color_dict
        if self.data:
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bar_height = self.height()
        bar_width = self.width() / len(self.data)

        for i in range(len(self.data)):
            value = self.data[i]
            color = self.color_dict[value]
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(i * bar_width, 0, bar_width, bar_height)
        painter.end()


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentChanged.connect(self.updateGeometry)

    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return self.sizeHint()

    def sizeHint(self):
        lc = QSize(0, 0)
        rc = QSize(0, 0)
        opt = QStyleOptionTabWidgetFrame()
        self.initStyleOption(opt)
        if self.cornerWidget(Qt.TopLeftCorner):
            lc = self.cornerWidget(Qt.TopLeftCorner).sizeHint()
        if self.cornerWidget(Qt.TopRightCorner):
            rc = self.cornerWidget(Qt.TopRightCorner).sizeHint()
        layout = self.findChild(QStackedLayout)
        layoutHint = layout.currentWidget().sizeHint()
        tabHint = self.tabBar().sizeHint()
        if self.tabPosition() in (QTabWidget.North, QTabWidget.South):
            size = QSize(
                max(layoutHint.width(), tabHint.width() + rc.width() + lc.width()),
                layoutHint.height()
                + max(rc.height(), max(lc.height(), tabHint.height())),
            )
        else:
            size = QSize(
                layoutHint.width() + max(rc.width(), max(lc.width(), tabHint.width())),
                max(layoutHint.height(), tabHint.height() + rc.height() + lc.height()),
            )
        return size
        # max_width = 0
        # max_height = 0
        # opt = QStyleOptionTabWidgetFrame()
        # self.initStyleOption(opt)
        # for i in range(self.count()):
        #     content_width = self.widget(i).sizeHint().width()
        #     content_height = self.widget(i).sizeHint().height()
        #     max_width = max(max_width, content_width)
        #     max_height = max(max_height, content_height)
        # return QSize(max_width, max_height)
