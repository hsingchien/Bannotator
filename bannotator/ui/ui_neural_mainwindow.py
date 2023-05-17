# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'neural_mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

from bannotator.widgets import TraceAxis

class Ui_NeuralWindow(object):
    def setupUi(self, NeuralWindow):
        if not NeuralWindow.objectName():
            NeuralWindow.setObjectName(u"NeuralWindow")
        NeuralWindow.resize(912, 600)
        self.actionImportNeuralRecord = QAction(NeuralWindow)
        self.actionImportNeuralRecord.setObjectName(u"actionImportNeuralRecord")
        self.actionResetNeuralRecording = QAction(NeuralWindow)
        self.actionResetNeuralRecording.setObjectName(u"actionResetNeuralRecording")
        self.centralwidget = QWidget(NeuralWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.trace_stream_combobox = QComboBox(self.centralwidget)
        self.trace_stream_combobox.setObjectName(u"trace_stream_combobox")

        self.horizontalLayout.addWidget(self.trace_stream_combobox)

        self.import_recording = QPushButton(self.centralwidget)
        self.import_recording.setObjectName(u"import_recording")

        self.horizontalLayout.addWidget(self.import_recording)

        self.reset_recording = QPushButton(self.centralwidget)
        self.reset_recording.setObjectName(u"reset_recording")

        self.horizontalLayout.addWidget(self.reset_recording)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.full_trace_push_button = QPushButton(self.centralwidget)
        self.full_trace_push_button.setObjectName(u"full_trace_push_button")
        self.full_trace_push_button.setCheckable(True)

        self.horizontalLayout.addWidget(self.full_trace_push_button)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.space_spinbox = QSpinBox(self.centralwidget)
        self.space_spinbox.setObjectName(u"space_spinbox")
        self.space_spinbox.setValue(2)

        self.horizontalLayout.addWidget(self.space_spinbox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.trace_view = TraceAxis(self.centralwidget)
        self.trace_view.setObjectName(u"trace_view")

        self.verticalLayout.addWidget(self.trace_view)

        self.avg_trace_view = TraceAxis(self.centralwidget)
        self.avg_trace_view.setObjectName(u"avg_trace_view")

        self.verticalLayout.addWidget(self.avg_trace_view)

        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.behavior_groupbox = QGroupBox(self.centralwidget)
        self.behavior_groupbox.setObjectName(u"behavior_groupbox")
        self.verticalLayout_4 = QVBoxLayout(self.behavior_groupbox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.behavior_scrollarea = QScrollArea(self.behavior_groupbox)
        self.behavior_scrollarea.setObjectName(u"behavior_scrollarea")
        self.behavior_scrollarea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 105, 510))
        self.behavior_scrollarea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.behavior_scrollarea)


        self.horizontalLayout_2.addWidget(self.behavior_groupbox)

        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        NeuralWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(NeuralWindow)

        QMetaObject.connectSlotsByName(NeuralWindow)
    # setupUi

    def retranslateUi(self, NeuralWindow):
        NeuralWindow.setWindowTitle(QCoreApplication.translate("NeuralWindow", u"MainWindow", None))
        self.actionImportNeuralRecord.setText(QCoreApplication.translate("NeuralWindow", u"Import neural recording", None))
        self.actionResetNeuralRecording.setText(QCoreApplication.translate("NeuralWindow", u"Clear neural recording", None))
        self.label.setText(QCoreApplication.translate("NeuralWindow", u"Stream", None))
        self.import_recording.setText(QCoreApplication.translate("NeuralWindow", u"Import", None))
        self.reset_recording.setText(QCoreApplication.translate("NeuralWindow", u"Reset", None))
        self.pushButton_2.setText(QCoreApplication.translate("NeuralWindow", u"Sort/Cluster", None))
        self.full_trace_push_button.setText(QCoreApplication.translate("NeuralWindow", u"Full trace", None))
        self.label_2.setText(QCoreApplication.translate("NeuralWindow", u"Space", None))
        self.behavior_groupbox.setTitle(QCoreApplication.translate("NeuralWindow", u"Behaviors", None))
    # retranslateUi

