# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_annotation_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_NewAnnotationDialog(object):
    def setupUi(self, NewAnnotationDialog):
        if not NewAnnotationDialog.objectName():
            NewAnnotationDialog.setObjectName(u"NewAnnotationDialog")
        NewAnnotationDialog.resize(267, 417)
        NewAnnotationDialog.setStyleSheet(u"QWidget { background-color: rgb(89, 89, 89); color: white }")
        self.verticalLayout = QVBoxLayout(NewAnnotationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.nStream_label = QLabel(NewAnnotationDialog)
        self.nStream_label.setObjectName(u"nStream_label")

        self.gridLayout.addWidget(self.nStream_label, 0, 0, 1, 1)

        self.nStream_spinBox = QSpinBox(NewAnnotationDialog)
        self.nStream_spinBox.setObjectName(u"nStream_spinBox")
        self.nStream_spinBox.setMinimum(1)
        self.nStream_spinBox.setMaximum(100)

        self.gridLayout.addWidget(self.nStream_spinBox, 0, 1, 1, 1)

        self.behavior_label = QLabel(NewAnnotationDialog)
        self.behavior_label.setObjectName(u"behavior_label")

        self.gridLayout.addWidget(self.behavior_label, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.behavior_text_edit = QPlainTextEdit(NewAnnotationDialog)
        self.behavior_text_edit.setObjectName(u"behavior_text_edit")

        self.gridLayout.addWidget(self.behavior_text_edit, 2, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(NewAnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewAnnotationDialog)
        self.buttonBox.accepted.connect(NewAnnotationDialog.accept)
        self.buttonBox.rejected.connect(NewAnnotationDialog.reject)

        QMetaObject.connectSlotsByName(NewAnnotationDialog)
    # setupUi

    def retranslateUi(self, NewAnnotationDialog):
        NewAnnotationDialog.setWindowTitle(QCoreApplication.translate("NewAnnotationDialog", u"Create new annotation", None))
        self.nStream_label.setText(QCoreApplication.translate("NewAnnotationDialog", u"number of streams", None))
        self.behavior_label.setText(QCoreApplication.translate("NewAnnotationDialog", u"Behavior - keybind:", None))
    # retranslateUi

