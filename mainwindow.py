from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt
from state import GuiState
from video import BehavVideo
from data import Annotation
from dataview import (
    BehaviorTableModel,
    StreamTableModel,
    GenericTableView,
    StatsTableModel,
)
from widgets import TrackBar
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
        self.state["current_frame"] = self.curframe_spinBox.value() - 1
        self.state["play_speed"] = self.speed_doubleSpinBox.value()
        self.state["track_window"] = self.track_window_spinbox.value()
        self.state["tracks"] = dict()
        # Key = ID, item = TrackBar widget
        self.state["stream_tables"] = dict()
        # Key = ID, item = stream table model

        # Set up UI
        self.bvscene = QGraphicsScene()
        self.vid1_view.setScene(self.bvscene)
        self.video_item = QGraphicsPixmapItem()
        self.bvscene.addItem(self.video_item)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video_update_frame)

        # Set up pushbuttons, spinboxes and other interactable widgets
        self.play_button.clicked.connect(self.play_video)
        self.speed_doubleSpinBox.valueChanged.connect(self.set_play_speed)
        self.video_scrollbar.valueChanged.connect(self.set_frame)
        self.curframe_spinBox.valueChanged.connect(self.set_frame)
        self.track_window_spinbox.valueChanged.connect(self.set_track_window)
        # Connect menu bar actions
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_annotation.triggered.connect(self.open_annotation)
        # Connect state change
        self.state.connect(
            "current_frame",
            [self.go_to_frame, lambda: self.update_gui(["video_ui", "tracks"])],
        )
        self.state.connect(
            "track_window",
            [lambda: self.update_gui(["tracks"])],
        )
        self.state.connect("annot", self.plot_tracks)
        self.state.connect(
            "video",
            [
                lambda: self.go_to_frame(self.state["current_frame"]),
                lambda: self.update_gui(["gui"]),
            ],
        )
        self.state.connect("annot", [lambda: self.update_gui(["gui"])])

    def update_gui(self, topics):
        if "video_ui" in topics:
            self.video_scrollbar.setValue(self.state["current_frame"] + 1)
            self.curframe_spinBox.setValue(self.state["current_frame"] + 1)
        if "tracks" in topics:
            try:
                self.update_tracks()
            except Exception:
                pass
        if "gui" in topics:
            try:
                annot_length = self.state["annot"].get_length()
                self.video_scrollbar.setMaximum(annot_length)
                self.curframe_spinBox.setMaximum(annot_length)
                self.track_window_spinbox.setMaximum(annot_length)
            except Exception:
                self.video_scrollbar.setMaximum(self.state["video"].num_frame())
                self.curframe_spinBox.setMaximum(self.state["video"].num_frame())
                self.track_window_spinbox.setMaximum(self.state["video"].num_frame())

    def set_frame(self, frameN):
        # Called by frame slider and spinbox
        self.state["current_frame"] = frameN - 1

    def set_track_window(self, value):
        self.state["track_window"] = int(value)

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
        self.state["FPS"] = bvideo.frame_rate()
        self.go_to_frame(self.state["current_frame"])
        self.video_scrollbar.setMinimum(1)
        self.curframe_spinBox.setMinimum(1)

    def open_annotation(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        anno_path, _ = fileDialog.getOpenFileName(
            self, caption="Open annotation file", filter="Text files (*.txt)"
        )
        if not anno_path:
            return False
        # Create annotation object
        annotation = Annotation({})
        annotation.construct_from_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        annotation.read_from_file(anno_path)
        annotation.assign_behavior_color()
        self.state["annot"] = annotation
        # Set up table views
        # Set up behavior tableview
        behavior_tablemodel = BehaviorTableModel(
            behav_list=annotation.get_behaviors(),
            properties=["ID", "name", "keybind", "color"],
            state=self.state,
            items=[],
        )
        self.behavior_table.setModel(behavior_tablemodel)
        # Set up Statstableview
        stats_tablemodel = StatsTableModel(
            behav_lists=annotation.get_behaviors(),
            properties=["ID", "name"],
            state=self.state,
            items=[],
        )
        self.stats_table.setModel(stats_tablemodel)
        # self.behavior_table.set_columns_fixed([0, 1, 2, 3])
        streams = annotation.get_streams()
        for ID, stream in streams.items():
            stream_table = StreamTableModel(
                stream=stream, properties=["name", "start", "end"], state=self.state
            )
            stream_table_view = GenericTableView()
            stream_table_view.setModel(stream_table)
            stream_table_view.set_columns_fixed([1, 2])
            self.state["stream_tables"][ID] = stream_table_view
            self.stream_table_layout.addWidget(stream_table_view)
        return True

    def go_to_frame(self, frameN):
        video = self.state["video"]
        if video:
            frame_pixmap = video.get_pixmap(frameN)
            self.video_item.setPixmap(frame_pixmap)
            return True
        else:
            return False

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

    def plot_tracks(self):
        annot = self.state["annot"]
        streams = annot.get_streams()
        current_frame = self.state["current_frame"]
        track_window = self.state["track_window"]
        track_start = current_frame - int(1 / 2 * track_window)
        track_end = current_frame + int(np.ceil(1 / 2 * track_window))
        if track_end == track_start:
            track_end = track_start + 1
        for _, stream in streams.items():
            stream_vect = stream.get_stream_vect()
            color_dict = stream.get_color_dict()
            this_start = track_start
            this_end = track_end
            if this_start < 0:
                this_start = 0
                this_end = this_start + track_window
            if this_end >= stream_vect.size:
                this_end = stream_vect.size
                this_start = this_end - track_window
            window_vect = stream_vect[this_start:this_end]
            track = TrackBar(data=window_vect, color_dict=color_dict)
            self.state["tracks"][stream.ID] = track
            self.track_layout.addWidget(track)

    def update_tracks(self):
        annot = self.state["annot"]
        streams = annot.get_streams()
        current_frame = self.state["current_frame"]
        track_window = self.state["track_window"]

        track_start = current_frame - int(1 / 2 * track_window)
        track_end = current_frame + int(np.ceil(1 / 2 * track_window).item())

        for _, stream in streams.items():
            stream_vect = stream.get_stream_vect()
            this_start = track_start
            this_end = track_end
            if this_start < 0:
                this_start = 0
                this_end = this_start + track_window
            if this_end >= stream_vect.size:
                this_end = stream_vect.size
                this_start = this_end - track_window
            window_vect = stream_vect[this_start:this_end]
            self.state["tracks"][stream.ID].set_data(window_vect)
        return True
