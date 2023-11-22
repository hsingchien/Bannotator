# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_behavior_dialog.ui'
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
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_AddBehaviorDialog(object):
    def setupUi(self, AddBehaviorDialog):
        if not AddBehaviorDialog.objectName():
            AddBehaviorDialog.setObjectName(u"AddBehaviorDialog")
        AddBehaviorDialog.resize(206, 161)
        self.verticalLayout = QVBoxLayout(AddBehaviorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.name = QLabel(AddBehaviorDialog)
        self.name.setObjectName(u"name")

        self.gridLayout.addWidget(self.name, 0, 0, 1, 1)

        self.name_edit = QLineEdit(AddBehaviorDialog)
        self.name_edit.setObjectName(u"name_edit")

        self.gridLayout.addWidget(self.name_edit, 0, 1, 1, 1)

        self.keybind = QLabel(AddBehaviorDialog)
        self.keybind.setObjectName(u"keybind")

        self.gridLayout.addWidget(self.keybind, 1, 0, 1, 1)

        self.keybind_comboBox = QComboBox(AddBehaviorDialog)
        self.keybind_comboBox.setObjectName(u"keybind_comboBox")

        self.gridLayout.addWidget(self.keybind_comboBox, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(AddBehaviorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AddBehaviorDialog)
        self.buttonBox.accepted.connect(AddBehaviorDialog.accept)
        self.buttonBox.rejected.connect(AddBehaviorDialog.reject)

        QMetaObject.connectSlotsByName(AddBehaviorDialog)
    # setupUi

    def retranslateUi(self, AddBehaviorDialog):
        AddBehaviorDialog.setWindowTitle(QCoreApplication.translate("AddBehaviorDialog", u"Add behavior", None))
        self.name.setText(QCoreApplication.translate("AddBehaviorDialog", u"name", None))
        self.keybind.setText(QCoreApplication.translate("AddBehaviorDialog", u"keybind", None))
    # retranslateUi

