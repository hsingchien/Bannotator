from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from state import GuiState
from video import BehavVideo
import pyqtgraph as pg
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Initialize states
        self.state = GuiState()
        self.state["video"] = None
        self.state["FPS"] = None
        self.state["current_frame"] = None
        self.state["play_speed"] = self.speed_doubleSpinBox.value()
        # Set up UI
        self.bvscene = QGraphicsScene()
        self.vid1_view.setScene(self.bvscene)
        self.video_item = QGraphicsPixmapItem()
        self.bvscene.addItem(self.video_item)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.play_video_update_frame)
        
        # Set up pushbuttons and spinboxes 
        self.play_button.clicked.connect(self.play_video)
        self.speed_doubleSpinBox.valueChanged.connect(self.set_play_speed)
        # Connect menu bar actions
        self.actionOpen_video.triggered.connect(self.open_video)

        # Connect state change 
        self.state.connect("current_frame", self.go_to_frame)

    def open_video(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        video_path, _ = fileDialog.getOpenFileName(self, caption="Open single behavior video", filter="Video files (*.avi *.mp4 *.flv *.flv *.mkv)")
        if not video_path:
            return False
        bvideo = BehavVideo(video_path,self)
        self.state["video"] = bvideo
        self.state["current_frame"] = 0
        self.state["FPS"] = bvideo.frame_rate()

        self.video_scrollbar.setMaximum(bvideo.num_frame())
        self.curframe_spinBox.setMaximum(bvideo.num_frame())

    def go_to_frame(self, frameN):
        video = self.state["video"]
        frame_pixmap = video.get_pixmap(frameN)
        self.video_item.setPixmap(frame_pixmap)
    
    def play_video_update_frame(self):
        if self.state["current_frame"] < (self.state["video"].num_frame()-1):
            self.state["current_frame"] += 1
    
    def play_video(self):
        self.timer.start(1000/(self.state["FPS"]*self.state["play_speed"]))

    def set_play_speed(self, value):
        self.state["play_speed"] = value
        if self.timer.isActive():
            self.play_video()
        else:
            return True