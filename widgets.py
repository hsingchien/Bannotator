import PySide6.QtWidgets
from PySide6 import QtGui
from PySide6.QtCore import Signal, QRectF, Qt
from pyqtgraph import GraphicsView, PlotWidget
import numpy as np
from PySide6.QtGui import QPixmap, QFont


class BvGraphicsView(GraphicsView):
    def __init__(
        self, vid_x: int = None, vid_y: int = None, zoom: float = 1, *args, **kwargs
    ):
        super().__init__(useOpenGL=True, *args, **kwargs)
        # To track the zoom level of the view
        self.current_zoom_level = zoom

        # self.setOptimizationFlags(self.optimizationFlags())

    def zoom(self, zoom_level: float, center=None):
        # self.scale(
        #     sx=new_zoom_level / self.current_zoom_level,
        #     sy=new_zoom_level / self.current_zoom_level,
        #     center=center,
        # )
        # self.current_zoom_level = new_zoom_level
        bounding_width, bounding_height = self.get_bounding_wh()
        zoom_level = zoom_level / 10
        if center is None:
            center_x = 1 / 2 * bounding_width
            center_y = 1 / 2 * bounding_height
        else:
            center_x = center.x()
            center_y = center.y()
        w = bounding_width / zoom_level
        h = bounding_height / zoom_level

        left_margin = min(max(center_x - 1 / 2 * w, 0), bounding_width - w)
        top_margin = min(max(center_y - 1 / 2 * h, 0), bounding_height - h)
        self.setRange(
            QRectF(
                left_margin,
                top_margin,
                w,
                h,
            ),
            padding=0,
        )

    def set_center(self, center):
        if center is None:
            return None
        bounding_width, bounding_height = self.get_bounding_wh()
        w = self.range.width()
        h = self.range.height()
        left_margin = min(max(center.x() - 1 / 2 * w, 0), bounding_width - w)
        top_margin = min(max(center.y() - 1 / 2 * h, 0), bounding_height - h)
        self.setRange(
            QRectF(
                left_margin,
                top_margin,
                w,
                h,
            ),
            padding=0,
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def get_bounding_wh(self):
        # get the biggest width and height of the items
        width = 0
        height = 0
        for item in self.items():
            if item.boundingRect().width() > width:
                width = item.boundingRect().width()
            if item.boundingRect().height() > height:
                height = item.boundingRect().height()
        return (width, height)


class DiscreteSlider(PySide6.QtWidgets.QSlider):
    valueChangedDiscrete = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.emit_discrete_value)

    def emit_discrete_value(self, value):
        min_value = self.minimum()
        max_value = self.maximum()
        value_step = self.singleStep()
        valid_value_list = np.arange(min_value, max_value + value_step, value_step)
        val_select = valid_value_list[np.argmin(np.abs(valid_value_list - value))]
        self.setValue(min(val_select, max_value))
        self.valueChangedDiscrete.emit(min(val_select, max_value))


class TraceAxis(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableAutoRange()


class AboutDialog(PySide6.QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About CScreener")
        self.setFixedSize(300, 200)
        self.setWindowIcon(QtGui.QIcon(":/icon/app_icon"))

        vlayout = PySide6.QtWidgets.QVBoxLayout()
        title_label = PySide6.QtWidgets.QLabel("CScreener")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Helvetica [Cronyx]", 16, QFont.Bold))
        vlayout.addWidget(title_label)

        version_label = PySide6.QtWidgets.QLabel("Ver. 0.1")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Helvetica [Cronyx]", 12))
        vlayout.addWidget(version_label)

        author_label = PySide6.QtWidgets.QLabel("Xingjian Zhang")
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setFont(QFont("Helvetica [Cronyx]", 12))
        vlayout.addWidget(author_label)

        repo_label = PySide6.QtWidgets.QLabel(
            '<a href="https://github.com/hsingchien/CScreener">CScreener Repo</a>'
        )
        repo_label.setFont(QFont("Helvetica [Cronyx]", 12))
        repo_label.setAlignment(Qt.AlignCenter)
        repo_label.setTextFormat(Qt.RichText)
        repo_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        repo_label.setOpenExternalLinks(True)
        vlayout.addWidget(repo_label)

        icon_label = PySide6.QtWidgets.QLabel()
        icon_pixmap = QPixmap(":/icon/app_icon")
        icon_label.setPixmap(icon_pixmap)
        icon_label.setScaledContents(True)
        icon_label.setMaximumSize(180, 180)

        hlayout = PySide6.QtWidgets.QHBoxLayout()
        hlayout.addWidget(icon_label)
        hlayout.addLayout(vlayout)
        self.setLayout(hlayout)


class HotkeyDialog(PySide6.QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hotkey")
        self.setWindowIcon(QtGui.QIcon(":/icon/app_icon"))
        self.setFixedSize(350, 200)

        vlayout = PySide6.QtWidgets.QVBoxLayout()
        title_label = PySide6.QtWidgets.QLabel("HotKeys")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Helvetica [Cronyx]", 12, QFont.Bold))
        vlayout.addWidget(title_label)
        hotkeys = []
        hotkeys.append(PySide6.QtWidgets.QLabel("I\\K - Move up\\down focus cell"))
        hotkeys.append(PySide6.QtWidgets.QLabel("O\\L - Move up\\down companion cell"))
        hotkeys.append(
            PySide6.QtWidgets.QLabel(
                "G\\H - Toggle cell label of focus\\companion cell"
            )
        )
        hotkeys.append(
            PySide6.QtWidgets.QLabel(
                "A\\S\\D\\F - Sort cell table 2 by column 1\\3\\4\\5"
            )
        )

        hotkeys.append(PySide6.QtWidgets.QLabel("B\\N - Jump to max intensity frame of focus\\companion cell"))

        hotkeys.append(
            PySide6.QtWidgets.QLabel("Left arrow\\Right arrow - Previous\\Next frame")
        )

        # hotkey_label.setAlignment(Qt.AlignLeft)
        for hotkey_label in hotkeys:
            hotkey_label.setFont(QFont("Helvetica [Cronyx]", 9))
            hotkey_label.setAlignment(Qt.AlignLeft)
            vlayout.addWidget(hotkey_label)

        self.setLayout(vlayout)
