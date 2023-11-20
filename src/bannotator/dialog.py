from PySide6.QtWidgets import QInputDialog, QDialog, QDialogButtonBox
from bannotator.ui import *
import re


class TruncateAnnotationDialog(QDialog, Ui_TruncateAnnotationDialog):
    def __init__(self, annot_length, vid_length, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.from_spinbox.setMaximum(annot_length - vid_length + 1)
        self.from_spinbox.setMinimum(1)
        self.to_spinbox.setMinimum(vid_length)
        self.to_spinbox.setMaximum(annot_length)
        self.to_spinbox.valueChanged.connect(
            lambda x: self.from_spinbox.setValue(x - vid_length + 1)
        )
        self.from_spinbox.valueChanged.connect(
            lambda x: self.to_spinbox.setValue(x + vid_length - 1)
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_input(self):
        if self.exec() == QDialog.Accepted:
            from_value = self.from_spinbox.value()
            to_value = self.to_spinbox.value()
            return (from_value, to_value)
        else:
            return (None, None)


class AddBehaviorDialog(QDialog, Ui_AddBehaviorDialog):
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        behavior_list = annotation.get_behaviors()
        self.all_names = [behav.name for behav in behavior_list[0]]
        all_key_binds = [behav.keybind for behav in behavior_list[0]]
        letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
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
            return (None, None)

    def validate_name(self, user_input):
        if user_input and user_input not in self.all_names:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


class DeleteBehaviorDialog(QDialog, Ui_DeleteBehaviorDialog):
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        behavior_list = annotation.get_behaviors()
        all_behavior_names = [behav.name for behav in behavior_list[0]]
        self.behavior_combobox.addItems(all_behavior_names)
        self.replace_behavior_combobox.addItems(all_behavior_names)
        self.replace_behavior_combobox.setCurrentIndex(0)
        self.behavior_combobox.setCurrentIndex(0)
        self.update_behavior_info(self.behavior_combobox.currentText())
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.behavior_combobox.currentTextChanged.connect(self.validate_input)
        self.replace_behavior_combobox.currentTextChanged.connect(self.validate_input)
        self.behavior_combobox.currentTextChanged.connect(self.update_behavior_info)

    def validate_input(self):
        if (
            self.replace_behavior_combobox.currentText()
            == self.behavior_combobox.currentText()
        ):
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

    def update_behavior_info(self, bname):
        n_epochs = []
        for _, stream in self.annotation.get_streams().items():
            behav = stream.get_behavior_dict()[bname]
            n_epochs.append(str(behav.num_epochs()))
        n_epochs = ", ".join(n_epochs)
        self.num_epochs_label.setText(n_epochs)


class AddStreamDialog(QDialog, Ui_AddStreamDialog):
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        behavior_list = annotation.get_behaviors()
        all_behavior_names = [behav.name for behav in behavior_list[0]]
        self.behavior_combobox.addItems(all_behavior_names)

    def get_input(self):
        if self.exec() == QDialog.Accepted:
            behavior = self.behavior_combobox.currentText()
            return behavior
        else:
            return None


class DeleteStreamDialog(QDialog, Ui_DeleteStreamDialog):
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.annotation = annotation
        ids = list(annotation.get_streams().keys())
        self.stream_combobox.addItems([str(id) for id in ids])

    def get_input(self):
        if self.exec() == QDialog.Accepted:
            streamID = int(self.stream_combobox.currentText())
            return streamID
        else:
            return None

class NewAnnotationDialog(QDialog, Ui_NewAnnotationDialog):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setupUi(self)
        self.behavior_text_edit.textChanged.connect(self.validate_behaivor)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def validate_behaivor(self):
        ok = False
        names = []
        keybinds = []
        text = self.behavior_text_edit.toPlainText()
        bk_pairs = text.split("\n")
        # Remove empty lines
        for l in bk_pairs:
            if re.match(r'^\s*$', l):
                bk_pairs.remove(l)
        # Check if the text is in the format of  word-key
        pattern = re.compile(r'^(\w+)(\s*[-]*\s*)([a-zA-Z])$')
        for bk in bk_pairs:
            bkl = bk.lower()
            mat = re.match(pattern, bkl)
            if not mat:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                return ok
            else:
                name = mat.group(1)
                space = mat.group(2)
                k = mat.group(3)
                if len(space) < 1:
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    return ok
                else:
                    names.append(name)
                    keybinds.append(k)
        # Check if words and keys are unique
        if len(names) != len(set(names)):
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return ok
        if len(keybinds) != len(set(keybinds)):
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return ok
        ok = True
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        return ok
        
    def get_input(self):
        if self.exec() == QDialog.Accepted:
            names = []
            keybinds = []
            nstream = self.nStream_spinBox.value()
            bk_pairs = self.behavior_text_edit.toPlainText().split("\n")
            # Remove empty lines
            for l in bk_pairs:
                if re.match(r'^\s*$', l):
                    bk_pairs.remove(l)
            pattern = re.compile(r'^(\w+)\s*[-]*\s*(\w)$')
            for bk in bk_pairs:
                bkl = bk.lower()
                mat = re.match(pattern, bkl)
                names.append(mat.group(1))
                keybinds.append(mat.group(2))
            return (nstream, names, keybinds)
        else:
            return (None,None,None)


