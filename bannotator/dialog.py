from PySide6.QtWidgets import QInputDialog, QDialog, QDialogButtonBox
from bannotator.ui import *
class CropAnnotationDialog(QInputDialog):
    def __init__(self, annot_length, vid_length, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setInputMode(QInputDialog.IntInput)
        self.setIntMinimum(1)
        self.setIntMaximum(annot_length-vid_length+1)
    def showDialog(self):
        int_input, ok = self.getInt(self, "Is this the correct annotation?", "Annotation is longer than the video 1.\nTruncate the annotation from\n OK to proceed. Cancel to abort")
        return int_input, ok

class AddBehaviorDialog(QDialog, Ui_AddBehaviorDialog):
    def __init__(self, annotation = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        behavior_list = annotation.get_behaviors()
        self.all_names = [behav.name for behav in behavior_list[0]]
        all_key_binds = [behav.get_keybind() for behav in behavior_list[0]]
        letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
        available_strokes = [l for l in letters if l not in all_key_binds] + [" "]
        self.keybind_comboBox.addItems(available_strokes)
        self.keybind_comboBox.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.name_edit.textChanged.connect(self.validate_name)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    def get_input(self):
        if self.exec() == QDialog.Accepted:
            name = self.name_edit.text()
            keybind = self.keybind_comboBox.currentText()
            return (name, keybind)
        else:
            return (None,None)
        
    def validate_name(self, user_input):
        if user_input and user_input not in self.all_names:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


