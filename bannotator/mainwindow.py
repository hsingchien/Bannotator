from bannotator.ui.ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import (
    QFileDialog,
    QAbstractItemView,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt, QEvent
from bannotator.state import GuiState
import bannotator.utility as utt
from bannotator.video import BehavVideo, SeqBehavVideo
from bannotator.data import Annotation
from bannotator.dataview import (
    BehaviorTableModel,
    StreamTableModel,
    GenericTableView,
    StatsTableModel,
    BehavEpochTableModel,
)
from bannotator.dialog import *
from bannotator.widgets import TrackBar, BehavVideoView, BehavLabel, AnnotatorMainWindow
import numpy as np
import os


class MainWindow(AnnotatorMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Annotator")
        self.setWindowIcon(QIcon(":/icon.ico"))
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
        self.dialog_state = False

        # Container for dynamically generated widgets
        # Key = stream ID, item = TrackBar widget
        self.tracks = dict()
        self.full_tracks = dict()
        # Key = stream ID, item = stream QLabel for current behavior
        self.stream_labels = dict()
        # Key = stream ID, item = stream table model
        self.stream_tables = dict()
        # Key = ID, item = behavior epoch table model
        self.behav_epoch_tables = dict()

        # Group video viewers into list
        self.vid_views = [self.vid1_view]
        self.vids = []
        self.vids_stretch_factor = []
        # Set up timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video_update_frame)
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.timeout.connect(self.save_annotation_copy)
        self.auto_save_timer.start(30000)
        # Set up pushbuttons, spinboxes and other interactable widgets
        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.timer.stop)
        self.speed_doubleSpinBox.valueChanged.connect(self.set_play_speed)
        self.video_slider.valueChanged.connect(
            lambda x: self.state.set("current_frame", x - 1)
        )
        self.curframe_spinBox.valueChanged.connect(
            lambda x: self.state.set("current_frame", x - 1)
        )
        self.track_window_spinbox.valueChanged.connect(
            lambda x: self.state.set("track_window", x)
        )
        self.video_layout_comboBox.currentTextChanged.connect(
            lambda x: self.state.set("video_layout", x)
        )

        self.add_behavior_button.clicked.connect(self.add_behavior)
        self.delete_behavior_button.clicked.connect(self.delete_behavior)
        self.add_stream_button.clicked.connect(self.add_stream)
        self.delete_stream_button.clicked.connect(self.delete_stream)
        # Connect menu bar actions
        # File menu
        self.actionReset.triggered.connect(self.reset_app)
        self.actionQuit.triggered.connect(self.close)
        # Video menu
        self.actionOpen_video.triggered.connect(self.open_video)
        self.actionAdd_seq.triggered.connect(self.add_seq)
        # Annotation menu
        self.actionOpen_annotation.triggered.connect(self.open_annotation)
        self.actionSave_annotation.triggered.connect(self.save_annotation)
        self.actionOpen_config.triggered.connect(self.open_config)
        self.actionSave_config.triggered.connect(self.save_config)
        self.actionAuto_save_annotation.toggled.connect(
            lambda x: self.auto_save_timer.start(30000)
            if x
            else self.auto_save_timer.stop()
        )
        self.actionClose_annotation.triggered.connect(self.close_annotation)
        # View menu
        self.actionFull_annotation.toggled.connect(
            lambda: self.update_gui(["view_options"])
        )
        self.actionBehavior_table.toggled.connect(
            lambda: self.update_gui(["view_options"])
        )
        self.actionEpoch_table.toggled.connect(
            lambda: self.update_gui(["view_options"])
        )
        self.behav_table_dock.closed.connect(self.actionBehavior_table.setChecked)
        self.epoch_dock.closed.connect(self.actionEpoch_table.setChecked)
        self.tracks_dock.closed.connect(self.actionFull_annotation.setChecked)

        self.actionTrack_epoch.toggled.connect(
            lambda: self.update_gui(["view_options"])
        )

        # Connect state change
        self.connect_states()

    def connect_states(self):
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
            "annot", [self.setup_table_models, lambda: self.update_gui(["gui"])]
        )
        self.state.connect("video", [lambda: self.update_gui(["video_ui", "gui"])])
        self.state.connect("video_layout", [lambda: self.update_gui(["video_layout"])])
        self.state.connect("current_stream", [lambda: self.update_gui(["tracks"])])

    def update_gui(self, topics):
        if "video_ui" in topics:
            self.video_slider.setValue(self.state["current_frame"] + 1)
            self.curframe_spinBox.setValue(self.state["current_frame"] + 1)
            if self.state["slider_box"][0] is not None:
                self.video_slider.changeBoxRange(
                    self.state["slider_box"][0] + 1, self.state["slider_box"][1] + 1
                )  # "slider_box" index from 0, video_slider index from 1
            # Update time label
            if self.state["FPS"] is not None:
                cur_time = int(self.state["current_frame"] / self.state["FPS"])
                minutes, seconds = divmod(cur_time, 60)
                hours, minutes = divmod(minutes, 60)
                duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                self.time_label.setText(duration)

        if "tracks" in topics:
            # Update tracks highlight and behavior label (selected with a bracket)
            for _, stream in self.state["annot"].get_streams().items():
                if self.state["current_stream"] is stream:
                    self.tracks[stream.ID].set_selected(True)
                    self.stream_labels[stream.ID].set_selected(True)
                else:
                    self.tracks[stream.ID].set_selected(False)
                    self.stream_labels[stream.ID].set_selected(False)
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
            if self.state["annot"] is not None:
                # Enable annotation options
                self.actionSave_annotation.setEnabled(True)
                self.actionSave_config.setEnabled(True)
            else:
                self.actionSave_annotation.setEnabled(False)
                self.actionSave_config.setEnabled(False)
            if self.state["video"] > 0:
                self.actionOpen_config.setEnabled(True)
            else:
                self.actionOpen_config.setEnabled(False)

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

        if "view_options" in topics:
            self.behav_table_dock.setVisible(self.actionBehavior_table.isChecked())
            self.epoch_dock.setVisible(self.actionEpoch_table.isChecked())
            self.tracks_dock.setVisible(self.actionFull_annotation.isChecked())
            # Set the epoch tracking state
            if self.actionTrack_epoch.isChecked() and self.stream_tables:
                for ID, stream in self.state["annot"].get_streams().items():
                    self.stream_tables[ID].connect_scroll()
                    self.behav_epoch_tables[ID].connect_scroll()
                    stream.get_epoch_by_idx(self.state["current_frame"])
            elif self.stream_tables:
                for ID in self.state["annot"].get_streams():
                    self.stream_tables[ID].disconnect_scroll()
                    self.behav_epoch_tables[ID].disconnect_scroll()

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
        valid_video = False
        # Check if the length of the video is significantly different from annotation
        if (
            self.state["annot"]
            and self.state["annot"].get_length() != bvideo.num_frame()
        ):
            warning_dialog = QMessageBox.warning(
                self,
                "Is this the correct video?",
                "The video length does not match the annotation.\nOK to proceed. Cancel to abort.",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                # If user click anything else but OK, reject input
                bvideo.stop_worker()
                return False
            else:
                valid_video = True

        # Check if the video is significantly different from video 0
        if (
            self.state["video"] > 0
            and not valid_video
            and np.abs(bvideo.num_frame() - self.vids[0].num_frame())
            > 0.05 * self.vids[0].num_frame()
        ):
            warning_dialog = QMessageBox.warning(
                self,
                "Is this the correct video?",
                "The video length significantly differs from video 1.\nOK to proceed. Cancel to abort.",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                # If user click anything else but OK, reject input
                bvideo.stop_worker()
                return False
            else:
                valid_video = True

        self.vids.append(bvideo)
        # Set stretch factors
        if self.state["video"] == 0:
            self.vids_stretch_factor = [1]
        else:
            self.vids_stretch_factor.append(
                bvideo.num_frame() / self.vids[0].num_frame()
            )
        # Connect scene
        if self.state["video"] == 0:
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
        # Change state and trigger callbakcs
        self.go_to_frame(self.state["current_frame"])
        self.state["video"] += 1
        self.video_slider.setMinimum(1)
        self.curframe_spinBox.setMinimum(1)

    def add_seq(self):
        self.statusbar.showMessage(
            "Opening .seq file. If this file is compressed (jpeg), it may take a few minutes...",
            0,
        )
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        video_path, _ = fileDialog.getOpenFileName(
            self,
            caption="Open single seq behavior video",
            filter="Video files (*.seq)",
        )
        if not video_path:
            return False
        self.statusbar.clearMessage()
        bvideo = SeqBehavVideo(video_path, self.statusbar)
        valid_video = False
        # Check if the length of the video is significantly different from annotation
        if (
            self.state["annot"]
            and self.state["annot"].get_length() != bvideo.num_frame()
        ):
            warning_dialog = QMessageBox.warning(
                self,
                "Is this the correct video?",
                "The video length does not match the annotation.\nOK to proceed. Cancel to abort.",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                # If user click anything else but OK, reject input
                bvideo.stop_worker()
                return False
            else:
                valid_video = True
        # Check if the video is significantly different from video 0
        if (
            self.state["video"] > 0
            and not valid_video
            and np.abs(bvideo.num_frame() - self.vids[0].num_frame())
            > 0.05 * self.vids[0].num_frame()
        ):
            warning_dialog = QMessageBox.warning(
                self,
                "Is this the correct video?",
                "The video length significantly differs from video 1.\nOK to proceed. Cancel to abort.",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                # If user click anything else but OK, reject input
                bvideo.stop_worker()
                return False
            else:
                valid_video = True

        # Stretch factor for current video relative to the video 0
        if self.state["video"] == 0:
            self.vids_stretch_factor = [1]
        else:
            self.vids_stretch_factor.append(
                bvideo.num_frame() / self.vids[0].num_frame()
            )
        #
        bvideo.start_frame_fetcher()
        bvideo.run_worker.connect(lambda: self.go_to_frame(self.state["current_frame"]))
        self.vids.append(bvideo)
        if self.state["video"] == 0:
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
        # Refresh the scene
        self.go_to_frame(self.state["current_frame"])
        # Trigger ui updtates
        self.state["video"] += 1
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
        annot_length = annotation.get_length()
        if self.vids and annot_length < self.vids[0].num_frame():
            warning_dialog = QMessageBox.warning(
                self,
                "Is this the correct annotation?",
                "Annotation is shorter than video 1!\nOk to pad with default behavior. Cancel to abort",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                return False
            else:
                annotation.set_length(self.vids[0].num_frame())

        elif self.vids and annot_length > self.vids[0].num_frame():
            # Guide user to shrink the annotation
            self.dialog_state = True
            (from_value, to_value) = TruncateAnnotationDialog(
                annot_length, self.vids[0].num_frame(), parent=self
            ).get_input()
            if from_value is not None:
                annotation.truncate(start=from_value, length=self.vids[0].num_frame())
            else:
                return False
        self.state["annot"] = annotation

    def open_config(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        config_path, _ = fileDialog.getOpenFileName(
            self, caption="Open configuration file", filter="Text files (*.txt)"
        )
        if not config_path:
            return False
        # Create behaviors and empty streams
        annotation = Annotation({})
        annotation.construct_from_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        annotation.read_config_from_file(config_path)
        if self.state["video"] > 0:
            annotation.set_length(self.vids[0].num_frame())
        else:
            annotation.set_length(self.video_slider.maximum())
        annotation.assign_behavior_color()
        self.state["annot"] = annotation

    def setup_table_models(self):
        # Set up table views
        # Set up behavior tableview
        annotation = self.state["annot"]
        if annotation is None:
            return False
        behavior_tablemodel = BehaviorTableModel(
            annotation=annotation,
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
        annotation.content_layout_changed.connect(behavior_tablemodel.change_layout)
        # Set up Statstableview
        stats_tablemodel = StatsTableModel(
            annotation=annotation,
            properties=["ID", "name"],
            state=self.state,
            items=[],
        )
        self.stats_table.setModel(stats_tablemodel)
        annotation.content_changed.connect(self.stats_table.repaint_table)
        annotation.content_layout_changed.connect(stats_tablemodel.change_layout)
        # Connect behavior and stats table to sync the activated row display
        behavior_tablemodel.activated_behavior_changed.connect(
            stats_tablemodel.receive_activate_behavior
        )
        stats_tablemodel.activated_behavior_changed.connect(
            behavior_tablemodel.receive_activate_behavior
        )
        # Set up epochs table for each stream
        streams = annotation.get_streams()
        for _, stream in streams.items():
            self.setup_stream_tables(stream)
            # Emit the cur_epoch signal from the stream after all tables are set up to
            # highlight the current epoch
            stream.get_epoch_by_idx(self.state["current_frame"])

        self.update_slider_box()
        for _, stream in streams.items():
            self.plot_stream_tracks(stream)

        # Set the first stream as current stream
        IDs = sorted(list(streams.keys()))
        self.state["current_stream"] = streams[IDs[0]]

        return True

    def setup_stream_tables(self, stream):
        # Create stream tables
        stream_table = StreamTableModel(
            stream=stream, properties=["name", "start", "end"], state=self.state
        )
        stream_table_view = GenericTableView()
        stream_table_view.setModel(stream_table)
        stream_table_view.set_columns_fixed([1, 2])
        stream.data_changed.connect(stream_table_view.repaint_table)
        stream.epoch_number_changed.connect(stream_table_view.change_layout)
        self.stream_tables[stream.ID] = stream_table_view
        self.stream_table_layout.addWidget(stream_table_view)
        stream_table.jump_to_frame.connect(lambda x: self.state.set("current_frame", x))
        # Create behavior label, add to the full track widget
        behav_label = BehavLabel(
            behav=stream.get_behavior_by_idx(self.state["current_frame"]),
        )
        self.cur_behav_layout.addWidget(behav_label)
        self.stream_labels[stream.ID] = behav_label
        # Connect video slider and frame spinbox to the stream to track the current epoch
        self.state.connect("current_frame", stream.get_epoch_by_idx)
        # get_epoch_by_idx will emit cur_epoch and cur_behavior, which will set the epoch table and behavior label respectively
        stream.cur_behavior_name.connect(behav_label.set_behavior)

        # Scroll to current epoch if action is checked
        if self.actionTrack_epoch.isChecked():
            stream_table_view.connect_scroll()
        # Create empty behavior epoch tables
        behav_epoch_table = BehavEpochTableModel(
            stream=stream, properties=["name", "start", "end"], state=self.state
        )
        self.behavior_table.model().activated_behavior_changed.connect(
            behav_epoch_table.set_behavior
        )
        self.stats_table.model().activated_behavior_changed.connect(
            behav_epoch_table.set_behavior
        )
        behav_epoch_table.jump_to_frame.connect(
            lambda x: self.state.set("current_frame", x)
        )
        behav_epoch_table_view = GenericTableView()
        behav_epoch_table_view.setModel(behav_epoch_table)
        self.behav_epoch_tables[stream.ID] = behav_epoch_table_view
        self.behav_epoch_table_layout.addWidget(behav_epoch_table_view)
        if self.actionTrack_epoch.isChecked():
            behav_epoch_table_view.connect_scroll()

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

    def save_annotation_copy(self):
        try:
            annot_path = self.state["annot"].get_file_path()
            if annot_path is None:
                filename = os.path.join(os.getcwd(), "annotation_backup.txt")
            else:
                filename = annot_path.replace(".txt", "_backup.txt")
            if self.state["annot"].save_to_file(filename, True):
                self.statusbar.clearMessage()
                self.statusbar.showMessage(
                    "Automatically saved annotaion backup.", 1000
                )
        except Exception:
            if self.state["annot"] is not None:
                self.statusbar.clearMessage()
                self.statusbar.showMessage(
                    "Autosave failed! Try manually save the annotation and auto-save will succeed next time.",
                    4000,
                )
            pass

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
            for i, video in enumerate(videos):
                this_frameN = frameN * self.vids_stretch_factor[i]
                video.get_pixmap(int(this_frameN))
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

    def plot_stream_tracks(self, stream):
        # Generate tracks for the stream
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
        # if self.state["current_stream"] is stream:
        #     track.set_selected(True)
        # else:
        #     track.set_selected(False)
        self.tracks[stream.ID] = track
        stream.data_changed.connect(track.set_data)
        stream.color_changed.connect(track.set_color_dict)
        self.state.connect("current_frame", track.set_frame_mark)
        self.state.connect("slider_box", track.set_slider_box)
        self.track_layout.addWidget(track)
        # Make full length track widgets
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
        self.full_tracks[stream.ID] = full_track
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
            cur_stream.get_epoch_by_idx(self.state["current_frame"])
            return True

    def add_behavior(self):
        if self.state["annot"] is None:
            return False
        self.dialog_state = True
        newdialog = AddBehaviorDialog(parent=self, annotation=self.state["annot"])
        name, keybind = newdialog.get_input()
        if name is not None and keybind is not None:
            self.state["annot"].add_behavior(name, keybind)
        self.dialog_state = False

    def add_stream(self):
        if self.state["annot"] is None:
            return False
        self.dialog_state = True
        newdialog = AddStreamDialog(parent=self, annotation=self.state["annot"])
        behavior = newdialog.get_input()
        if behavior is not None:
            new_stream = self.state["annot"].add_stream(behavior)
            self.setup_stream_tables(new_stream)
            self.plot_stream_tracks(new_stream)
            self.dialog_state = False
        else:
            self.dialog_state = False
            return False

    def delete_behavior(self):
        if self.state["annot"] is None:
            return False
        self.dialog_state = True
        newdialog = DeleteBehaviorDialog(parent=self, annotation=self.state["annot"])
        to_del, to_rep = newdialog.get_input()
        if to_del is not None:
            # If behavior_epoch tables are viewing the deleted behavior, set it to replace behavior
            if self.stats_table.model().current_activate_property("name") == to_del:
                self.stats_table.model().set_activate_by_name(to_rep)
            self.state["annot"].delete_behavior(to_del, to_rep)
        else:
            self.dialog_state = False
            return False
        for _, stream in self.state["annot"].get_streams().items():
            stream.get_epoch_by_idx(self.state["current_frame"])
        self.dialog_state = False

    def delete_stream(self):
        if self.state["annot"] is None:
            return False
        self.dialog_state = True
        newdialog = DeleteStreamDialog(parent=self, annotation=self.state["annot"])
        del_id = newdialog.exec()
        if del_id is None:
            self.dialog_state = False
            return False
        if self.state["annot"].num_stream() == 1:
            self.dialog_state = False
            return False
        # Remove tables
        stream_table = self.stream_tables.pop(del_id)
        utt.reset_table(stream_table)
        behav_stream_table = self.behav_epoch_tables.pop(del_id)
        utt.reset_table(behav_stream_table)
        self.stream_table_layout.removeWidget(stream_table)
        self.behav_epoch_table_layout.removeWidget(behav_stream_table)
        # Remove tracks
        full_track = self.full_tracks.pop(del_id)
        track = self.tracks.pop(del_id)
        self.state.disconnect("current_frame", track.set_frame_mark)
        self.state.disconnect("slider_box", track.set_slider_box)
        self.state.disconnect("current_frame", full_track.set_frame_mark)
        self.state.disconnect("slider_box", full_track.set_slider_box)
        stream = self.state["annot"].delete_stream(del_id)
        if self.state["current_stream"] is stream:
            streams = self.state["annot"].get_streams()
            IDs = sorted(list(streams.keys()))
            self.state["current_stream"] = streams[IDs[0]]

        self.full_tracks_layout.removeWidget(full_track)
        self.track_layout.removeWidget(track)
        blabel = self.stream_labels.pop(del_id)
        self.cur_behav_layout.removeWidget(blabel)
        # Delete widgets
        stream_table.deleteLater()
        behav_stream_table.deleteLater()
        full_track.deleteLater()
        track.deleteLater()
        blabel.deleteLater()
        self.state.disconnect("current_frame", stream.get_epoch_by_idx)
        del stream
        self.dialog_state = False
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

    def close_annotation(self, suppress_warning=False):
        # First clear out all the widgets
        if self.state["annot"] is None:
            return False
        self.timer.stop()
        if not suppress_warning:
            warning_dialog = QMessageBox.warning(
                self,
                "Do you want to close annotation?",
                "Make sure to save before closing!",
                QMessageBox.Ok,
                QMessageBox.Cancel,
            )
            if warning_dialog != QMessageBox.Ok:
                return False
        self.video_slider.clear_track()
        utt.clear_layout(self.track_layout)
        utt.clear_layout(self.full_tracks_layout)
        utt.clear_layout(self.cur_behav_layout)
        utt.clear_layout(self.stream_table_layout)
        utt.clear_layout(self.behav_epoch_table_layout)
        utt.reset_table(self.behavior_table)
        utt.reset_table(self.stats_table)
        # Reset connections
        self.state.clear_connections("annot")
        self.state.clear_connections("current_frame")
        self.state.clear_connections("slider_box")
        self.state.clear_connections("current_stream")
        self.state.clear_connections("track_window")
        # Clear containers
        self.tracks.clear()
        self.full_tracks.clear()
        self.stream_labels.clear()
        self.stream_tables.clear()
        self.behav_epoch_tables.clear()
        self.state["annot"] = None
        self.state["slider_box"] = [None, None]
        # Reconnect callbacks
        self.connect_states()

        self.update_gui(["gui"])

    def reset_app(self):
        self.timer.stop()
        warning_dialog = QMessageBox.warning(
            self,
            "Do you want to reset the app",
            "Make sure to save unsaved work!",
            QMessageBox.Ok,
            QMessageBox.Cancel,
        )
        if warning_dialog != QMessageBox.Ok:
            return False
        # Close videos
        self.state["video_layout"] = "Side by Side"
        self.state["video"] = 0
        for vid in self.vids:
            vid.stop_worker()
        while len(self.vid_views) > 1:
            vid_view = self.vid_views.pop(-1)
            self.video_layout.removeWidget(vid_view)
            vid_view.deleteLater()
        self.vid1_view.clear_pixmap()
        self.state.clear_connections("video")
        self.state.clear_connections("video_layout")
        self.state.clear_connections("FPS")
        self.state.clear_connections("play_speed")
        self.state["FPS"] = None
        self.vids_stretch_factor = []
        self.vids.clear()
        self.close_annotation(True)

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

        elif event.key() == Qt.Key_Minus and event.modifiers() != Qt.ControlModifier:
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
        elif event.key() == Qt.Key_Minus and event.modifiers() == Qt.ControlModifier:
            try:
                current_stream = self.state["current_stream"]
                current_behav_epoch_table = self.behav_epoch_tables[current_stream.ID]
                current_behav_epoch_table.model().jump_to_prev(
                    self.state["current_frame"]
                )
            except Exception:
                pass
        elif event.key() == Qt.Key_Equal and event.modifiers() != Qt.ControlModifier:
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
        elif event.key() == Qt.Key_Equal and event.modifiers() == Qt.ControlModifier:
            try:
                current_stream = self.state["current_stream"]
                current_behav_epoch_table = self.behav_epoch_tables[current_stream.ID]
                current_behav_epoch_table.model().jump_to_next(
                    self.state["current_frame"]
                )
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
        if self.dialog_state:
            return True
        return False

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            for video in self.vids:
                video.stop_worker()
            event.accept()
        else:
            event.ignore()
