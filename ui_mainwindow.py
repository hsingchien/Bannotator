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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QGraphicsView,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollBar, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

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
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.curframe_spinBox = QSpinBox(self.frame)
        self.curframe_spinBox.setObjectName(u"curframe_spinBox")

        self.horizontalLayout_3.addWidget(self.curframe_spinBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.framewindow_lineEdit = QLineEdit(self.frame)
        self.framewindow_lineEdit.setObjectName(u"framewindow_lineEdit")
        self.framewindow_lineEdit.setMaxLength(6)

        self.horizontalLayout_3.addWidget(self.framewindow_lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.speed_doubleSpinBox = QDoubleSpinBox(self.frame)
        self.speed_doubleSpinBox.setObjectName(u"speed_doubleSpinBox")

        self.horizontalLayout_3.addWidget(self.speed_doubleSpinBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextFormat(Qt.PlainText)
        self.label_4.setScaledContents(False)
        self.label_4.setTextInteractionFlags(Qt.NoTextInteraction)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.time_label = QLabel(self.frame)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setTextFormat(Qt.PlainText)

        self.horizontalLayout_3.addWidget(self.time_label)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(3, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.horizontalLayout_3.setStretch(5, 4)
        self.horizontalLayout_3.setStretch(6, 1)
        self.horizontalLayout_3.setStretch(7, 1)
        self.horizontalLayout_3.setStretch(9, 1)
        self.horizontalLayout_3.setStretch(10, 1)

        self.verticalLayout_4.addWidget(self.frame)

        self.vid1_view = QGraphicsView(self.centralwidget)
        self.vid1_view.setObjectName(u"vid1_view")

        self.verticalLayout_4.addWidget(self.vid1_view)

        self.video_scrollbar = QScrollBar(self.centralwidget)
        self.video_scrollbar.setObjectName(u"video_scrollbar")
        self.video_scrollbar.setPageStep(10)
        self.video_scrollbar.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.video_scrollbar)

        self.track_view = QGraphicsView(self.centralwidget)
        self.track_view.setObjectName(u"track_view")

        self.verticalLayout_4.addWidget(self.track_view)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 16)
        self.verticalLayout_4.setStretch(2, 2)
        self.verticalLayout_4.setStretch(3, 6)

        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.control_layout = QVBoxLayout()
        self.control_layout.setObjectName(u"control_layout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.behav_tab = QWidget()
        self.behav_tab.setObjectName(u"behav_tab")
        self.verticalLayout_2 = QVBoxLayout(self.behav_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableView = QTableView(self.behav_tab)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(self.behav_tab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.behav_tab)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.behav_tab, "")
        self.epoch_tab = QWidget()
        self.epoch_tab.setObjectName(u"epoch_tab")
        self.verticalLayout = QVBoxLayout(self.epoch_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView_2 = QTableView(self.epoch_tab)
        self.tableView_2.setObjectName(u"tableView_2")

        self.verticalLayout.addWidget(self.tableView_2)

        self.tabWidget.addTab(self.epoch_tab, "")
        self.stats_tab = QWidget()
        self.stats_tab.setObjectName(u"stats_tab")
        self.verticalLayout_3 = QVBoxLayout(self.stats_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView_3 = QTableView(self.stats_tab)
        self.tableView_3.setObjectName(u"tableView_3")

        self.verticalLayout_3.addWidget(self.tableView_3)

        self.tabWidget.addTab(self.stats_tab, "")

        self.control_layout.addWidget(self.tabWidget)

        self.control_widget = QStackedWidget(self.centralwidget)
        self.control_widget.setObjectName(u"control_widget")
        self.control_widget.setFrameShape(QFrame.NoFrame)
        self.control_widget.setFrameShadow(QFrame.Plain)
        self.control_widget.setLineWidth(3)
        self.control_panel = QWidget()
        self.control_panel.setObjectName(u"control_panel")
        self.control_widget.addWidget(self.control_panel)
        self.stat_panel = QWidget()
        self.stat_panel.setObjectName(u"stat_panel")
        self.control_widget.addWidget(self.stat_panel)

        self.control_layout.addWidget(self.control_widget)

        self.control_layout.setStretch(0, 3)
        self.control_layout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.control_layout)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
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

        self.tabWidget.setCurrentIndex(0)
        self.control_widget.setCurrentIndex(0)


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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Current Frame", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Frame Window", None))
        self.framewindow_lineEdit.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"00:00", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.behav_tab), QCoreApplication.translate("MainWindow", u"Behaviors", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.epoch_tab), QCoreApplication.translate("MainWindow", u"Epochs", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stats_tab), QCoreApplication.translate("MainWindow", u"Stats", None))
        self.menuVideo.setTitle(QCoreApplication.translate("MainWindow", u"Video", None))
        self.menuAnnotation.setTitle(QCoreApplication.translate("MainWindow", u"Annotation", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

