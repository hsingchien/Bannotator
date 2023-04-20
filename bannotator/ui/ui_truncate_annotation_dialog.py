# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'truncate_annotation_dialog.ui'
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
    QHBoxLayout, QLabel, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_TruncateAnnotationDialog(object):
    def setupUi(self, TruncateAnnotationDialog):
        if not TruncateAnnotationDialog.objectName():
            TruncateAnnotationDialog.setObjectName(u"TruncateAnnotationDialog")
        TruncateAnnotationDialog.resize(274, 179)
        self.verticalLayout = QVBoxLayout(TruncateAnnotationDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(TruncateAnnotationDialog)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.PlainText)
        self.label.setScaledContents(False)
        self.label.setIndent(0)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(TruncateAnnotationDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.from_spinbox = QSpinBox(TruncateAnnotationDialog)
        self.from_spinbox.setObjectName(u"from_spinbox")
        self.from_spinbox.setMinimum(1)

        self.horizontalLayout.addWidget(self.from_spinbox)

        self.label_3 = QLabel(TruncateAnnotationDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.to_spinbox = QSpinBox(TruncateAnnotationDialog)
        self.to_spinbox.setObjectName(u"to_spinbox")

        self.horizontalLayout.addWidget(self.to_spinbox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(TruncateAnnotationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TruncateAnnotationDialog)
        self.buttonBox.accepted.connect(TruncateAnnotationDialog.accept)
        self.buttonBox.rejected.connect(TruncateAnnotationDialog.reject)

        QMetaObject.connectSlotsByName(TruncateAnnotationDialog)
    # setupUi

    def retranslateUi(self, TruncateAnnotationDialog):
        TruncateAnnotationDialog.setWindowTitle(QCoreApplication.translate("TruncateAnnotationDialog", u"Is this the correct annotation?", None))
        self.label.setText(QCoreApplication.translate("TruncateAnnotationDialog", u"Annotation is longer than the video 1.\n"
"Truncate the annotation to match the length\n"
" OK to proceed. Cancel to abort", None))
        self.label_2.setText(QCoreApplication.translate("TruncateAnnotationDialog", u"From", None))
        self.label_3.setText(QCoreApplication.translate("TruncateAnnotationDialog", u"To", None))
    # retranslateUi

