# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merge_behavior_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QLineEdit, QSizePolicy,
    QWidget)

class Ui_MergeBehaviorDialog(object):
    def setupUi(self, MergeBehaviorDialog):
        if not MergeBehaviorDialog.objectName():
            MergeBehaviorDialog.setObjectName(u"MergeBehaviorDialog")
        MergeBehaviorDialog.resize(557, 300)
        self.buttonBox = QDialogButtonBox(MergeBehaviorDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.comboBox = QComboBox(MergeBehaviorDialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(60, 100, 69, 22))
        self.comboBox_2 = QComboBox(MergeBehaviorDialog)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(210, 100, 69, 22))
        self.lineEdit = QLineEdit(MergeBehaviorDialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(360, 100, 113, 22))
        self.checkBox = QCheckBox(MergeBehaviorDialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(70, 150, 76, 20))
        self.checkBox_2 = QCheckBox(MergeBehaviorDialog)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(70, 180, 76, 20))
        self.checkBox_3 = QCheckBox(MergeBehaviorDialog)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(210, 150, 76, 20))
        self.checkBox_4 = QCheckBox(MergeBehaviorDialog)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setGeometry(QRect(210, 180, 76, 20))

        self.retranslateUi(MergeBehaviorDialog)
        self.buttonBox.accepted.connect(MergeBehaviorDialog.accept)
        self.buttonBox.rejected.connect(MergeBehaviorDialog.reject)

        QMetaObject.connectSlotsByName(MergeBehaviorDialog)
    # setupUi

    def retranslateUi(self, MergeBehaviorDialog):
        MergeBehaviorDialog.setWindowTitle(QCoreApplication.translate("MergeBehaviorDialog", u"Dialog", None))
        self.checkBox.setText(QCoreApplication.translate("MergeBehaviorDialog", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("MergeBehaviorDialog", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("MergeBehaviorDialog", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("MergeBehaviorDialog", u"CheckBox", None))
    # retranslateUi

