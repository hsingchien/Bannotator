from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsPixmapItem,
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from state import GuiState
from video import BehavVideo
from data import Annotation
from dataview import BehaviorTableModel, StreamTableModel
import numpy as np
import pyqtgraph as pg


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Initialize states
        self.state = GuiState()
        self.state["video"] = None
        self.state["annot"] = None
        self.state["FPS"] = None
        self.state["current_frame"] = None
        self.state["play_speed"] = self.speed_doubleSpinBox.value()
        # Set up UI
        self.bvscene = QGraphicsScene()
        self.vid1_view.setScene(self.bvscene)
        self.video_item = QGraphicsPixmapItem()
        self.bvscene.addItem(self.video_item)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video_update_frame)

        # Set up pushbuttons and spinboxes
        self.play_button.clicked.connect(self.play_video)
        self.speed_doubleSpinBox.valueChanged.connect(self.set_play_speed)
        self.video_scrollbar.valueChanged.connect(self.set_frame)
        self.curframe_spinBox.valueChanged.connect(self.set_frame)
        # Connect menu bar actions
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_annotation.triggered.connect(self.open_annotation)
        # Connect state change
        self.state.connect(
            "current_frame", [self.go_to_frame, lambda: self.update_gui(["video_ui"])]
        )

        # self.state.connect("video", )

    def update_gui(self, topics):
        if "video_ui" in topics:
            self.video_scrollbar.setValue(self.state["current_frame"] + 1)
            self.curframe_spinBox.setValue(self.state["current_frame"] + 1)

    def set_frame(self, frameN):
        # Called by frame slider and spinbox
        self.state["current_frame"] = frameN - 1

    def open_video(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        video_path, _ = fileDialog.getOpenFileName(
            self,
            caption="Open single behavior video",
            filter="Video files (*.avi *.mp4 *.flv *.flv *.mkv)",
        )
        if not video_path:
            return False
        bvideo = BehavVideo(video_path, self)
        self.state["video"] = bvideo
        self.state["current_frame"] = 0
        self.state["FPS"] = bvideo.frame_rate()
        self.video_scrollbar.setMinimum(1)
        self.video_scrollbar.setMaximum(bvideo.num_frame())
        self.curframe_spinBox.setMinimum(1)
        self.curframe_spinBox.setMaximum(bvideo.num_frame())

    def open_annotation(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        anno_path, _ = fileDialog.getOpenFileName(
            self, caption="Open annotation file", filter="Text files (*.txt)"
        )
        if not anno_path:
            return False
        annotation = Annotation({})
        annotation.construct_from_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        annotation.read_from_file(anno_path)
        self.state["annot"] = annotation
        behavior_tablemodel = BehaviorTableModel(annotation.get_behaviors(), self.state)
        self.behavior_table.setModel(behavior_tablemodel)
        stream_tablemodel = StreamTableModel(annotation, self.state)
        self.stream_table.setModel(stream_tablemodel)
        return True

    def go_to_frame(self, frameN):
        video = self.state["video"]
        frame_pixmap = video.get_pixmap(frameN)
        self.video_item.setPixmap(frame_pixmap)

    def play_video_update_frame(self):
        if abs(self.state["play_speed"] - 0.00) > 2.0001:
            next_frame = self.state["current_frame"] + 1 * np.round(
                self.state["play_speed"]
            )
        elif abs(self.state["play_speed"] - 0.00) > 0.0001:
            next_frame = self.state["current_frame"] + 1 * np.sign(
                self.state["play_speed"]
            )

        if next_frame < self.state["video"].num_frame() and next_frame > -1:
            self.state["current_frame"] = next_frame
            return True
        elif next_frame >= self.state["video"].num_frame():
            self.state["current_frame"] = self.state["video"].num_frame() - 1
            self.timer.stop()
        elif next_frame <= 0:
            self.state["current_frame"] = 0
            self.timer.stop()
        else:
            return False

    def play_video(self):
        if abs(self.state["play_speed"] - 0.00) > 2.0001:
            # If playspeed faster than 2.0, then play at original FPS
            self.timer.start(self.state["FPS"])
        elif abs(self.state["play_speed"] - 0.00) > 0.0001:
            # If playspeed slower than 2.0, play at multiplied FPS
            self.timer.start(1000 / (self.state["FPS"] * abs(self.state["play_speed"])))
        else:
            self.timer.stop()

    def set_play_speed(self, value):
        self.state["play_speed"] = value
        if self.timer.isActive():
            self.play_video()
        else:
            return True
