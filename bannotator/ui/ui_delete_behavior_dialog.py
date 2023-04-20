# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delete_behavior_dialog.ui'
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

class Ui_DeleteBehaviorDialog(object):
    def setupUi(self, DeleteBehaviorDialog):
        if not DeleteBehaviorDialog.objectName():
            DeleteBehaviorDialog.setObjectName(u"DeleteBehaviorDialog")
        DeleteBehaviorDialog.resize(304, 136)
        self.verticalLayout = QVBoxLayout(DeleteBehaviorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(DeleteBehaviorDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox = QComboBox(DeleteBehaviorDialog)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 2)

        self.label_3 = QLabel(DeleteBehaviorDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 2)

        self.comboBox_2 = QComboBox(DeleteBehaviorDialog)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(DeleteBehaviorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DeleteBehaviorDialog)
        self.buttonBox.accepted.connect(DeleteBehaviorDialog.accept)
        self.buttonBox.rejected.connect(DeleteBehaviorDialog.reject)

        QMetaObject.connectSlotsByName(DeleteBehaviorDialog)
    # setupUi

    def retranslateUi(self, DeleteBehaviorDialog):
        DeleteBehaviorDialog.setWindowTitle(QCoreApplication.translate("DeleteBehaviorDialog", u"Delete behavior", None))
        self.label.setText(QCoreApplication.translate("DeleteBehaviorDialog", u"Delete", None))
        self.label_3.setText(QCoreApplication.translate("DeleteBehaviorDialog", u"Its # epochs will be replaced with", None))
    # retranslateUi

