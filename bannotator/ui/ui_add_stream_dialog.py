# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_stream_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_AddStreamDialog(object):
    def setupUi(self, AddStreamDialog):
        if not AddStreamDialog.objectName():
            AddStreamDialog.setObjectName(u"AddStreamDialog")
        AddStreamDialog.resize(225, 112)
        self.verticalLayout = QVBoxLayout(AddStreamDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.streamID_label = QLabel(AddStreamDialog)
        self.streamID_label.setObjectName(u"streamID_label")

        self.gridLayout.addWidget(self.streamID_label, 0, 0, 1, 1)

        self.label = QLabel(AddStreamDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.comboBox = QComboBox(AddStreamDialog)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(AddStreamDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddStreamDialog)
        self.buttonBox.accepted.connect(AddStreamDialog.accept)
        self.buttonBox.rejected.connect(AddStreamDialog.reject)

        QMetaObject.connectSlotsByName(AddStreamDialog)
    # setupUi

    def retranslateUi(self, AddStreamDialog):
        AddStreamDialog.setWindowTitle(QCoreApplication.translate("AddStreamDialog", u"Add stream", None))
        self.streamID_label.setText(QCoreApplication.translate("AddStreamDialog", u"Stream ID: ", None))
        self.label.setText(QCoreApplication.translate("AddStreamDialog", u"Filled with ", None))
    # retranslateUi

