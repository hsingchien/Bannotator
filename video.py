import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap

class BehavVideo(cv2.VideoCapture):
    def __init__(self, video_path, mwindow) -> None:
        super().__init__(video_path)
        self.last_frame_index = int(self.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        self.video_path = video_path

    def get_frame(self, frameN):
        self.set(cv2.CAP_PROP_POS_FRAMES, frameN)
        success, frame = self.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        else:
            return None
        
    def get_pixmap(self,frameN):
        frame = self.get_frame(frameN)
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = 3*width
            q_image = QImage(frame.data, width, height, bytes_per_line,QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            return pixmap
        else:
            return False

    def num_frame(self):
        return self.last_frame_index + 1
    
    def frame_rate(self):
        return int(self.get(cv2.CAP_PROP_FPS))