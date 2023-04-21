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

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.behavior_combobox = QComboBox(DeleteBehaviorDialog)
        self.behavior_combobox.setObjectName(u"behavior_combobox")

        self.gridLayout.addWidget(self.behavior_combobox, 0, 2, 1, 1)

        self.num_epochs_label = QLabel(DeleteBehaviorDialog)
        self.num_epochs_label.setObjectName(u"num_epochs_label")

        self.gridLayout.addWidget(self.num_epochs_label, 1, 0, 1, 1)

        self.epoch_info_label = QLabel(DeleteBehaviorDialog)
        self.epoch_info_label.setObjectName(u"epoch_info_label")

        self.gridLayout.addWidget(self.epoch_info_label, 1, 1, 1, 2)

        self.replace_behavior_combobox = QComboBox(DeleteBehaviorDialog)
        self.replace_behavior_combobox.setObjectName(u"replace_behavior_combobox")

        self.gridLayout.addWidget(self.replace_behavior_combobox, 1, 3, 1, 1)


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
        self.num_epochs_label.setText(QCoreApplication.translate("DeleteBehaviorDialog", u"TextLabel", None))
        self.epoch_info_label.setText(QCoreApplication.translate("DeleteBehaviorDialog", u"epochs will be merged into", None))
    # retranslateUi

