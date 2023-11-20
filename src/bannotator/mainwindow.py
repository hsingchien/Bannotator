import numpy as np
import os
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
import bannotator.dialog as dialog
from bannotator.widgets import TrackBar, BehavVideoView, BehavLabel, AnnotatorMainWindow
from bannotator.ui.ui_mainwindow import Ui_MainWindow
from bannotator.neuralwindow import NeuralWindow


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
        self._dialog_state = False

        # Container for dynamically generated widgets
        # Key = stream ID, item = TrackBar widget
        self._stream_tracks = dict()
        self._full_stream_tracks = dict()
        # Key = stream ID, item = stream QLabel for current behavior
        self._behavior_labels = dict()
        # Key = stream ID, item = stream table model
        self._epoch_tables = dict()
        # Key = ID, item = behavior epoch table model
        self._behav_epoch_tables = dict()

        # Initialize a neural window
        self.neural_window = NeuralWindow(state=self.state)

        # Group video viewers into list
        self._video_views = [self.vid1_view]
        self._videos = []
        self._video_stretch_factor = []
        # Set up timers
        self._play_timer = QTimer(self)
        self._play_timer.timeout.connect(self._video_play_frame_update)
        self._auto_save_timer = QTimer(self)
        self._auto_save_timer.timeout.connect(self._save_annotation_copy)
        self._auto_save_timer.start(30000)
        self._update_gui_timer = QTimer(self)
        self._update_gui_timer.timeout.connect(lambda: self._update_gui(["gui"]))
        self._update_gui_timer.start(33)
        self._key_hold_monitor = QTimer(self)
        self._key_hold_monitor.setSingleShot(True)

        # Set up pushbuttons, spinboxes and other interactable widgets
        self.play_button.clicked.connect(self._play_video)
        self.pause_button.clicked.connect(self._play_timer.stop)
        self.speed_doubleSpinBox.valueChanged.connect(self._set_play_speed)
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

        self.add_behavior_button.clicked.connect(self._add_behavior)
        self.delete_behavior_button.clicked.connect(self._delete_behavior)
        self.add_stream_button.clicked.connect(self._add_stream)
        self.delete_stream_button.clicked.connect(self._delete_stream)
        # Connect menu bar actions
        # File menu
        self.actionReset.triggered.connect(self._reset_app)
        self.actionQuit.triggered.connect(self.close)
        # Video menu
        self.actionOpen_video.triggered.connect(self._open_video)
        self.actionAdd_seq.triggered.connect(self._add_seq)
        # Annotation menu
        self.actionOpen_annotation.triggered.connect(self._open_annotation)
        self.actionSave_annotation.triggered.connect(self._save_annotation)
        self.actionSave_annotation_as_MAT.triggered.connect(self._save_annotation_mat)
        self.actionNew_annotation.triggered.connect(self._new_annotation)
        self.actionOpen_config.triggered.connect(self._open_config)
        self.actionSave_config.triggered.connect(self._save_config)
        self.actionAuto_save_annotation.toggled.connect(
            lambda x: self._auto_save_timer.start(30000)
            if x
            else self._auto_save_timer.stop()
        )
        self.actionClose_annotation.triggered.connect(self._close_annotation)
        # View menu
        self.actionFull_annotation.toggled.connect(
            lambda: self._update_gui(["view_options"])
        )
        self.actionBehavior_table.toggled.connect(
            lambda: self._update_gui(["view_options"])
        )
        self.actionEpoch_table.toggled.connect(
            lambda: self._update_gui(["view_options"])
        )
        self.actionNeural_window.toggled.connect(
            lambda: self._update_gui(["view_options"])
        )

        self.behav_table_dock.closed.connect(self.actionBehavior_table.setChecked)
        self.epoch_dock.closed.connect(self.actionEpoch_table.setChecked)
        self.tracks_dock.closed.connect(self.actionFull_annotation.setChecked)
        self.neural_window.closed.connect(self.actionNeural_window.setChecked)

        self.actionTrack_epoch.toggled.connect(
            lambda: self._update_gui(["view_options"])
        )
        self.actionShuffle_colors.triggered.connect(
            lambda: self.state["annot"].assign_behavior_color()
            if self.state["annot"] is not None
            else None
        )
        # Connect state change
        self._connect_states()

    def _connect_states(self):
        self.state.connect(
            "current_frame",
            [
                self._go_to_frame,
                self._update_slider_box,
                lambda: self._update_gui(["video_ui"]),
            ],
        )

        self.state.connect(
            "track_window",
            [self._update_slider_box],
        )
        self.state.connect("slider_box", [lambda: self._update_gui(["video_ui"])])
        self.state.connect(
            "annot", [self._setup_annotation_widgets, lambda: self._update_gui(["gui"])]
        )
        self.state.connect("video", [lambda: self._update_gui(["video_ui"])])
        self.state.connect("video_layout", [lambda: self._update_gui(["video_layout"])])
        self.state.connect("current_stream", [lambda: self._update_gui(["tracks"])])

    def _update_gui(self, topics):
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
                    self._stream_tracks[stream.ID].set_selected(True)
                    self._behavior_labels[stream.ID].set_selected(True)
                else:
                    self._stream_tracks[stream.ID].set_selected(False)
                    self._behavior_labels[stream.ID].set_selected(False)
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
                self.video_slider.setMaximum(self._videos[0].num_frame())
                self.curframe_spinBox.setMaximum(self._videos[0].num_frame())
                self.track_window_spinbox.setMaximum(self._videos[0].num_frame())
            # Update the video layout combobox
            if (
                self.state["video"] > 3
                and self.video_layout_comboBox.findText("Grid") == -1
            ):
                self.video_layout_comboBox.addItem("Grid")
            elif (
                self.state["video"] <= 3
                and self.video_layout_comboBox.currentText() != "Grid"
            ):
                self.video_layout_comboBox.removeItem(
                    self.video_layout_comboBox.findText("Grid")
                )
            elif (
                self.state["video"] <= 3
                and self.video_layout_comboBox.currentText() == "Grid"
            ):
                self.video_layout_comboBox.setCurrentText("Side by Side")
                self.video_layout_comboBox.removeItem(
                    self.video_layout_comboBox.findText("Grid")
                )
            if self.state["annot"] is not None:
                # Enable annotation options
                self.actionSave_annotation.setEnabled(True)
                self.actionSave_annotation_as_MAT.setEnabled(True)
                self.actionSave_config.setEnabled(True)
            else:
                self.actionSave_annotation.setEnabled(False)
                self.actionSave_annotation_as_MAT.setEnabled(False)
                self.actionSave_config.setEnabled(False)
            if self.state["video"] > 0:
                self.actionOpen_config.setEnabled(True)
                self.actionNew_annotation.setEnabled(True)
            else:
                self.actionOpen_config.setEnabled(False)
                self.actionNew_annotation.setEnabled(False)
            # Fit all video views
            for view in self._video_views:
                view.fitPixItem()
            # Display video path in window title
            if self.state["video"] > 0:
                file_name = self._videos[0].file_name()
                self.setWindowTitle(" - ".join(["Annotator", file_name]))
            else:
                self.setWindowTitle("Annotator")
            # Set stretch factor for video layout (side by side and stacked)
            if self.state["video_layout"] != "Grid":
                for view in self._video_views:
                    self.video_layout.setStretchFactor(view, 1)
            # Update neural window
            self.neural_window.update_stream_combobox()

        if "video_layout" in topics:
            # Convert video layout
            current_layout = self.video_layout
            index = self.display_layout.indexOf(current_layout)
            stretch_factor = self.display_layout.stretch(index)
            if self.state["video_layout"] == "Side by Side":
                new_layout = QHBoxLayout()
                for vid in self._video_views:
                    new_layout.addWidget(vid, 1)
            if self.state["video_layout"] == "Stacked":
                new_layout = QVBoxLayout()
                for vid in self._video_views:
                    new_layout.addWidget(vid, 1)

            if self.state["video_layout"] == "Grid":
                nvideos = len(self._video_views)
                new_layout = QGridLayout()
                n_row = np.floor(np.sqrt(nvideos))
                n_col = np.ceil(nvideos / n_row)
                for i, vid in enumerate(self._video_views):
                    new_layout.addWidget(vid, i // n_col, i % n_col)
                for i in range(int(n_row)):
                    new_layout.setRowStretch(i, 1)
                for i in range(int(n_col)):
                    new_layout.setColumnStretch(i, 1)
            self.video_layout = new_layout
            self.display_layout.removeItem(current_layout)
            self.display_layout.insertLayout(index, new_layout, stretch_factor)

        if "view_options" in topics:
            self.behav_table_dock.setVisible(self.actionBehavior_table.isChecked())
            self.epoch_dock.setVisible(self.actionEpoch_table.isChecked())
            self.tracks_dock.setVisible(self.actionFull_annotation.isChecked())
            self.neural_window.setVisible(self.actionNeural_window.isChecked())
            # Set the epoch tracking state
            if self.actionTrack_epoch.isChecked() and self._epoch_tables:
                for ID, stream in self.state["annot"].get_streams().items():
                    self._epoch_tables[ID].connect_scroll()
                    self._behav_epoch_tables[ID].connect_scroll()
                    stream.get_epoch_by_idx(self.state["current_frame"])
            elif self._epoch_tables:
                for ID in self.state["annot"].get_streams():
                    self._epoch_tables[ID].disconnect_scroll()
                    self._behav_epoch_tables[ID].disconnect_scroll()

    def _update_slider_box(self):
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

    def _open_video(self):
        # Add a mainstream video file.
        # Also create and start a frame fetching worker in a separate thread, emitting frames at 60Hz
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
            and np.abs(bvideo.num_frame() - self._videos[0].num_frame())
            > 0.05 * self._videos[0].num_frame()
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

        self._videos.append(bvideo)
        # Set stretch factors
        if self.state["video"] == 0:
            self._video_stretch_factor = [1]
        else:
            self._video_stretch_factor.append(
                bvideo.num_frame() / self._videos[0].num_frame()
            )
        # Connect scene
        if self.state["video"] == 0:
            bvideo.new_frame_fetched.connect(self._video_views[0].updatePixmap)
            self.state["FPS"] = bvideo.frame_rate()
        else:
            new_view = BehavVideoView()
            bvideo.new_frame_fetched.connect(new_view.updatePixmap)
            self._video_views.append(new_view)
            self._update_gui(["video_layout"])
            # new_view.show()
        # Change state and trigger callbakcs
        self._go_to_frame(self.state["current_frame"])
        self.state["video"] += 1
        QTimer.singleShot(30, lambda: self._update_gui(["gui"]))

    def _add_seq(self):
        # Add a .seq file. SeqBehavVideo class supports reading RAW and JPEG seq files.
        # Also create a frame fetching worker that fetches frames and emits at 60Hz to the video widget.
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
            and np.abs(bvideo.num_frame() - self._videos[0].num_frame())
            > 0.05 * self._videos[0].num_frame()
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
            self._video_stretch_factor = [1]
        else:
            self._video_stretch_factor.append(
                bvideo.num_frame() / self._videos[0].num_frame()
            )
        #
        bvideo.start_frame_fetcher()
        bvideo.run_worker.connect(
            lambda: self._go_to_frame(self.state["current_frame"])
        )
        self._videos.append(bvideo)
        if self.state["video"] == 0:
            bvideo.new_frame_fetched.connect(self._video_views[0].updatePixmap)
            self.state["FPS"] = bvideo.frame_rate()
        else:
            new_view = BehavVideoView()
            bvideo.new_frame_fetched.connect(new_view.updatePixmap)
            self._video_views.append(new_view)
            self._update_gui(["video_layout"])
            # new_view.show()
        # Refresh the scene
        self._go_to_frame(self.state["current_frame"])
        # Trigger ui updtates
        self.state["video"] += 1
        self.video_slider.setMinimum(1)
        self.curframe_spinBox.setMinimum(1)
        QTimer.singleShot(30, lambda: self._update_gui(["gui"]))

    def _open_annotation(self):
        # Open an existing annotation.txt file.
        # Read and load an existing annotation txt file.
        # Loaded annotation is inexplicitly verified
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
        annotation.assign_behavior_color(12)
        annot_length = annotation.get_length()
        if self._videos and annot_length < self._videos[0].num_frame():
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
                annotation.set_length(self._videos[0].num_frame())

        elif self._videos and annot_length > self._videos[0].num_frame():
            # Guide user to shrink the annotation
            self._dialog_state = True
            (from_value, to_value) = dialog.TruncateAnnotationDialog(
                annot_length, self._videos[0].num_frame(), parent=self
            ).get_input()
            if from_value is not None:
                annotation.truncate(
                    start=from_value, length=self._videos[0].num_frame()
                )
            else:
                return False
        self.state["annot"] = annotation

    def _new_annotation(self):
        # Create a new annotation.
        # Pops out a new annotation dialog, guide the user to create a new annotation
        if self.state["annot"] is not None:
            annot_closed = self._close_annotation(False)
        else:
            annot_closed = True
        if not annot_closed:
            return False
        self._dialog_state = True
        new_dialog = dialog.NewAnnotationDialog()
        (nstream, ns, ks) = new_dialog.get_input()
        if nstream is None:
            self._dialog_state = False
            return False
        annotation = Annotation({})
        fake_annots = dict()
        le = self.video_slider.maximum()
        for i in range(nstream):
            fake_annots[i + 1] = [
                " ".join(["1", str(le), ns[0]])
            ]  # Create a fake annotation file read
        fake_config = []
        for i, n in enumerate(ns):
            fake_config.append(" ".join([n, ks[i]]))
        annotation._construct_streams(fake_config, fake_annots)
        annotation.assign_behavior_color(12)
        self.state["annot"] = annotation
        self._dialog_state = False
        return True

    def _open_config(self):
        # Open and read a configuration.txt file.
        # Creates empty streams as defined in the configuration file.
        # The length of the streams is determined by the video.
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
            annotation.set_length(self._videos[0].num_frame())
        else:
            annotation.set_length(self.video_slider.maximum())
        annotation.assign_behavior_color(12)
        self.state["annot"] = annotation

    def _setup_annotation_widgets(self):
        # Called after a valid annotation is loaded
        # Sets up the behavior table, stats table, stream epoch tables and behavior epoch tables.
        # Create full length track widgets, track widgets and behavior labels for each stream.
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
            self._setup_stream_tables(stream)
            # Emit the cur_epoch signal from the stream after all tables are set up to
            # highlight the current epoch
            stream.get_epoch_by_idx(self.state["current_frame"])

        self._update_slider_box()
        for _, stream in streams.items():
            self._plot_stream_tracks(stream)

        # Set the first stream as current stream
        IDs = sorted(list(streams.keys()))
        self.state["current_stream"] = streams[IDs[0]]

        return True

    def _setup_stream_tables(self, stream):
        # Create stream tables and connect table signals and ui behavior
        stream_table = StreamTableModel(
            stream=stream, properties=["name", "start", "end"], state=self.state
        )
        stream_table_view = GenericTableView()
        stream_table_view.setModel(stream_table)
        stream_table_view.set_columns_fixed([1, 2])
        stream.data_changed.connect(stream_table_view.repaint_table)
        stream.epoch_number_changed.connect(stream_table_view.change_layout)
        self._epoch_tables[stream.ID] = stream_table_view
        self.stream_table_layout.addWidget(stream_table_view)
        stream_table.jump_to_frame.connect(lambda x: self.state.set("current_frame", x))
        # Create behavior label, add to the full track widget
        behav_label = BehavLabel(
            behav=stream.get_behavior_by_idx(self.state["current_frame"]),
        )
        self.cur_behav_layout.addWidget(behav_label)
        self._behavior_labels[stream.ID] = behav_label
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
        self._behav_epoch_tables[stream.ID] = behav_epoch_table_view
        self.behav_epoch_table_layout.addWidget(behav_epoch_table_view)
        if self.actionTrack_epoch.isChecked():
            behav_epoch_table_view.connect_scroll()

    def _save_annotation(self):
        # Save annotation dialog
        self.state["annot"].saved_in_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        self.statusbar.showMessage("Saving annotation...", 0)
        if self.state["annot"].get_file_path() is not None:
            annot_name = self.state["annot"].get_file_path()
        elif self._videos:
            vid_path = self._videos[0].file_name()
            annot_name = vid_path.replace("." + vid_path.split(".")[-1], "_annot.txt")
        else:
            annot_name = "annotation.txt"

        filename, _ = QFileDialog.getSaveFileName(
            None, "Save Annotation", annot_name, "text Files (*.txt)"
        )
        if not filename:
            return False
        self.statusbar.clearMessage()
        return self.state["annot"].save_to_file(filename)

    def _save_annotation_copy(self):
        # Auto-save annotation copy silently.
        try:
            annot_path = self.state["annot"].get_file_path()
            if annot_path is not None:
                filename = annot_path.replace(".txt", "_backup.txt")
            elif self._videos:
                vid_path = self._videos[0].file_name()
                filename = vid_path.replace(
                    "." + vid_path.split(".")[-1], "_annotation_backup.txt"
                )
            else:
                filename = os.path.join(os.getcwd(), "annotation_backup.txt")

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

    def _save_annotation_mat(self):
        # Save annotation dialog
        self.state["annot"].saved_in_file.connect(
            lambda x: self.statusbar.showMessage(x, 5000)
        )
        self.statusbar.showMessage("Saving annotation...", 0)
        if self.state["annot"].get_file_path() is not None:
            annot_name = self.state["annot"].get_file_path().replace("txt", "mat")
        elif self._videos:
            vid_path = self._videos[0].file_name()
            annot_name = vid_path.replace("." + vid_path.split(".")[-1], "_annot.mat")
        else:
            annot_name = "annotation.mat"

        filename, _ = QFileDialog.getSaveFileName(
            None, "Save Annotation", annot_name, "mat Files (*.mat)"
        )
        if not filename:
            return False
        self.statusbar.clearMessage()
        return self.state["annot"].save_to_matfile(filename)

    def _save_config(self):
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

    def _go_to_frame(self, frameN):
        # Send frame index signal to all the frame fetchers. Also stretch the frame according to stretch factors.
        videos = self._videos
        if videos:
            for i, video in enumerate(videos):
                this_frameN = frameN * self._video_stretch_factor[i]
                video.get_pixmap(int(this_frameN))
            return True
        else:
            return False

    def _video_play_frame_update(self):
        # Calculate the index of next frame based on the play speed and change the current frame state.
        # When speed is higher than 2x, round the speed to integer.
        if abs(self.state["play_speed"] - 0.00) > 2.0001:
            next_frame = self.state["current_frame"] + 1 * np.round(
                self.state["play_speed"]
            )
        # When speed is between 0 and 2x, use the true speed value.
        elif abs(self.state["play_speed"] - 0.00) > 0.0001:
            next_frame = self.state["current_frame"] + 1 * np.sign(
                self.state["play_speed"]
            )
        # When next frame reaches the edge, stop playing
        if next_frame < self._videos[0].num_frame() and next_frame > -1:
            self.state["current_frame"] = next_frame
            return True
        elif next_frame >= self._videos[0].num_frame():
            self.state["current_frame"] = self._videos[0].num_frame() - 1
            self._play_timer.stop()
        elif next_frame <= 0:
            self.state["current_frame"] = 0
            self._play_timer.stop()
        else:
            return False

    def _play_video(self):
        play_speed = self.state["play_speed"]
        # Start play timer based on the value of play speed
        if abs(play_speed - 0.00) > 2.0001:
            # If playspeed faster than 2.0, then play timer timeout at original FPS
            # Speeding up video by skipping frames
            self._play_timer.start(self.state["FPS"])
        elif abs(play_speed - 0.00) > 0.0001:
            # If playspeed slower than 2.0, speeding up by speeding up timer without skipping frames
            self._play_timer.start(1000 / (self.state["FPS"] * abs(play_speed)))
        else:
            # If playspeed is 0, stop the play timer
            self._play_timer.stop()

    def _set_play_speed(self, value):
        self.state["play_speed"] = value
        if self._play_timer.isActive():
            self._play_video()
        else:
            return True

    def _plot_stream_tracks(self, stream):
        # Generate tracks for the streams.
        stream_vect = stream.get_stream_vect()
        color_dict = stream.get_color_dict()
        # Create windowed stream tracks.
        track = TrackBar(
            data=stream_vect,
            color_dict=color_dict,
            frame_mark=self.state["current_frame"],
            slider_box=self.state["slider_box"],
            min_height=16,
            use_pixmap=False,
            full_track_flag=False,
        )
        self._stream_tracks[stream.ID] = track
        stream.data_changed.connect(track.set_data)
        stream.color_changed.connect(track.set_color_dict)
        self.state.connect("current_frame", track.set_frame_mark)
        self.state.connect("slider_box", track.set_slider_box)
        self.track_layout.addWidget(track)
        # Make full length track widgets
        full_track = TrackBar(
            data=stream_vect,
            color_dict=color_dict,
            frame_mark=self.state["current_frame"],
            slider_box=self.state["slider_box"],
            min_height=8,
            use_pixmap=True,
            full_track_flag=True,
        )
        self.state.connect("current_frame", full_track.set_frame_mark)
        self.state.connect("slider_box", full_track.set_slider_box)
        stream.data_changed.connect(full_track.set_data)
        stream.color_changed.connect(full_track.set_color_dict)
        self.full_tracks_layout.addWidget(full_track)
        self._full_stream_tracks[stream.ID] = full_track
        # Also connect stream content change signals to video slider track update
        stream.data_changed.connect(self.video_slider.set_track_data)
        stream.color_changed.connect(self.video_slider.set_color_dict)

    def _change_current_behavior(self, keypressed: str = None):
        # Called upon user invoked behavior change from keypresss
        # Emit signals to change the ui
        cur_idx = self.state["current_frame"]
        cur_stream = self.state["current_stream"]
        if cur_stream is None:
            return False
        else:
            cur_stream.set_behavior(cur_idx, keypressed)
            cur_stream.get_epoch_by_idx(self.state["current_frame"])
            return True

    def _add_behavior(self):
        # Dialog to guide behavior adding.
        # Give options to define name and keystroke.
        if self.state["annot"] is None:
            return False
        self._dialog_state = True
        newdialog = dialog.AddBehaviorDialog(
            parent=self, annotation=self.state["annot"]
        )
        name, keybind = newdialog.get_input()
        if name is not None and keybind is not None:
            self.state["annot"].add_behavior(name, keybind)
        self._dialog_state = False

    def _add_stream(self):
        # Dialog to guide stream adding.
        # New stream will be initialized with selected behavior.
        if self.state["annot"] is None:
            return False
        self._dialog_state = True
        newdialog = dialog.AddStreamDialog(parent=self, annotation=self.state["annot"])
        behavior = newdialog.get_input()
        if behavior is not None:
            new_stream = self.state["annot"].add_stream(behavior)
            self._setup_stream_tables(new_stream)
            self._plot_stream_tracks(new_stream)
            new_stream.get_epoch_by_idx(self.state["current_frame"])
            self._dialog_state = False
        else:
            self._dialog_state = False
            return False

    def _delete_behavior(self):
        # Dialog to guide behavior deleting.
        # Epochs of deleted behavior will be merged into selected behavior.
        if self.state["annot"] is None:
            return False
        self._dialog_state = True
        newdialog = dialog.DeleteBehaviorDialog(
            parent=self, annotation=self.state["annot"]
        )
        to_del, to_rep = newdialog.get_input()
        if to_del is not None:
            # If behavior_epoch tables are viewing the deleted behavior, set it to replace behavior
            if self.stats_table.model().current_activate_property("name") == to_del:
                self.stats_table.model().set_activate_by_name(to_rep)
            self.state["annot"].delete_behavior(to_del, to_rep)
        else:
            self._dialog_state = False
            return False
        for _, stream in self.state["annot"].get_streams().items():
            stream.get_epoch_by_idx(self.state["current_frame"])
        self._dialog_state = False

    def _delete_stream(self):
        # Dialog to guide stream deleting.
        # Widgets associated with the deleted stream are removed alongside.
        if self.state["annot"] is None:
            return False
        self._dialog_state = True
        newdialog = dialog.DeleteStreamDialog(
            parent=self, annotation=self.state["annot"]
        )
        del_id = newdialog.get_input()
        if del_id is None:
            self._dialog_state = False
            return False
        if self.state["annot"].num_stream() == 1:
            self._dialog_state = False
            return False
        # Remove tables
        stream_table = self._epoch_tables.pop(del_id)
        utt.reset_table(stream_table)
        behav_stream_table = self._behav_epoch_tables.pop(del_id)
        utt.reset_table(behav_stream_table)
        self.stream_table_layout.removeWidget(stream_table)
        self.behav_epoch_table_layout.removeWidget(behav_stream_table)
        # Remove tracks
        full_track = self._full_stream_tracks.pop(del_id)
        track = self._stream_tracks.pop(del_id)
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
        blabel = self._behavior_labels.pop(del_id)
        self.cur_behav_layout.removeWidget(blabel)
        # Delete widgets
        stream_table.deleteLater()
        behav_stream_table.deleteLater()
        full_track.deleteLater()
        track.deleteLater()
        blabel.deleteLater()
        self.state.disconnect("current_frame", stream.get_epoch_by_idx)
        del stream
        self._dialog_state = False
        return True

    def _assign_current_stream(self, keyint: int):
        # Respond to user num key press. Assign the current stream to the corresponding stream.
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

    def _close_annotation(self, suppress_warning=False):
        # Close the current annotation. Also removes all the widgets and reset the signal connections.
        # First clear out all the widgets
        if self.state["annot"] is None:
            return False
        self._play_timer.stop()
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
        self._stream_tracks.clear()
        self._full_stream_tracks.clear()
        self._behavior_labels.clear()
        self._epoch_tables.clear()
        self._behav_epoch_tables.clear()
        self.state["annot"] = None
        self.state["slider_box"] = [None, None]
        # Reconnect callbacks
        self._connect_states()
        self._update_gui(["gui"])
        return True

    def _reset_app(self):
        # Close annotation and remove all videos.
        self._play_timer.stop()
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
        for vid in self._videos:
            vid.stop_worker()
        while len(self._video_views) > 1:
            vid_view = self._video_views.pop(-1)
            self.video_layout.removeWidget(vid_view)
            vid_view.deleteLater()
        self.state.clear_connections("video")
        self.state.clear_connections("video_layout")
        self.state.clear_connections("FPS")
        self.state.clear_connections("play_speed")
        self.state["FPS"] = None
        self._video_stretch_factor = []
        self._videos.clear()
        self._close_annotation(True)
        self.vid1_view.clear_pixmap()
        self._update_gui(["gui"])
        return True

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if self._editing_state():
                return False
            if event.key() in range(Qt.Key_A, Qt.Key_Z + 1):
                # Alphabets
                self._change_current_behavior(event.text().lower())
            if event.key() in range(Qt.Key_0, Qt.Key_9 + 1):
                # Numbers
                try:
                    self._assign_current_stream(event.key())
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
                    self._assign_current_stream(i)
                except:
                    pass

            elif (
                event.key() == Qt.Key_Minus and event.modifiers() != Qt.ControlModifier
            ):
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
                        previous_epoch = current_stream.get_epoch_by_idx(
                            current_frame - 1
                        )
                        self.state["current_frame"] = previous_epoch.start - 1
                except Exception:
                    pass
            elif (
                event.key() == Qt.Key_Minus and event.modifiers() == Qt.ControlModifier
            ):
                try:
                    current_stream = self.state["current_stream"]
                    current_behav_epoch_table = self._behav_epoch_tables[
                        current_stream.ID
                    ]
                    current_behav_epoch_table.model().jump_to_prev(
                        self.state["current_frame"]
                    )
                except Exception:
                    pass
            elif (
                event.key() == Qt.Key_Equal and event.modifiers() != Qt.ControlModifier
            ):
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
            elif (
                event.key() == Qt.Key_Equal and event.modifiers() == Qt.ControlModifier
            ):
                try:
                    current_stream = self.state["current_stream"]
                    current_behav_epoch_table = self._behav_epoch_tables[
                        current_stream.ID
                    ]
                    current_behav_epoch_table.model().jump_to_next(
                        self.state["current_frame"]
                    )
                except Exception:
                    pass

            elif event.key() == Qt.Key_Space:
                # Spacebar, toggle play/pause
                try:
                    if not self._play_timer.isActive():
                        self._play_video()
                    else:
                        self._play_timer.stop()
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
                self.state["play_speed"] = -1.0
                self._key_hold_monitor.timeout.connect(lambda: self._play_video())
                self._key_hold_monitor.start(100)
            elif event.key() == Qt.Key_Right:
                # RIGHT key, next 1 frame
                self.state["current_frame"] = min(
                    self.state["current_frame"] + 1, self.curframe_spinBox.maximum()
                )
                self.state["play_speed"] = 1.0
                self._key_hold_monitor.timeout.connect(lambda: self._play_video())
                self._key_hold_monitor.start(100)
            else:
                return super().eventFilter(obj, event)
        elif event.type() == QEvent.KeyRelease:
            if self._editing_state():
                return False
            if event.key() == Qt.Key_Left:
                self._key_hold_monitor.stop()
                self._play_timer.stop()
                self.state["play_speed"] = self.speed_doubleSpinBox.value()
                self._key_hold_monitor.timeout.disconnect()
            elif event.key() == Qt.Key_Right:
                self._key_hold_monitor.stop()
                self._play_timer.stop()
                self.state["play_speed"] = self.speed_doubleSpinBox.value()
                self._key_hold_monitor.timeout.disconnect()
            else:
                return super().eventFilter(obj, event)
        else:
            return super().eventFilter(obj, event)
        # Stop propagation
        return True

    def _editing_state(self):
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
        for _, table in self._epoch_tables.items():
            if table.state() == QAbstractItemView.EditingState:
                return True
        if self._dialog_state:
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
            for video in self._videos:
                video.stop_worker()
            self.neural_window.close()
            event.accept()
        else:
            event.ignore()
