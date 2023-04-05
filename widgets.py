from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QTabWidget,
    QWidget,
    QStyleOptionTabWidgetFrame,
    QStackedLayout,
    QSlider,
    QGraphicsPixmapItem,
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtGui import QPainter, QPen, QPixmap
from PySide6.QtCore import Slot, QSize, Qt, QEvent, Signal, QPoint
import numpy as np
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

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() in range(
            Qt.Key_0, Qt.Key_9 + 1
        ):
            return True
        else:
            return super().event(event)


class VideoSlider(QSlider):
    @Slot(int, int)
    def changeBoxRange(self, boxstart, boxend):
        self.boxstart = boxstart
        self.boxend = boxend
        self.update()

    def __init__(self, parent, boxstart: int = None, boxend: int = None):
        super().__init__(parent)
        if boxstart is None:
            self.boxstart = self.minimum()
            self.boxend = self.minimum()
        else:
            self.boxstart = boxstart
            self.boxend = boxend

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.boxend and self.boxstart:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 1))
            painter.setRenderHint(QPainter.Antialiasing)
            box_height = self.height()
            bar_width = self.width()
            box_width = (
                bar_width
                * (self.boxend - self.boxstart)
                / (self.maximum() - self.minimum())
            )
            box_start = (
                (self.boxstart - self.minimum())
                / (self.maximum() - self.minimum())
                * self.width()
            )
            painter.drawRect(box_start, 0, box_width, box_height)
            painter.end()


class TrackBar(QWidget):
    def __init__(
        self,
        data: np.ndarray = None,
        color_dict: Dict = None,
        frame_mark: int = None,
        parent=None,
    ):
        super().__init__(parent)
        self.data = data
        self.color_dict = color_dict
        self.frame_mark = frame_mark

    def set_data(self, data: np.ndarray, frame_mark: int):
        self.data = data
        self.frame_mark = frame_mark
        if self.color_dict:
            self.update()

    def set_color_dict(self, color_dict: Dict = None):
        self.color_dict = color_dict
        if self.data is not None:
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
            if i == self.frame_mark:
                painter.drawRect(i * bar_width, 0, bar_width, bar_height)
            else:
                painter.drawRect(
                    i * bar_width, 0.2 * bar_height, bar_width, 0.6 * bar_height
                )
        painter.end()


class TabWidget(QTabWidget):
    # Auto-resizing tab
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


class BehavVideoView(QGraphicsView):
    frame_updated = Signal()

    def __init__(self, parent=None, background="default"):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setScene(QGraphicsScene())
        self.pixItem = QGraphicsPixmapItem()
        self.scene().addItem(self.pixItem)
        self.scene().sceneRectChanged.connect(self.fitPixItem)


    @Slot()
    def updatePixmap(self, new_pixmap):
        if isinstance(new_pixmap, QPixmap):
            self.pixItem.setPixmap(new_pixmap)
            self.frame_updated.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.pixItem, aspectRadioMode=Qt.KeepAspectRatio)

    def fitPixItem(self, srect=None):
        self.fitInView(self.pixItem, aspectRadioMode=Qt.KeepAspectRatio)

