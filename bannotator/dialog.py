from PySide6.QtWidgets import QInputDialog, QDialog, QDialogButtonBox
from bannotator.ui import *
class TruncateAnnotationDialog(QDialog, Ui_TruncateAnnotationDialog):
    def __init__(self, annot_length, vid_length, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.from_spinbox.setMaximum(annot_length-vid_length+1)
        self.from_spinbox.setMinimum(1)
        self.to_spinbox.setMinimum(vid_length)
        self.to_spinbox.setMaximum(annot_length)
        self.to_spinbox.valueChanged.connect(lambda x: self.from_spinbox.setValue(x-vid_length+1))
        self.from_spinbox.valueChanged.connect(lambda x: self.to_spinbox.setValue(x+vid_length-1))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    def get_input(self):
        if self.exec() == QDialog.Accepted:
            from_value = self.from_spinbox.value()
            to_value = self.to_spinbox.value()
            return (from_value, to_value)
        else:
            return (None,None)


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

class DeleteBehaviorDialog(QDialog, Ui_DeleteBehaviorDialog):
    def __init__(self, annotation = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        behavior_list = annotation.get_behaviors()
        all_behavior_names = [behav.name for behav in behavior_list[0]]
        self.behavior_combobox.addItems(all_behavior_names)
        self.replace_behavior_combobox.addItems(all_behavior_names)
        self.behavior_combobox.setCurrentIndex(0)
        self.replace_behavior_combobox.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.behavior_combobox.currentTextChanged.connect(self.validate_input)
        self.replace_behavior_combobox.currentTextChanged.connect(self.validate_input)
        
    def validate_input(self):
        if self.replace_behavior_combobox.currentText() == self.behavior_combobox.currentText():
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            
    def get_input(self):
        if self.exec() == QDialog.Accepted:
            to_delete = self.behavior_combobox.currentText()
            replace = self.replace_behavior_combobox.currentText()
            return (to_delete, replace)
        else:
            return (None, None)
        
        
        


