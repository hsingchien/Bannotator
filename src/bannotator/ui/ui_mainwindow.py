# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from bannotator.dataview import GenericTableView
from bannotator.widgets import BehavVideoView, DockWidget, PlaySpeedSpinBox, VideoSlider
import bannotator.resources.resource_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        self.actionOpen_video = QAction(MainWindow)
        self.actionOpen_video.setObjectName("actionOpen_video")
        self.actionOpen_config = QAction(MainWindow)
        self.actionOpen_config.setObjectName("actionOpen_config")
        self.actionOpen_config.setEnabled(False)
        self.actionSave_config = QAction(MainWindow)
        self.actionSave_config.setObjectName("actionSave_config")
        self.actionSave_config.setEnabled(False)
        self.actionOpen_annotation = QAction(MainWindow)
        self.actionOpen_annotation.setObjectName("actionOpen_annotation")
        self.actionSave_annotation = QAction(MainWindow)
        self.actionSave_annotation.setObjectName("actionSave_annotation")
        self.actionSave_annotation.setEnabled(False)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionNew_config = QAction(MainWindow)
        self.actionNew_config.setObjectName("actionNew_config")
        self.actionFull_annotation = QAction(MainWindow)
        self.actionFull_annotation.setObjectName("actionFull_annotation")
        self.actionFull_annotation.setCheckable(True)
        self.actionFull_annotation.setChecked(True)
        self.actionBehavior_table = QAction(MainWindow)
        self.actionBehavior_table.setObjectName("actionBehavior_table")
        self.actionBehavior_table.setCheckable(True)
        self.actionBehavior_table.setChecked(True)
        self.actionEpoch_table = QAction(MainWindow)
        self.actionEpoch_table.setObjectName("actionEpoch_table")
        self.actionEpoch_table.setCheckable(True)
        self.actionEpoch_table.setChecked(True)
        self.actionRemove_video = QAction(MainWindow)
        self.actionRemove_video.setObjectName("actionRemove_video")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionReset = QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionTips = QAction(MainWindow)
        self.actionTips.setObjectName("actionTips")
        self.actionAdd_seq = QAction(MainWindow)
        self.actionAdd_seq.setObjectName("actionAdd_seq")
        self.actionTrack_epoch = QAction(MainWindow)
        self.actionTrack_epoch.setObjectName("actionTrack_epoch")
        self.actionTrack_epoch.setCheckable(True)
        self.actionTrack_epoch.setChecked(True)
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMerge_behaviors = QAction(MainWindow)
        self.actionMerge_behaviors.setObjectName("actionMerge_behaviors")
        self.actionAuto_save_annotation = QAction(MainWindow)
        self.actionAuto_save_annotation.setObjectName("actionAuto_save_annotation")
        self.actionAuto_save_annotation.setCheckable(True)
        self.actionAuto_save_annotation.setChecked(True)
        self.actionMerge_behavior = QAction(MainWindow)
        self.actionMerge_behavior.setObjectName("actionMerge_behavior")
        self.actionClose_annotation = QAction(MainWindow)
        self.actionClose_annotation.setObjectName("actionClose_annotation")
        self.actionNew_annotation = QAction(MainWindow)
        self.actionNew_annotation.setObjectName("actionNew_annotation")
        self.actionNew_annotation.setEnabled(False)
        self.actionShuffle_colors = QAction(MainWindow)
        self.actionShuffle_colors.setObjectName("actionShuffle_colors")
        self.actionSave_annotation_as_MAT = QAction(MainWindow)
        self.actionSave_annotation_as_MAT.setObjectName("actionSave_annotation_as_MAT")
        self.actionSave_annotation_as_MAT.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.display_layout = QVBoxLayout(self.layoutWidget)
        self.display_layout.setSpacing(4)
        self.display_layout.setObjectName("display_layout")
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        self.video_control_hlayout = QHBoxLayout()
        self.video_control_hlayout.setSpacing(3)
        self.video_control_hlayout.setObjectName("video_control_hlayout")
        self.time_label = QLabel(self.layoutWidget)
        self.time_label.setObjectName("time_label")
        font = QFont()
        font.setFamilies(["Courier New"])
        font.setPointSize(13)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.time_label.setFont(font)
        self.time_label.setTextFormat(Qt.MarkdownText)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.video_control_hlayout.addWidget(self.time_label)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.video_control_hlayout.addItem(self.horizontalSpacer)

        self.current_frame_label = QLabel(self.layoutWidget)
        self.current_frame_label.setObjectName("current_frame_label")

        self.video_control_hlayout.addWidget(self.current_frame_label)

        self.curframe_spinBox = QSpinBox(self.layoutWidget)
        self.curframe_spinBox.setObjectName("curframe_spinBox")
        self.curframe_spinBox.setMinimum(1)
        self.curframe_spinBox.setMaximum(1000)

        self.video_control_hlayout.addWidget(self.curframe_spinBox)

        self.horizontalSpacer_1 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.video_control_hlayout.addItem(self.horizontalSpacer_1)

        self.play_button = QPushButton(self.layoutWidget)
        self.play_button.setObjectName("play_button")

        self.video_control_hlayout.addWidget(self.play_button)

        self.pause_button = QPushButton(self.layoutWidget)
        self.pause_button.setObjectName("pause_button")

        self.video_control_hlayout.addWidget(self.pause_button)

        self.video_speed_label = QLabel(self.layoutWidget)
        self.video_speed_label.setObjectName("video_speed_label")

        self.video_control_hlayout.addWidget(self.video_speed_label)

        self.speed_doubleSpinBox = PlaySpeedSpinBox(self.layoutWidget)
        self.speed_doubleSpinBox.setObjectName("speed_doubleSpinBox")
        self.speed_doubleSpinBox.setMinimum(-10.000000000000000)
        self.speed_doubleSpinBox.setMaximum(10.000000000000000)
        self.speed_doubleSpinBox.setSingleStep(0.100000000000000)
        self.speed_doubleSpinBox.setValue(1.000000000000000)

        self.video_control_hlayout.addWidget(self.speed_doubleSpinBox)

        self.track_window_label = QLabel(self.layoutWidget)
        self.track_window_label.setObjectName("track_window_label")

        self.video_control_hlayout.addWidget(self.track_window_label)

        self.track_window_spinbox = QSpinBox(self.layoutWidget)
        self.track_window_spinbox.setObjectName("track_window_spinbox")
        self.track_window_spinbox.setMinimum(1)
        self.track_window_spinbox.setMaximum(1000)
        self.track_window_spinbox.setValue(500)

        self.video_control_hlayout.addWidget(self.track_window_spinbox)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.video_control_hlayout.addItem(self.horizontalSpacer_2)

        self.video_layout_label = QLabel(self.layoutWidget)
        self.video_layout_label.setObjectName("video_layout_label")

        self.video_control_hlayout.addWidget(self.video_layout_label)

        self.video_layout_comboBox = QComboBox(self.layoutWidget)
        self.video_layout_comboBox.addItem("")
        self.video_layout_comboBox.addItem("")
        self.video_layout_comboBox.setObjectName("video_layout_comboBox")
        self.video_layout_comboBox.setMinimumSize(QSize(10, 0))

        self.video_control_hlayout.addWidget(self.video_layout_comboBox)

        self.video_control_hlayout.setStretch(0, 1)
        self.video_control_hlayout.setStretch(3, 1)
        self.video_control_hlayout.setStretch(8, 1)
        self.video_control_hlayout.setStretch(10, 1)
        self.video_control_hlayout.setStretch(13, 1)

        self.display_layout.addLayout(self.video_control_hlayout)

        self.video_layout = QHBoxLayout()
        self.video_layout.setObjectName("video_layout")
        self.vid1_view = BehavVideoView(self.layoutWidget)
        self.vid1_view.setObjectName("vid1_view")
        font1 = QFont()
        font1.setFamilies(["Andale Mono"])
        self.vid1_view.setFont(font1)

        self.video_layout.addWidget(self.vid1_view)

        self.display_layout.addLayout(self.video_layout)

        self.video_slider = VideoSlider(self.layoutWidget)
        self.video_slider.setObjectName("video_slider")
        self.video_slider.setStyleSheet(
            "QSlider::groove:horizontal {\n"
            "    border: 0px solid #999999;\n"
            "    height: 20px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */\n"
            "    margin-left: 3px;\n"
            "	margin-right: 3px;\n"
            "}\n"
            "QSlider::handle:horizontal {\n"
            "    background: #ffffff;\n"
            "    border: 1px solid #5c5c5c;\n"
            "    width: 6px;\n"
            "    margin-left: -3px;\n"
            "	margin-right:-3px;\n"
            "    border-radius: 3px;\n"
            "	subcontrol-origin: content;\n"
            "}"
        )
        self.video_slider.setMinimum(1)
        self.video_slider.setMaximum(1000)
        self.video_slider.setValue(1)
        self.video_slider.setOrientation(Qt.Horizontal)
        self.video_slider.setTickPosition(QSlider.NoTicks)

        self.display_layout.addWidget(self.video_slider)

        self.display_layout.setStretch(1, 4)
        self.splitter.addWidget(self.layoutWidget)
        self.track_frame = QFrame(self.splitter)
        self.track_frame.setObjectName("track_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.track_frame.sizePolicy().hasHeightForWidth())
        self.track_frame.setSizePolicy(sizePolicy1)
        self.track_frame.setMinimumSize(QSize(0, 0))
        self.track_frame.setFrameShape(QFrame.StyledPanel)
        self.track_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.track_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.track_layout = QVBoxLayout()
        self.track_layout.setSpacing(2)
        self.track_layout.setObjectName("track_layout")

        self.horizontalLayout_2.addLayout(self.track_layout)

        self.splitter.addWidget(self.track_frame)

        self.verticalLayout_8.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 37))
        self.menuVideo = QMenu(self.menubar)
        self.menuVideo.setObjectName("menuVideo")
        self.menuAnnotation = QMenu(self.menubar)
        self.menuAnnotation.setObjectName("menuAnnotation")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuWindows = QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.behav_table_dock = DockWidget(MainWindow)
        self.behav_table_dock.setObjectName("behav_table_dock")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.behav_table_dock.sizePolicy().hasHeightForWidth()
        )
        self.behav_table_dock.setSizePolicy(sizePolicy2)
        self.behav_table_dock.setMinimumSize(QSize(328, 226))
        self.behav_table_dock.setFloating(False)
        self.behav_table_dock.setFeatures(
            QDockWidget.DockWidgetClosable
            | QDockWidget.DockWidgetFloatable
            | QDockWidget.DockWidgetMovable
        )
        self.behav_table_dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
        )
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.dockWidgetContents.sizePolicy().hasHeightForWidth()
        )
        self.dockWidgetContents.setSizePolicy(sizePolicy3)
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.control_layout = QVBoxLayout()
        self.control_layout.setObjectName("control_layout")
        self.control_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.annotation_tabs = QTabWidget(self.dockWidgetContents)
        self.annotation_tabs.setObjectName("annotation_tabs")
        self.annotation_tabs.setAcceptDrops(False)
        self.annotation_tabs.setTabShape(QTabWidget.Rounded)
        self.annotation_tabs.setMovable(True)
        self.behav_tab = QWidget()
        self.behav_tab.setObjectName("behav_tab")
        self.verticalLayout_6 = QVBoxLayout(self.behav_tab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.behavior_table = GenericTableView(self.behav_tab)
        self.behavior_table.setObjectName("behavior_table")
        sizePolicy1.setHeightForWidth(
            self.behavior_table.sizePolicy().hasHeightForWidth()
        )
        self.behavior_table.setSizePolicy(sizePolicy1)
        self.behavior_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.behavior_table.horizontalHeader().setMinimumSectionSize(20)
        self.behavior_table.verticalHeader().setVisible(False)

        self.verticalLayout_6.addWidget(self.behavior_table)

        self.annotation_tabs.addTab(self.behav_tab, "")
        self.stats_tab = QWidget()
        self.stats_tab.setObjectName("stats_tab")
        self.verticalLayout_3 = QVBoxLayout(self.stats_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.stats_table = GenericTableView(self.stats_tab)
        self.stats_table.setObjectName("stats_table")

        self.verticalLayout_3.addWidget(self.stats_table)

        self.annotation_tabs.addTab(self.stats_tab, "")

        self.control_layout.addWidget(self.annotation_tabs)

        self.verticalLayout_2.addLayout(self.control_layout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_behavior_button = QPushButton(self.dockWidgetContents)
        self.add_behavior_button.setObjectName("add_behavior_button")

        self.horizontalLayout.addWidget(self.add_behavior_button)

        self.delete_behavior_button = QPushButton(self.dockWidgetContents)
        self.delete_behavior_button.setObjectName("delete_behavior_button")

        self.horizontalLayout.addWidget(self.delete_behavior_button)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.behav_table_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.behav_table_dock)
        self.epoch_dock = DockWidget(MainWindow)
        self.epoch_dock.setObjectName("epoch_dock")
        self.epoch_dock.setMinimumSize(QSize(299, 150))
        self.epoch_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QTabWidget(self.dockWidgetContents_2)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.all_epoch = QWidget()
        self.all_epoch.setObjectName("all_epoch")
        self.verticalLayout = QVBoxLayout(self.all_epoch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stream_table_layout = QHBoxLayout()
        self.stream_table_layout.setSpacing(0)
        self.stream_table_layout.setObjectName("stream_table_layout")
        self.stream_table_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.verticalLayout.addLayout(self.stream_table_layout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.add_stream_button = QPushButton(self.all_epoch)
        self.add_stream_button.setObjectName("add_stream_button")

        self.horizontalLayout_9.addWidget(self.add_stream_button)

        self.delete_stream_button = QPushButton(self.all_epoch)
        self.delete_stream_button.setObjectName("delete_stream_button")

        self.horizontalLayout_9.addWidget(self.delete_stream_button)

        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalLayout.setStretch(0, 1)
        self.tabWidget.addTab(self.all_epoch, "")
        self.behavior_epoch = QWidget()
        self.behavior_epoch.setObjectName("behavior_epoch")
        self.horizontalLayout_4 = QHBoxLayout(self.behavior_epoch)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.behav_epoch_table_layout = QHBoxLayout()
        self.behav_epoch_table_layout.setSpacing(0)
        self.behav_epoch_table_layout.setObjectName("behav_epoch_table_layout")

        self.horizontalLayout_4.addLayout(self.behav_epoch_table_layout)

        self.tabWidget.addTab(self.behavior_epoch, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.epoch_dock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.epoch_dock)
        self.tracks_dock = DockWidget(MainWindow)
        self.tracks_dock.setObjectName("tracks_dock")
        self.tracks_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 2, -1, 2)
        self.full_tracks_layout = QVBoxLayout()
        self.full_tracks_layout.setObjectName("full_tracks_layout")

        self.verticalLayout_5.addLayout(self.full_tracks_layout)

        self.cur_behav_layout = QHBoxLayout()
        self.cur_behav_layout.setObjectName("cur_behav_layout")
        self.cur_behav_layout.setContentsMargins(10, -1, 10, -1)

        self.verticalLayout_5.addLayout(self.cur_behav_layout)

        self.tracks_dock.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.tracks_dock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuVideo.menuAction())
        self.menubar.addAction(self.menuAnnotation.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuVideo.addAction(self.actionOpen_video)
        self.menuVideo.addAction(self.actionAdd_seq)
        self.menuAnnotation.addAction(self.actionOpen_annotation)
        self.menuAnnotation.addAction(self.actionNew_annotation)
        self.menuAnnotation.addAction(self.actionSave_annotation)
        self.menuAnnotation.addAction(self.actionSave_annotation_as_MAT)
        self.menuAnnotation.addAction(self.actionClose_annotation)
        self.menuAnnotation.addSeparator()
        self.menuAnnotation.addAction(self.actionOpen_config)
        self.menuAnnotation.addAction(self.actionSave_config)
        self.menuAnnotation.addSeparator()
        self.menuAnnotation.addAction(self.actionAuto_save_annotation)
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionHelp)
        self.menuWindows.addAction(self.actionFull_annotation)
        self.menuWindows.addAction(self.actionBehavior_table)
        self.menuWindows.addAction(self.actionEpoch_table)
        self.menuWindows.addSeparator()
        self.menuWindows.addAction(self.actionTrack_epoch)
        self.menuWindows.addSeparator()
        self.menuWindows.addAction(self.actionShuffle_colors)

        self.retranslateUi(MainWindow)

        self.annotation_tabs.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.actionOpen_video.setText(
            QCoreApplication.translate("MainWindow", "Add video", None)
        )
        self.actionOpen_config.setText(
            QCoreApplication.translate("MainWindow", "Open config", None)
        )
        self.actionSave_config.setText(
            QCoreApplication.translate("MainWindow", "Save config", None)
        )
        self.actionOpen_annotation.setText(
            QCoreApplication.translate("MainWindow", "Open annotation", None)
        )
        self.actionSave_annotation.setText(
            QCoreApplication.translate("MainWindow", "Save annotation", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionNew_config.setText(
            QCoreApplication.translate("MainWindow", "New config", None)
        )
        self.actionFull_annotation.setText(
            QCoreApplication.translate("MainWindow", "Full annotation", None)
        )
        self.actionBehavior_table.setText(
            QCoreApplication.translate("MainWindow", "Behavior table", None)
        )
        self.actionEpoch_table.setText(
            QCoreApplication.translate("MainWindow", "Epoch table", None)
        )
        self.actionRemove_video.setText(
            QCoreApplication.translate("MainWindow", "Remove video/seq", None)
        )
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.actionReset.setText(
            QCoreApplication.translate("MainWindow", "Reset", None)
        )
        self.actionTips.setText(QCoreApplication.translate("MainWindow", "Tips", None))
        self.actionAdd_seq.setText(
            QCoreApplication.translate("MainWindow", "Add seq", None)
        )
        self.actionTrack_epoch.setText(
            QCoreApplication.translate("MainWindow", "Track epoch", None)
        )
        self.actionHelp.setText(
            QCoreApplication.translate("MainWindow", "Hot keys", None)
        )
        self.actionMerge_behaviors.setText(
            QCoreApplication.translate("MainWindow", "Merge behaviors", None)
        )
        self.actionAuto_save_annotation.setText(
            QCoreApplication.translate("MainWindow", "Auto save annotation", None)
        )
        self.actionMerge_behavior.setText(
            QCoreApplication.translate("MainWindow", "Merge behavior", None)
        )
        self.actionClose_annotation.setText(
            QCoreApplication.translate("MainWindow", "Close annotation", None)
        )
        self.actionNew_annotation.setText(
            QCoreApplication.translate("MainWindow", "New annotation", None)
        )
        self.actionShuffle_colors.setText(
            QCoreApplication.translate("MainWindow", "Shuffle colors", None)
        )
        self.actionSave_annotation_as_MAT.setText(
            QCoreApplication.translate("MainWindow", "Save annotation as MAT", None)
        )
        self.time_label.setText(
            QCoreApplication.translate("MainWindow", "00:00:00", None)
        )
        self.current_frame_label.setText(
            QCoreApplication.translate("MainWindow", "Frame", None)
        )
        self.play_button.setText(QCoreApplication.translate("MainWindow", "Play", None))
        self.pause_button.setText(
            QCoreApplication.translate("MainWindow", "Pause", None)
        )
        self.video_speed_label.setText(
            QCoreApplication.translate("MainWindow", "Speed", None)
        )
        self.track_window_label.setText(
            QCoreApplication.translate("MainWindow", "Track Window", None)
        )
        self.video_layout_label.setText(
            QCoreApplication.translate("MainWindow", "Video Layout", None)
        )
        self.video_layout_comboBox.setItemText(
            0, QCoreApplication.translate("MainWindow", "Side by Side", None)
        )
        self.video_layout_comboBox.setItemText(
            1, QCoreApplication.translate("MainWindow", "Stacked", None)
        )

        self.menuVideo.setTitle(QCoreApplication.translate("MainWindow", "Video", None))
        self.menuAnnotation.setTitle(
            QCoreApplication.translate("MainWindow", "Annotation", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "App", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuWindows.setTitle(
            QCoreApplication.translate("MainWindow", "View", None)
        )
        self.behav_table_dock.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Behaviors", None)
        )
        self.annotation_tabs.setTabText(
            self.annotation_tabs.indexOf(self.behav_tab),
            QCoreApplication.translate("MainWindow", "Behaviors", None),
        )
        self.annotation_tabs.setTabText(
            self.annotation_tabs.indexOf(self.stats_tab),
            QCoreApplication.translate("MainWindow", "Stats", None),
        )
        self.add_behavior_button.setText(
            QCoreApplication.translate("MainWindow", "Add behavior", None)
        )
        self.delete_behavior_button.setText(
            QCoreApplication.translate("MainWindow", "Delete behavior", None)
        )
        self.epoch_dock.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Epochs", None)
        )
        self.add_stream_button.setText(
            QCoreApplication.translate("MainWindow", "Add stream", None)
        )
        self.delete_stream_button.setText(
            QCoreApplication.translate("MainWindow", "Delete stream", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.all_epoch),
            QCoreApplication.translate("MainWindow", "All Epochs", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.behavior_epoch),
            QCoreApplication.translate("MainWindow", "Behavior Epochs", None),
        )
        self.tracks_dock.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Full annotation tracks", None)
        )

    # retranslateUi
