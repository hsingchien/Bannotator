# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delete_stream_dialog.ui'
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
    QDialogButtonBox, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_DeleteStreamDialog(object):
    def setupUi(self, DeleteStreamDialog):
        if not DeleteStreamDialog.objectName():
            DeleteStreamDialog.setObjectName(u"DeleteStreamDialog")
        DeleteStreamDialog.resize(199, 96)
        self.verticalLayout = QVBoxLayout(DeleteStreamDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(DeleteStreamDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.stream_combobox = QComboBox(DeleteStreamDialog)
        self.stream_combobox.setObjectName(u"stream_combobox")

        self.horizontalLayout.addWidget(self.stream_combobox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(DeleteStreamDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DeleteStreamDialog)
        self.buttonBox.accepted.connect(DeleteStreamDialog.accept)
        self.buttonBox.rejected.connect(DeleteStreamDialog.reject)

        QMetaObject.connectSlotsByName(DeleteStreamDialog)
    # setupUi

    def retranslateUi(self, DeleteStreamDialog):
        DeleteStreamDialog.setWindowTitle(QCoreApplication.translate("DeleteStreamDialog", u"Delete stream", None))
        self.label.setText(QCoreApplication.translate("DeleteStreamDialog", u"Stream ID", None))
    # retranslateUi

