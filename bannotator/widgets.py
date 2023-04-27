from PySide6.QtWidgets import (
    QMainWindow,
    QDoubleSpinBox,
    QTabWidget,
    QWidget,
    QStyleOptionTabWidgetFrame,
    QStackedLayout,
    QSlider,
    QGraphicsPixmapItem,
    QGraphicsView,
    QGraphicsScene,
    QDockWidget,
    QLabel,
)
from PySide6.QtGui import QPainter, QPen, QPixmap, QColor, QFont, QFontDatabase
from PySide6.QtCore import Slot, QSize, Qt, Signal, QRect
import numpy as np
from typing import Dict


class PlaySpeedSpinBox(QDoubleSpinBox):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self._cutoff_low = -2.0
        self._cutoff_high = 2.0
        self._step_ratio = 10.0
        self.valueChanged.connect(self._verify_value)

    def stepBy(self, steps: int) -> None:
        if (
            np.ceil(self.value()) == self._cutoff_low
            and steps > 0
            and self.value() < self._cutoff_low - 0.00001
        ):
            return super().setValue(self._cutoff_low)
        if (
            np.floor(self.value()) == self._cutoff_high
            and steps < 0
            and self.value() > self._cutoff_high + 0.00001
        ):
            return super().setValue(self._cutoff_high)

        if (self.value() >= self._cutoff_high and steps > 0) or (
            self.value() <= self._cutoff_low and steps < 0
        ):
            return super().stepBy(steps * self._step_ratio)
        elif (self.value() >= self._cutoff_high + 1 and steps < 0) or (
            self.value() <= self._cutoff_low - 1 and steps > 0
        ):
            return super().stepBy(steps * self._step_ratio)
        else:
            return super().stepBy(steps)
    
    def _verify_value(self, val):
        if val > self._cutoff_high or val < self._cutoff_low:
            self.setValue(round(val))

class VideoSlider(QSlider):
    @Slot(int, int)
    def changeBoxRange(self, boxstart, boxend):
        self.boxstart = boxstart
        self.boxend = boxend
        self.update()

    def __init__(self, parent, boxstart=None, boxend=None):
        super().__init__(parent)
        if boxstart is not None and boxend is not None:
            self.boxstart = boxstart
            self.boxend = boxend
        else:
            self.boxstart = None
            self.boxend = None
        self.track_data = None
        self.update_track_flag = False
        self.color_dict = None
        self.pixmap_bg = None

    def paintEvent(self, event):
        if self.update_track_flag:
            self.draw_pixmap_bg()

        if self.pixmap_bg is not None:
            painter = QPainter(self)
            painter.drawPixmap(
                QRect(3, 0, self.width() - 6, self.height()), self.pixmap_bg
            )
            painter.end()

        if self.boxend and self.boxstart:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 2))
            painter.setRenderHint(QPainter.Antialiasing)
            box_height = self.height()
            bar_width = self.width() - 6
            box_width = (
                bar_width
                * (self.boxend - self.boxstart)
                / (self.maximum() - self.minimum())
            )
            box_start = (
                (self.boxstart - self.minimum())
                / (self.maximum() - self.minimum())
                * bar_width
            )
            painter.drawRect(box_start + 3, 0, box_width, box_height)
            painter.end()

        super().paintEvent(event)

    def clear_track(self):
        self.boxstart = None
        self.boxend = None
        self.track_data = None
        self.update_track_flag = False
        self.color_dict = None
        self.pixmap_bg = None
        self.update()

    def set_track_data(self, new_track_data):
        self.track_data = new_track_data
        self.update_track_flag = True
        self.update()

    def set_color_dict(self, color_dict):
        self.color_dict = color_dict
        self.update_track_flag = True
        self.update()

    def set_color_track(self, new_track_data, new_color_dict):
        self.track_data = new_track_data
        self.color_dict = new_color_dict
        self.update_track_flag = True
        self.update()

    def draw_pixmap_bg(self):
        if self.update_track_flag and self.track_data is not None:
            self.pixmap_bg = QPixmap(self.width() - 6, self.height())
            painter = QPainter(self.pixmap_bg)
            painter.setRenderHint(QPainter.Antialiasing)

            bar_height = self.height()
            bar_width = (self.width() - 6) / len(self.track_data)

            for i in range(len(self.track_data)):
                value = self.track_data[i]
                color = self.color_dict[value]
                painter.setBrush(color)
                painter.setPen(color)
                painter.drawRect(i * bar_width, 0, bar_width, bar_height)

            painter.end()
            self.update_track_flag = False

    def update_track_bg(self):
        self.update_track_flag = True
        self.update()

    def resizeEvent(self, event):
        if self.track_data is not None:
            self.update_track_flag = True
        return super().resizeEvent(event)


class TrackBar(QWidget):
    def __init__(
        self,
        data: np.ndarray = None,
        color_dict: Dict = None,
        frame_mark: int = None,
        slider_box=[],
        min_height = 8,
        use_pixmap=False,
        full_track_flag=False,
        parent=None,
    ):
        super().__init__(parent)
        self.setMinimumHeight(min_height)
        self.full_data = data
        self.color_dict = color_dict
        self.selected = False
        self.slider_box = slider_box
        self.frame_mark = frame_mark
        self.redraw_track_flag = False
        self.use_pixmap = use_pixmap
        self.pixmap = None
        self.full_track_flag = full_track_flag

        if not self.full_track_flag and self.slider_box:
            # Only draw the content in the slider box
            self.data = self.full_data[self.slider_box[0] : self.slider_box[1]]
        else:
            # Draw the whole track
            self.data = self.full_data

        if use_pixmap:
            self.draw_pixmap_bg()

    def set_data(self, data: np.ndarray):
        self.full_data = data
        if not self.full_track_flag and self.slider_box:
            self.data = self.full_data[self.slider_box[0] : self.slider_box[1]]
        else:
            self.data = self.full_data

        # Update the widget after data is changed
        if self.use_pixmap:
            # Set redraw pixmap flag
            self.redraw_track_flag = True
        self.update()

    def set_color_dict(self, color_dict: Dict = None):
        self.color_dict = color_dict
        if self.use_pixmap:
            self.redraw_track_flag = True
        self.update()

    def set_frame_mark(self, new_frame_mark=None):
        # Only update frame mark rect
        old_frame_mark = self.frame_mark
        if old_frame_mark == new_frame_mark:
            return False

        if self.use_pixmap:
            self.frame_mark = new_frame_mark
            self.update()
        else:
            bar_height = self.height()
            bar_width = self.width() / len(self.data)
            if not self.full_track_flag:
                # The position of the frame mark is relative to the beginning of the data
                old_frame_mark -= self.slider_box[0]
            self.frame_mark = new_frame_mark

            if not self.full_track_flag:
                new_frame_mark -= self.slider_box[0]
            self.update(
                max(old_frame_mark * bar_width - 10, 0),
                0,
                max(bar_width + 10, 20),
                bar_height,
            )
            self.update(
                max(new_frame_mark * bar_width - 10, 0),
                0,
                max(bar_width + 10, 20),
                bar_height,
            )

    def set_slider_box(self, new_slider_box=[]):
        self.slider_box = new_slider_box
        if not self.full_track_flag:
            self.data = self.full_data[new_slider_box[0] : new_slider_box[1]]
            if self.use_pixmap:
                self.redraw_track_flag = True
        self.update()

    def draw_pixmap_bg(self):
        if self.data is not None:
            self.pixmap = QPixmap(self.width(), self.height())
            painter = QPainter(self.pixmap)
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
            self.redraw_track_flag = False

    def paintEvent(self, event):
        bar_height = self.height()
        bar_width = self.width() / len(self.data)
        if not self.full_track_flag:
            frame_mark = self.frame_mark - self.slider_box[0]
        else:
            frame_mark = self.frame_mark
        # Full length track use pixmap to improve performance
        if self.redraw_track_flag and self.use_pixmap:
            self.draw_pixmap_bg()
        if self.pixmap is not None:
            # Make colored track pixmap
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawPixmap(QRect(0, 0, self.width(), self.height()), self.pixmap)
            # Mark the current frame with black line
            painter.setPen(QPen(Qt.black, 2))
            painter.drawRect(frame_mark * bar_width, 0, bar_width, bar_height)
            # Mark the slider box, if full track flag is true
            if self.full_track_flag:
                painter.drawRect(
                    self.slider_box[0] * bar_width,
                    0,
                    (self.slider_box[1] - self.slider_box[0]) * bar_width,
                    bar_height,
                )
            if self.selected:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor("#C7038A"), 2))
                painter.drawRect(0, 0, self.width(), bar_height)
            painter.end()

        else:
            # Dyanamically update the event rect area
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            paint_rect = event.rect()
            start_index = int(paint_rect.x() / bar_width)
            end_index = start_index + int(np.ceil(paint_rect.width() / bar_width))
            for i in range(start_index - 1, end_index + 1):
                if i >= len(self.data):
                    break
                if i < 0:
                    continue
                value = self.data[i]
                color = self.color_dict[value]
                painter.setBrush(color)
                painter.setPen(color)

                if i == frame_mark:
                    painter.drawRect(i * bar_width, 0, bar_width, bar_height)
                else:
                    painter.drawRect(
                        i * bar_width, 0.2 * bar_height, bar_width, 0.6 * bar_height
                    )
            if self.full_track_flag:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(Qt.black, 2))
                painter.drawRect(
                    self.slider_box[0] * bar_width,
                    0,
                    (self.slider_box[1] - self.slider_box[0]) * bar_width,
                    bar_height,
                )
            if self.selected:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(QColor("#C7038A"), 2))
                painter.drawRect(0, 0.2 * bar_height, self.width(), 0.6 * bar_height)

            painter.end()

    def set_selected(self, selected: bool = False):
        self.selected = selected
        self.update()

    def resizeEvent(self, event):
        if self.use_pixmap:
            self.redraw_track_flag = True

        return super().resizeEvent(event)


class DockWidget(QDockWidget):
    closed = Signal(bool)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit(False)


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
        self.scene().setBackgroundBrush(QColor("#595959"))
        self.pixItem = QGraphicsPixmapItem()
        pixmap = QPixmap()
        pixmap.load(":/bg.png")
        self.pixItem.setPixmap(pixmap)
        self.scene().addItem(self.pixItem)
        # self.scene().sceneRectChanged.connect(self.fitPixItem)

    @Slot()
    def updatePixmap(self, new_pixmap):
        self.pixItem.setPixmap(new_pixmap)
        self.frame_updated.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitPixItem()

    def fitPixItem(self):
        self.scene().setSceneRect(self.pixItem.boundingRect())
        self.setAlignment(Qt.AlignCenter)
        self.fitInView(self.scene().sceneRect(), aspectRadioMode=Qt.KeepAspectRatio)

    def clear_pixmap(self):
        pixmap = QPixmap()
        pixmap.load(":/bg.png")
        self.pixItem.setPixmap(pixmap)
        self.fitPixItem()


class BehavLabel(QLabel):
    def __init__(self, behav=None):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Helvetica [Cronyx]", 16, QFont.Bold))
        self._selected = False
        self.behavior = behav
        behav.name_changed.connect(self.update_text)
        behav.color_changed.connect(self.update_text)
        self.update_text()

    @Slot()
    def set_behavior(self, new_behavior):
        self.behavior = new_behavior
        new_behavior.name_changed.connect(self.update_text)
        new_behavior.color_changed.connect(self.update_text)
        self.update_text()

    def set_selected(self, selected):
        self._selected = selected
        self.update_text()

    def update_text(self):
        if self._selected:
            bname = "[" + self.behavior.name + "]"
        else:
            bname = self.behavior.name
        self.setText(bname)
        self.setStyleSheet("color: {0}".format(self.behavior.color))


class AnnotatorMainWindow(QMainWindow):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
