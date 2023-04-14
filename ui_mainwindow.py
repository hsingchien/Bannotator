# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main-window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from dataview import GenericTableView
from widgets import (BehavVideoView, DockWidget, PlaySpeedSpinBox, TabWidget,
    VideoSlider)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 768)
        self.actionOpen_video = QAction(MainWindow)
        self.actionOpen_video.setObjectName(u"actionOpen_video")
        self.actionOpen_config = QAction(MainWindow)
        self.actionOpen_config.setObjectName(u"actionOpen_config")
        self.actionSave_config = QAction(MainWindow)
        self.actionSave_config.setObjectName(u"actionSave_config")
        self.actionOpen_annotation = QAction(MainWindow)
        self.actionOpen_annotation.setObjectName(u"actionOpen_annotation")
        self.actionSave_annotation = QAction(MainWindow)
        self.actionSave_annotation.setObjectName(u"actionSave_annotation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionNew_annotation = QAction(MainWindow)
        self.actionNew_annotation.setObjectName(u"actionNew_annotation")
        self.actionNew_config = QAction(MainWindow)
        self.actionNew_config.setObjectName(u"actionNew_config")
        self.actionFull_annotation = QAction(MainWindow)
        self.actionFull_annotation.setObjectName(u"actionFull_annotation")
        self.actionFull_annotation.setCheckable(True)
        self.actionFull_annotation.setChecked(True)
        self.actionBehavior_table = QAction(MainWindow)
        self.actionBehavior_table.setObjectName(u"actionBehavior_table")
        self.actionBehavior_table.setCheckable(True)
        self.actionBehavior_table.setChecked(True)
        self.actionEpoch_table = QAction(MainWindow)
        self.actionEpoch_table.setObjectName(u"actionEpoch_table")
        self.actionEpoch_table.setCheckable(True)
        self.actionEpoch_table.setChecked(True)
        self.actionRemove_video = QAction(MainWindow)
        self.actionRemove_video.setObjectName(u"actionRemove_video")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionReset = QAction(MainWindow)
        self.actionReset.setObjectName(u"actionReset")
        self.actionTips = QAction(MainWindow)
        self.actionTips.setObjectName(u"actionTips")
        self.actionAdd_seq = QAction(MainWindow)
        self.actionAdd_seq.setObjectName(u"actionAdd_seq")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.display_layout = QVBoxLayout()
        self.display_layout.setObjectName(u"display_layout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextFormat(Qt.PlainText)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_12.addWidget(self.label_4)

        self.time_label = QLabel(self.centralwidget)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setTextFormat(Qt.MarkdownText)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.time_label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_12.addWidget(self.label_2)

        self.curframe_spinBox = QSpinBox(self.centralwidget)
        self.curframe_spinBox.setObjectName(u"curframe_spinBox")
        self.curframe_spinBox.setMinimum(1)
        self.curframe_spinBox.setMaximum(1000)

        self.horizontalLayout_12.addWidget(self.curframe_spinBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.play_button = QPushButton(self.centralwidget)
        self.play_button.setObjectName(u"play_button")

        self.horizontalLayout_12.addWidget(self.play_button)

        self.pause_button = QPushButton(self.centralwidget)
        self.pause_button.setObjectName(u"pause_button")

        self.horizontalLayout_12.addWidget(self.pause_button)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_12.addWidget(self.label_3)

        self.speed_doubleSpinBox = PlaySpeedSpinBox(self.centralwidget)
        self.speed_doubleSpinBox.setObjectName(u"speed_doubleSpinBox")
        self.speed_doubleSpinBox.setMinimum(-10.000000000000000)
        self.speed_doubleSpinBox.setMaximum(10.000000000000000)
        self.speed_doubleSpinBox.setSingleStep(0.100000000000000)
        self.speed_doubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_12.addWidget(self.speed_doubleSpinBox)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_12.addWidget(self.label)

        self.track_window_spinbox = QSpinBox(self.centralwidget)
        self.track_window_spinbox.setObjectName(u"track_window_spinbox")
        self.track_window_spinbox.setMinimum(1)
        self.track_window_spinbox.setMaximum(1000)
        self.track_window_spinbox.setValue(500)

        self.horizontalLayout_12.addWidget(self.track_window_spinbox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_2)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_12.addWidget(self.label_5)

        self.video_layout_comboBox = QComboBox(self.centralwidget)
        self.video_layout_comboBox.addItem("")
        self.video_layout_comboBox.addItem("")
        self.video_layout_comboBox.setObjectName(u"video_layout_comboBox")

        self.horizontalLayout_12.addWidget(self.video_layout_comboBox)

        self.horizontalLayout_12.setStretch(1, 1)
        self.horizontalLayout_12.setStretch(3, 1)
        self.horizontalLayout_12.setStretch(4, 1)
        self.horizontalLayout_12.setStretch(8, 1)
        self.horizontalLayout_12.setStretch(10, 1)
        self.horizontalLayout_12.setStretch(11, 1)
        self.horizontalLayout_12.setStretch(13, 1)

        self.display_layout.addLayout(self.horizontalLayout_12)

        self.video_layout = QHBoxLayout()
        self.video_layout.setObjectName(u"video_layout")
        self.vid1_view = BehavVideoView(self.centralwidget)
        self.vid1_view.setObjectName(u"vid1_view")

        self.video_layout.addWidget(self.vid1_view)


        self.display_layout.addLayout(self.video_layout)

        self.video_slider = VideoSlider(self.centralwidget)
        self.video_slider.setObjectName(u"video_slider")
        self.video_slider.setStyleSheet(u"QSlider::groove:horizontal {\n"
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
"}")
        self.video_slider.setMinimum(1)
        self.video_slider.setMaximum(1000)
        self.video_slider.setValue(1)
        self.video_slider.setOrientation(Qt.Horizontal)
        self.video_slider.setTickPosition(QSlider.NoTicks)

        self.display_layout.addWidget(self.video_slider)

        self.track_frame = QFrame(self.centralwidget)
        self.track_frame.setObjectName(u"track_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.track_frame.sizePolicy().hasHeightForWidth())
        self.track_frame.setSizePolicy(sizePolicy1)
        self.track_frame.setMinimumSize(QSize(0, 0))
        self.track_frame.setFrameShape(QFrame.StyledPanel)
        self.track_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.track_frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.track_layout = QVBoxLayout()
        self.track_layout.setObjectName(u"track_layout")

        self.horizontalLayout_10.addLayout(self.track_layout)


        self.display_layout.addWidget(self.track_frame)

        self.display_layout.setStretch(0, 1)
        self.display_layout.setStretch(1, 16)
        self.display_layout.setStretch(3, 4)

        self.horizontalLayout_2.addLayout(self.display_layout)

        self.horizontalLayout_2.setStretch(0, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 22))
        self.menuVideo = QMenu(self.menubar)
        self.menuVideo.setObjectName(u"menuVideo")
        self.menuAnnotation = QMenu(self.menubar)
        self.menuAnnotation.setObjectName(u"menuAnnotation")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuWindows = QMenu(self.menubar)
        self.menuWindows.setObjectName(u"menuWindows")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.behav_table_dock = DockWidget(MainWindow)
        self.behav_table_dock.setObjectName(u"behav_table_dock")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.behav_table_dock.sizePolicy().hasHeightForWidth())
        self.behav_table_dock.setSizePolicy(sizePolicy2)
        self.behav_table_dock.setMinimumSize(QSize(328, 226))
        self.behav_table_dock.setFloating(False)
        self.behav_table_dock.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.behav_table_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy3)
        self.horizontalLayout_11 = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.control_layout = QVBoxLayout()
        self.control_layout.setObjectName(u"control_layout")
        self.control_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.annotation_tabs = TabWidget(self.dockWidgetContents)
        self.annotation_tabs.setObjectName(u"annotation_tabs")
        self.annotation_tabs.setAcceptDrops(False)
        self.annotation_tabs.setTabShape(QTabWidget.Rounded)
        self.annotation_tabs.setMovable(True)
        self.behav_tab = QWidget()
        self.behav_tab.setObjectName(u"behav_tab")
        self.verticalLayout_2 = QVBoxLayout(self.behav_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.behavior_table = GenericTableView(self.behav_tab)
        self.behavior_table.setObjectName(u"behavior_table")
        sizePolicy1.setHeightForWidth(self.behavior_table.sizePolicy().hasHeightForWidth())
        self.behavior_table.setSizePolicy(sizePolicy1)
        self.behavior_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.behavior_table.horizontalHeader().setMinimumSectionSize(20)
        self.behavior_table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.behavior_table)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(self.behav_tab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.behav_tab)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.annotation_tabs.addTab(self.behav_tab, "")
        self.stats_tab = QWidget()
        self.stats_tab.setObjectName(u"stats_tab")
        self.verticalLayout_3 = QVBoxLayout(self.stats_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stats_table = GenericTableView(self.stats_tab)
        self.stats_table.setObjectName(u"stats_table")

        self.verticalLayout_3.addWidget(self.stats_table)

        self.annotation_tabs.addTab(self.stats_tab, "")

        self.control_layout.addWidget(self.annotation_tabs)

        self.control_layout.setStretch(0, 3)

        self.horizontalLayout_11.addLayout(self.control_layout)

        self.behav_table_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.behav_table_dock)
        self.epoch_dock = DockWidget(MainWindow)
        self.epoch_dock.setObjectName(u"epoch_dock")
        self.epoch_dock.setMinimumSize(QSize(299, 150))
        self.epoch_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tabWidget = QTabWidget(self.dockWidgetContents_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.all_epoch = QWidget()
        self.all_epoch.setObjectName(u"all_epoch")
        self.verticalLayout = QVBoxLayout(self.all_epoch)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stream_table_layout = QHBoxLayout()
        self.stream_table_layout.setSpacing(0)
        self.stream_table_layout.setObjectName(u"stream_table_layout")
        self.stream_table_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.verticalLayout.addLayout(self.stream_table_layout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.pushButton_4 = QPushButton(self.all_epoch)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_9.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.all_epoch)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_9.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalLayout.setStretch(0, 1)
        self.tabWidget.addTab(self.all_epoch, "")
        self.behavior_epoch = QWidget()
        self.behavior_epoch.setObjectName(u"behavior_epoch")
        self.horizontalLayout_4 = QHBoxLayout(self.behavior_epoch)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.behav_epoch_table_layout = QHBoxLayout()
        self.behav_epoch_table_layout.setObjectName(u"behav_epoch_table_layout")

        self.horizontalLayout_4.addLayout(self.behav_epoch_table_layout)

        self.tabWidget.addTab(self.behavior_epoch, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.epoch_dock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.epoch_dock)
        self.tracks_dock = DockWidget(MainWindow)
        self.tracks_dock.setObjectName(u"tracks_dock")
        self.tracks_dock.setAllowedAreas(Qt.BottomDockWidgetArea|Qt.TopDockWidgetArea)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.horizontalLayout_5 = QHBoxLayout(self.dockWidgetContents_4)
        self.horizontalLayout_5.setSpacing(3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 2, -1, 2)
        self.full_tracks_layout = QVBoxLayout()
        self.full_tracks_layout.setObjectName(u"full_tracks_layout")

        self.horizontalLayout_5.addLayout(self.full_tracks_layout)

        self.tracks_dock.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.tracks_dock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuVideo.menuAction())
        self.menubar.addAction(self.menuAnnotation.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuVideo.addAction(self.actionOpen_video)
        self.menuVideo.addAction(self.actionAdd_seq)
        self.menuVideo.addSeparator()
        self.menuVideo.addAction(self.actionRemove_video)
        self.menuAnnotation.addAction(self.actionOpen_annotation)
        self.menuAnnotation.addAction(self.actionSave_annotation)
        self.menuAnnotation.addAction(self.actionNew_annotation)
        self.menuAnnotation.addSeparator()
        self.menuAnnotation.addAction(self.actionOpen_config)
        self.menuAnnotation.addAction(self.actionSave_config)
        self.menuAnnotation.addAction(self.actionNew_config)
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionTips)
        self.menuWindows.addAction(self.actionFull_annotation)
        self.menuWindows.addAction(self.actionBehavior_table)
        self.menuWindows.addAction(self.actionEpoch_table)

        self.retranslateUi(MainWindow)

        self.annotation_tabs.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_video.setText(QCoreApplication.translate("MainWindow", u"Add video", None))
        self.actionOpen_config.setText(QCoreApplication.translate("MainWindow", u"Open config", None))
        self.actionSave_config.setText(QCoreApplication.translate("MainWindow", u"Save config", None))
        self.actionOpen_annotation.setText(QCoreApplication.translate("MainWindow", u"Open annotation", None))
        self.actionSave_annotation.setText(QCoreApplication.translate("MainWindow", u"Save annotation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionNew_annotation.setText(QCoreApplication.translate("MainWindow", u"New annotation", None))
        self.actionNew_config.setText(QCoreApplication.translate("MainWindow", u"New config", None))
        self.actionFull_annotation.setText(QCoreApplication.translate("MainWindow", u"Full annotation", None))
        self.actionBehavior_table.setText(QCoreApplication.translate("MainWindow", u"Behavior table", None))
        self.actionEpoch_table.setText(QCoreApplication.translate("MainWindow", u"Epoch table", None))
        self.actionRemove_video.setText(QCoreApplication.translate("MainWindow", u"Remove video/seq", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.actionTips.setText(QCoreApplication.translate("MainWindow", u"Tips", None))
        self.actionAdd_seq.setText(QCoreApplication.translate("MainWindow", u"Add seq", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Current Frame", None))
        self.play_button.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Track Window", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Video Layout", None))
        self.video_layout_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Side by Side", None))
        self.video_layout_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Stacked", None))

        self.menuVideo.setTitle(QCoreApplication.translate("MainWindow", u"Video", None))
        self.menuAnnotation.setTitle(QCoreApplication.translate("MainWindow", u"Annotation", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuWindows.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.behav_table_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Behaviors", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Add behavior", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete behavior", None))
        self.annotation_tabs.setTabText(self.annotation_tabs.indexOf(self.behav_tab), QCoreApplication.translate("MainWindow", u"Behaviors", None))
        self.annotation_tabs.setTabText(self.annotation_tabs.indexOf(self.stats_tab), QCoreApplication.translate("MainWindow", u"Stats", None))
        self.epoch_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Epochs", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Add stream", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Delete stream", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.all_epoch), QCoreApplication.translate("MainWindow", u"All Epochs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.behavior_epoch), QCoreApplication.translate("MainWindow", u"Behavior Epochs", None))
        self.tracks_dock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Full annotation tracks", None))
    # retranslateUi

