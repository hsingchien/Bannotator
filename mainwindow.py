from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QAbstractItemView,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)
from PySide6.QtCore import QTimer, Qt, QEvent
from state import GuiState
from video import BehavVideo
from data import Annotation
from dataview import (
    BehaviorTableModel,
    StreamTableModel,
    GenericTableView,
    StatsTableModel,
)
from widgets import TrackBar, BehavVideoView
import numpy as np


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Initialize states
        self.state = GuiState()
        self.state["video"] = 0
        self.state["video_layout"] = self.video_layout_comboBox.currentText()
        self.state["annot"] = None
        self.state["FPS"] = None
        self.state["current_frame"] = self.curframe_spinBox.value() - 1
        self.state["play_speed"] = self.speed_doubleSpinBox.value()
        self.state["track_window"] = self.track_window_spinbox.value()
        self.state["slider_box"] = [None, None]
        self.state["current_stream"] = None

        # Container for dynamically generated widgets
        self.tracks = dict()
        self.full_tracks = dict()
        # Key = ID, item = TrackBar widget
        self.stream_tables = dict()
        # Key = ID, item = stream table model

        # Group video viewers into list
        self.vid_views = [self.vid1_view]
        self.vids = []
        # Set up timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video_update_frame)

        # Set up pushbuttons, spinboxes and other interactable widgets
        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.timer.stop)
        self.speed_doubleSpinBox.valueChanged.connect(self.set_play_speed)
        self.video_slider.valueChanged.connect(self.set_frame)
        self.curframe_spinBox.valueChanged.connect(self.set_frame)
        self.track_window_spinbox.valueChanged.connect(self.set_track_window)
        self.video_layout_comboBox.currentTextChanged.connect(self.set_video_layout)
        # Connect menu bar actions
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionOpen_annotation.triggered.connect(self.open_annotation)
        self.actionSave_annotation.triggered.connect(self.save_annotation)
        self.actionSave_config.triggered.connect(self.save_config)
        self.actionFull_annotation.toggled.connect(
            lambda: self.update_gui(["dock_widgets"])
        )
        self.actionBehavior_table.toggled.connect(
            lambda: self.update_gui(["dock_widgets"])
        )
        self.actionEpoch_table.toggled.connect(
            lambda: self.update_gui(["dock_widgets"])
        )
        self.behav_table_dock.visibilityChanged.connect(
            self.actionBehavior_table.setChecked
        )
        self.epoch_dock.visibilityChanged.connect(self.actionEpoch_table.setChecked)
        self.tracks_dock.visibilityChanged.connect(
            self.actionFull_annotation.setChecked
        )
        # Connect state change
        self.state.connect(
            "current_frame",
            [
                self.go_to_frame,
                self.update_slider_box,
                lambda: self.update_gui(["video_ui"]),
            ],
        )
        self.state.connect(
            "track_window",
            [self.update_slider_box],
        )
        self.state.connect("slider_box", [lambda: self.update_gui(["video_ui"])])
        self.state.connect(
            "annot", [self.update_slider_box, lambda: self.update_gui(["gui"])]
        )
        self.state.connect(
            "video",
            [
                lambda: self.go_to_frame(self.state["current_frame"]),
                lambda: self.update_gui(["gui"]),
            ],
        )
        self.state.connect("video_layout", [lambda: self.update_gui(["video_layout"])])
        self.state.connect("current_stream", [lambda: self.update_gui(["tracks"])])

    def update_gui(self, topics):
        if "video_ui" in topics:
            self.video_slider.setValue(self.state["current_frame"] + 1)
            self.curframe_spinBox.setValue(self.state["current_frame"] + 1)
            self.video_slider.changeBoxRange(
                self.state["slider_box"][0] + 1, self.state["slider_box"][1] + 1
            )  # "slider_box" index from 0, video_slider index from 1
        if "tracks" in topics:
            for _, stream in self.state["annot"].get_streams().items():
                if self.state["current_stream"] is stream:
                    self.tracks[stream.ID].set_selected(True)
                else:
                    self.tracks[stream.ID].set_selected(False)
            # Update background of the slider to be the current stream
            self.video_slider.set_color_track(
                self.state["current_stream"].get_stream_vect(),
                self.state["current_stream"].get_color_dict(),
            )

        if "gui" in topics:
            # "gui" includes all the elements update that do not happen frequently
            # Update range of spinboxes and slider
            if self.state["annot"]:
                annot_length = self.state["annot"].get_length()
                self.video_slider.setMaximum(annot_length)
                self.curframe_spinBox.setMaximum(annot_length)
                self.track_window_spinbox.setMaximum(annot_length)
            elif self.state["video"] > 0:
                self.video_slider.setMaximum(self.vids[0].num_frame())
                self.curframe_spinBox.setMaximum(self.vids[0].num_frame())
                self.track_window_spinbox.setMaximum(self.vids[0].num_frame())
            # Update the video layout combobox
            if (
                self.state["video"] > 2
                and self.video_layout_comboBox.findText("Grid") == -1
            ):
                self.video_layout_comboBox.addItem("Grid")
            elif (
                self.state["video"] <= 2
                and self.video_layout_comboBox.currentText() != "Grid"
            ):
                self.video_layout_comboBox.removeItem(
                    self.video_layout_comboBox.findText("Grid")
                )
            elif (
                self.state["video"] <= 2
                and self.video_layout_comboBox.currentText() == "Grid"
            ):
                self.video_layout_comboBox.setCurrentText("Side by Side")
                self.video_layout_comboBox.removeItem(
                    self.video_layout_comboBox.findText("Grid")
                )

        if "tables" in topics:
            # Repaint all tables
            self.behavior_table.repaint_table()
            self.stats_table.repaint_table()
            for _, table in self.stream_tables.items():
                table.repaint_table()

        if "video_layout" in topics:
            # Convert video layout
            current_layout = self.video_layout
            index = self.display_layout.indexOf(current_layout)
            stretch_factor = self.display_layout.stretch(index)
            if self.state["video_layout"] == "Side by Side":
                new_layout = QHBoxLayout()
                for vid in self.vid_views:
                    new_layout.addWidget(vid)
            if self.state["video_layout"] == "Stacked":
                new_layout = QVBoxLayout()
                for vid in self.vid_views:
                    new_layout.addWidget(vid)

            if self.state["video_layout"] == "Grid":
                new_layout = QGridLayout()
                n_row = np.floor(np.sqrt(self.state["video"]))
                n_col = np.ceil(self.state["video"] / n_row)
                for i, vid in enumerate(self.vid_views):
                    new_layout.addWidget(vid, i // n_col, i % n_col)
            self.video_layout = new_layout
            self.display_layout.removeItem(current_layout)
            self.display_layout.insertLayout(index, new_layout, stretch_factor)

        if "dock_widgets" in topics:
            self.behav_table_dock.setVisible(self.actionBehavior_table.isChecked())
            self.epoch_dock.setVisible(self.actionEpoch_table.isChecked())
            self.tracks_dock.setVisible(self.actionFull_annotation.isChecked())

    def set_frame(self, frameN):
        # Called by frame slider and spinbox
        self.state["current_frame"] = frameN - 1

    def set_track_window(self, value):
        self.state["track_window"] = value

    def update_slider_box(self):
        try:
            annot = self.state["annot"]
            current_frame = self.state["current_frame"]
            track_window = self.state["track_window"]
            track_start = current_frame - int(np.floor(1 / 2 * track_window))
            track_end = current_frame + int(np.ceil(1 / 2 * track_window))
            annot_len = annot.get_length()
            this_start = track_start
            this_end = track_end
            # Calculate start and end of track display
            if this_start < 0:
                this_start = 0
                this_end = this_start + track_window
            if this_end >= annot_len:
                this_end = annot_len
                this_start = this_end - track_window
            if track_end == track_start:
                track_end = track_start + 1
            self.state["slider_box"] = [int(this_start), int(this_end)]
        except Exception:
            pass

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
        bvideo = BehavVideo(video_path)
        self.vids.append(bvideo)
        self.state["video"] += 1
        if self.state["video"] == 1:
            bvideo.new_frame_fetched.connect(self.vid_views[0].updatePixmap)
            self.state["FPS"] = bvideo.frame_rate()
        else:
            new_view = BehavVideoView()
            bvideo.new_frame_fetched.connect(new_view.updatePixmap)
            self.vid_views.append(new_view)
            if self.state["video_layout"] != "Grid":
                self.video_layout.addWidget(new_view)
            else:
                n_row = np.floor(np.sqrt(self.state["video"]))
                n_col = np.ceil(self.state["video"] / n_row)
                if (
                    n_row == self.video_layout.rowCount()
                    and n_col == self.video_layout.columnCount()
                ):
                    self.video_layout.addWidget(
                        new_view,
                        (self.state["video"] - 1) // n_col,
                        (self.state["video"] - 1) % n_col,
                    )
                else:
                    # Rebuild the gridlayout
                    self.update_gui(["video_layout"])
            new_view.show()

        self.video_slider.setMinimum(1)
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
        self.behavior_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.behavior_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.behavior_table.model().dataChanged.connect(
            self.behavior_table.clearSelection
        )
        annotation.content_changed.connect(self.behavior_table.repaint_table)
        # Set up Statstableview
        stats_tablemodel = StatsTableModel(
            behav_lists=annotation.get_behaviors(),
            properties=["ID", "name"],
            state=self.state,
            items=[],
        )
        self.stats_table.setModel(stats_tablemodel)
        annotation.content_changed.connect(self.stats_table.repaint_table)
        # Set up epochs table for each stream
        streams = annotation.get_streams()
        for ID, stream in streams.items():
            stream_table = StreamTableModel(
                stream=stream, properties=["name", "start", "end"], state=self.state
            )
            stream_table_view = GenericTableView()
            stream_table_view.setModel(stream_table)
            stream_table_view.set_columns_fixed([1, 2])
            stream.data_changed.connect(stream_table_view.repaint_table)
            self.stream_tables[ID] = stream_table_view
            self.stream_table_layout.addWidget(stream_table_view)
        self.update_slider_box()
        self.plot_tracks()
        # Set the first stream as current stream
        IDs = sorted(list(streams.keys()))
        self.state["current_stream"] = streams[IDs[0]]

        return True

    def save_annotation(self):
        self.state["annot"].saved_in_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        self.statusbar.showMessage("Saving annotation...", 0)
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save Annotation", "annotation.txt", "text Files (*.txt)"
        )
        if not filename:
            return False
        self.statusbar.clearMessage()
        return self.state["annot"].save_to_file(filename)

    def save_config(self):
        self.state["annot"].saved_in_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        self.statusbar.showMessage("Saving annotation...", 0)
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save Configuration", "config.txt", "text Files (*.txt)"
        )
        if not filename:
            return False
        self.statusbar.clearMessage()
        return self.state["annot"].save_config_to_file(filename)

    def go_to_frame(self, frameN):
        videos = self.vids
        if videos:
            for video in videos:
                video.get_pixmap(frameN)
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

        if next_frame < self.vids[0].num_frame() and next_frame > -1:
            self.state["current_frame"] = next_frame
            return True
        elif next_frame >= self.vids[0].num_frame():
            self.state["current_frame"] = self.vids[0].num_frame() - 1
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
        this_start, this_end = self.state["slider_box"]
        annot = self.state["annot"]
        streams = annot.get_streams()
        # Generate tracks for streams
        for _, stream in streams.items():
            # Make mainwindow track widgets
            stream_vect = stream.get_stream_vect()
            color_dict = stream.get_color_dict()
            track = TrackBar(
                stream_vect,
                color_dict,
                self.state["current_frame"],
                self.state["slider_box"],
                False,
                False,
            )
            if self.state["current_stream"] is stream:
                track.set_selected(True)
            else:
                track.set_selected(False)
            self.tracks[stream.ID] = track
            stream.data_changed.connect(track.set_data)
            stream.color_changed.connect(track.set_color_dict)
            self.state.connect("current_frame", track.set_frame_mark)
            self.state.connect("slider_box", track.set_slider_box)
            self.track_layout.addWidget(track)
            # Make full length track widgets
            self.tracks_dock.resize(self.width(), 100)
            full_track = TrackBar(
                stream_vect,
                color_dict,
                self.state["current_frame"],
                self.state["slider_box"],
                True,
                True,
            )
            self.state.connect("current_frame", full_track.set_frame_mark)
            self.state.connect("slider_box", full_track.set_slider_box)
            stream.data_changed.connect(full_track.set_data)
            stream.color_changed.connect(full_track.set_color_dict)
            self.full_tracks_layout.addWidget(full_track)
            # Also connect stream content change signals to video slider track update
            stream.data_changed.connect(self.video_slider.set_track_data)
            stream.color_changed.connect(self.video_slider.set_color_dict)

    def change_current_behavior(self, keypressed: str = None):
        cur_idx = self.state["current_frame"]
        cur_stream = self.state["current_stream"]
        if cur_stream is None:
            return False
        else:
            cur_stream.set_behavior(cur_idx, keypressed)
            return True

    def assign_current_stream(self, keyint: int):
        keyint = keyint - 49
        if keyint == -1:
            keyint = 9
        skeys = sorted(list(self.state["annot"].get_streams().keys()))
        try:
            skey = skeys[keyint]
            self.state["current_stream"] = self.state["annot"].get_streams()[skey]
            return True
        except Exception:
            return False

    def set_video_layout(self, layout_option):
        self.state["video_layout"] = layout_option

    def eventFilter(self, obj, event):
        if event.type() != QEvent.KeyPress:
            return super().eventFilter(obj, event)
        if self.editing_state():
            return False
        if event.key() in range(Qt.Key_A, Qt.Key_Z + 1):
            # Alphabets
            self.change_current_behavior(event.text().lower())
        if event.key() in range(Qt.Key_0, Qt.Key_9 + 1):
            # Numbers
            try:
                self.assign_current_stream(event.key())
            except Exception:
                pass
        elif event.key() == Qt.Key_QuoteLeft:
            # ` key, rotate current stream
            # Find where the current stream is
            try:
                current_stream_id = self.state["current_stream"].ID
                skeys = sorted(list(self.state["annot"].get_streams().keys()))
                for i in range(len(skeys)):
                    if skeys[i] == current_stream_id:
                        break
                if i == len(skeys) - 1:
                    i = -1
                i += 50
                self.assign_current_stream(i)
            except:
                pass

        elif event.key() == Qt.Key_Minus:
            # - key, move to the previous cut point
            try:
                current_stream = self.state["current_stream"]
                current_frame = self.state["current_frame"]
                current_epoch = current_stream.get_epoch_by_idx(current_frame)
                if current_frame != (current_epoch.start - 1):
                    # Move to the start of the current epoch
                    self.state["current_frame"] = current_epoch.start - 1
                else:
                    # Move to the start of the previous epoch
                    previous_epoch = current_stream.get_epoch_by_idx(current_frame - 1)
                    self.state["current_frame"] = previous_epoch.start - 1
            except Exception:
                pass
        elif event.key() == Qt.Key_Equal:
            # = key, move to next end
            try:
                current_stream = self.state["current_stream"]
                current_frame = self.state["current_frame"]
                current_epoch = current_stream.get_epoch_by_idx(current_frame)
                if current_frame != (current_epoch.end):
                    # Move to the start of the current epoch
                    self.state["current_frame"] = current_epoch.end
                else:
                    # Move to the end of the next epoch
                    next_epoch = current_stream.get_epoch_by_idx(current_frame + 1)
                    self.state["current_frame"] = next_epoch.end
            except Exception:
                pass
        elif event.key() == Qt.Key_Space:
            # Spacebar, toggle play/pause
            try:
                if not self.timer.isActive():
                    self.play_video()
                else:
                    self.timer.stop()
            except:
                pass
        elif event.key() == Qt.Key_Up:
            # UP key, up the playspeed by 1 step
            self.speed_doubleSpinBox.stepBy(1)
        elif event.key() == Qt.Key_Down:
            # DOWN key, down the playspeed by 1 step
            self.speed_doubleSpinBox.stepBy(-1)
        elif event.key() == Qt.Key_Left:
            # LEFT key, previous 1 frame
            self.state["current_frame"] = max(self.state["current_frame"] - 1, 0)
        elif event.key() == Qt.Key_Right:
            # RIGHT key, next 1 frame
            self.state["current_frame"] = min(
                self.state["current_frame"] + 1, self.curframe_spinBox.maximum()
            )
        else:
            return super().eventFilter(obj, event)
        # Stop propagation
        return True

    def editing_state(self):
        # Check focus widgets
        if self.focusWidget() in [
            self.speed_doubleSpinBox,
            self.curframe_spinBox,
            self.track_window_spinbox,
        ]:
            return True
        if self.behavior_table.state() == QAbstractItemView.EditingState:
            return True
        if self.stats_table.state() == QAbstractItemView.EditingState:
            return True
        for _, table in self.stream_tables.items():
            if table.state() == QAbstractItemView.EditingState:
                return True
        return False

    def closeEvent(self, event):
        for video in self.vids:
            video.stop_worker()
            event.accept()
