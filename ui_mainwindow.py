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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QGraphicsView,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollBar, QSizePolicy, QSpinBox, QStackedWidget,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from dataview import GenericTableView
from widgets import (IntLineEdit, PlaySpeedSpinBox)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 768)
        self.actionOpen_video = QAction(MainWindow)
        self.actionOpen_video.setObjectName(u"actionOpen_video")
        self.actionOpen_config = QAction(MainWindow)
        self.actionOpen_config.setObjectName(u"actionOpen_config")
        self.actionCreate_new_config = QAction(MainWindow)
        self.actionCreate_new_config.setObjectName(u"actionCreate_new_config")
        self.actionOpen_annotation = QAction(MainWindow)
        self.actionOpen_annotation.setObjectName(u"actionOpen_annotation")
        self.actionSave_annotation = QAction(MainWindow)
        self.actionSave_annotation.setObjectName(u"actionSave_annotation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.display_layout = QVBoxLayout()
        self.display_layout.setObjectName(u"display_layout")
        self.vid1_view = QGraphicsView(self.centralwidget)
        self.vid1_view.setObjectName(u"vid1_view")

        self.display_layout.addWidget(self.vid1_view)

        self.video_scrollbar = QScrollBar(self.centralwidget)
        self.video_scrollbar.setObjectName(u"video_scrollbar")
        self.video_scrollbar.setMinimum(1)
        self.video_scrollbar.setMaximum(1000)
        self.video_scrollbar.setPageStep(500)
        self.video_scrollbar.setOrientation(Qt.Horizontal)

        self.display_layout.addWidget(self.video_scrollbar)

        self.track_frame = QFrame(self.centralwidget)
        self.track_frame.setObjectName(u"track_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.track_frame.sizePolicy().hasHeightForWidth())
        self.track_frame.setSizePolicy(sizePolicy)
        self.track_frame.setMinimumSize(QSize(0, 0))
        self.track_frame.setFrameShape(QFrame.StyledPanel)
        self.track_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.track_frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.track_layout = QVBoxLayout()
        self.track_layout.setObjectName(u"track_layout")

        self.horizontalLayout_10.addLayout(self.track_layout)


        self.display_layout.addWidget(self.track_frame)

        self.display_layout.setStretch(0, 16)
        self.display_layout.setStretch(1, 2)
        self.display_layout.setStretch(2, 4)

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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.horizontalLayout_11 = QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.control_layout = QVBoxLayout()
        self.control_layout.setObjectName(u"control_layout")
        self.annotation_tabs = QTabWidget(self.dockWidgetContents)
        self.annotation_tabs.setObjectName(u"annotation_tabs")
        self.behav_tab = QWidget()
        self.behav_tab.setObjectName(u"behav_tab")
        self.verticalLayout_2 = QVBoxLayout(self.behav_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.behavior_table = GenericTableView(self.behav_tab)
        self.behavior_table.setObjectName(u"behavior_table")
        self.behavior_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

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
        self.epoch_tab = QWidget()
        self.epoch_tab.setObjectName(u"epoch_tab")
        self.verticalLayout = QVBoxLayout(self.epoch_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stream_table_layout = QHBoxLayout()
        self.stream_table_layout.setSpacing(1)
        self.stream_table_layout.setObjectName(u"stream_table_layout")

        self.verticalLayout.addLayout(self.stream_table_layout)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_4 = QPushButton(self.epoch_tab)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_9.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.epoch_tab)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_9.addWidget(self.pushButton_3)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalLayout.setStretch(0, 8)
        self.annotation_tabs.addTab(self.epoch_tab, "")
        self.stats_tab = QWidget()
        self.stats_tab.setObjectName(u"stats_tab")
        self.verticalLayout_3 = QVBoxLayout(self.stats_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stats_table = GenericTableView(self.stats_tab)
        self.stats_table.setObjectName(u"stats_table")

        self.verticalLayout_3.addWidget(self.stats_table)

        self.annotation_tabs.addTab(self.stats_tab, "")

        self.control_layout.addWidget(self.annotation_tabs)

        self.control_widget = QStackedWidget(self.dockWidgetContents)
        self.control_widget.setObjectName(u"control_widget")
        self.control_widget.setAutoFillBackground(False)
        self.control_widget.setFrameShape(QFrame.NoFrame)
        self.control_widget.setFrameShadow(QFrame.Plain)
        self.control_widget.setLineWidth(3)
        self.stat_panel = QWidget()
        self.stat_panel.setObjectName(u"stat_panel")
        self.control_widget.addWidget(self.stat_panel)
        self.control_panel = QWidget()
        self.control_panel.setObjectName(u"control_panel")
        self.horizontalLayout_8 = QHBoxLayout(self.control_panel)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.play_button = QPushButton(self.control_panel)
        self.play_button.setObjectName(u"play_button")

        self.horizontalLayout_7.addWidget(self.play_button)

        self.pause_button = QPushButton(self.control_panel)
        self.pause_button.setObjectName(u"pause_button")

        self.horizontalLayout_7.addWidget(self.pause_button)


        self.gridLayout.addLayout(self.horizontalLayout_7, 2, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.control_panel)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.curframe_spinBox = QSpinBox(self.control_panel)
        self.curframe_spinBox.setObjectName(u"curframe_spinBox")
        self.curframe_spinBox.setMinimum(1)
        self.curframe_spinBox.setMaximum(100)

        self.horizontalLayout_4.addWidget(self.curframe_spinBox)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.control_panel)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextFormat(Qt.PlainText)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.time_label = QLabel(self.control_panel)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setTextFormat(Qt.MarkdownText)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.time_label)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 2, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.control_panel)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.trackwindow_lineEdit = IntLineEdit(self.control_panel)
        self.trackwindow_lineEdit.setObjectName(u"trackwindow_lineEdit")
        self.trackwindow_lineEdit.setMaxLength(6)

        self.horizontalLayout_6.addWidget(self.trackwindow_lineEdit)


        self.gridLayout.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.control_panel)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.speed_doubleSpinBox = PlaySpeedSpinBox(self.control_panel)
        self.speed_doubleSpinBox.setObjectName(u"speed_doubleSpinBox")
        self.speed_doubleSpinBox.setMinimum(-10.000000000000000)
        self.speed_doubleSpinBox.setMaximum(10.000000000000000)
        self.speed_doubleSpinBox.setSingleStep(0.100000000000000)
        self.speed_doubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.speed_doubleSpinBox)


        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 3)

        self.horizontalLayout_8.addLayout(self.gridLayout)

        self.control_widget.addWidget(self.control_panel)

        self.control_layout.addWidget(self.control_widget)

        self.control_layout.setStretch(0, 3)
        self.control_layout.setStretch(1, 1)

        self.horizontalLayout_11.addLayout(self.control_layout)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuVideo.menuAction())
        self.menubar.addAction(self.menuAnnotation.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuVideo.addAction(self.actionOpen_video)
        self.menuAnnotation.addAction(self.actionOpen_annotation)
        self.menuAnnotation.addAction(self.actionSave_annotation)
        self.menuAnnotation.addSeparator()
        self.menuAnnotation.addAction(self.actionOpen_config)
        self.menuAnnotation.addAction(self.actionCreate_new_config)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.annotation_tabs.setCurrentIndex(0)
        self.control_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_video.setText(QCoreApplication.translate("MainWindow", u"Open video", None))
        self.actionOpen_config.setText(QCoreApplication.translate("MainWindow", u"Open config", None))
        self.actionCreate_new_config.setText(QCoreApplication.translate("MainWindow", u"Save config", None))
        self.actionOpen_annotation.setText(QCoreApplication.translate("MainWindow", u"Open annotation", None))
        self.actionSave_annotation.setText(QCoreApplication.translate("MainWindow", u"Save annotation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuVideo.setTitle(QCoreApplication.translate("MainWindow", u"Video", None))
        self.menuAnnotation.setTitle(QCoreApplication.translate("MainWindow", u"Annotation", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Add behavior", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete behavior", None))
        self.annotation_tabs.setTabText(self.annotation_tabs.indexOf(self.behav_tab), QCoreApplication.translate("MainWindow", u"Behaviors", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Add stream", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Delete stream", None))
        self.annotation_tabs.setTabText(self.annotation_tabs.indexOf(self.epoch_tab), QCoreApplication.translate("MainWindow", u"Epochs", None))
        self.annotation_tabs.setTabText(self.annotation_tabs.indexOf(self.stats_tab), QCoreApplication.translate("MainWindow", u"Stats", None))
        self.play_button.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Current Frame", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Track Window", None))
        self.trackwindow_lineEdit.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
    # retranslateUi

