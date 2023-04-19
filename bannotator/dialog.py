from PySide6.QtWidgets import QInputDialog

class CropAnnotationDialog(QInputDialog):
    def __init__(self, annot_length, vid_length, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.setInputMode(QInputDialog.IntInput)
        self.setIntMinimum(1)
        self.setIntMaximum(annot_length-vid_length+1)
    def showDialog(self):
        int_input, ok = self.getInt(self, "Is this the correct annotation?", "Annotation is longer than the video 1.\nTruncate the annotation from\n OK to proceed. Cancel to abort")
        return int_input, ok

# class AddBehaviorDialog()