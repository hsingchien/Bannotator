import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRunnable, Signal, Slot, QObject, QThreadPool


class BehavVideo(QObject):
    fetch_frame_number = Signal(object)
    new_frame_fetched = Signal(object)
    run_worker = Signal(bool)
    
    @Slot()
    def emit_new_frame(self,new_frame):
        self.new_frame_fetched.emit(new_frame)
        
    def __init__(self, video_path) -> None:
        super().__init__()
        vid = cv2.VideoCapture(video_path)
        self.last_frame_index = int(vid.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        self.video_path = video_path
        self.FPS = int(vid.get(cv2.CAP_PROP_FPS))
        vid.release()
        self.worker = VideoWorker(video_path)
        self.threadpool = QThreadPool()
        self.fetch_frame_number.connect(self.worker.receive_frame_number)
        self.run_worker.connect(self.worker.receive_run_state)
        self.worker.signals.frame_signal.connect(self.emit_new_frame)
        self.threadpool.start(self.worker)

        
    def get_pixmap(self,frameN):
        self.fetch_frame_number.emit(frameN)

    def file_name(self):
        return self.file_name

    def num_frame(self):
        return self.last_frame_index + 1
    
    def frame_rate(self):
        return self.FPS

    def stop_worker(self):
        self.run_worker.emit(False)
        self.threadpool.waitForDone()
        self.clear_threads()

    def clear_threads(self):
        self.threadpool.clear()

class VideoSignals(QObject):
    frame_signal = Signal(object)
class VideoWorker(QRunnable):
    @Slot()
    def receive_frame_number(self, frameN:int):
        self._frame_number = frameN
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running

    def __init__(self, url):
        super(VideoWorker, self).__init__()
        self.url = url
        self.signals = VideoSignals()
        self._frame_number = None
        self._run = True
        self._current_frame_number = -10
    @Slot()
    def run(self):
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        while self._run:
            if self._frame_number is not None:
                # Set the current frame position to the requested frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_number)
                # Read the frame
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.signals.frame_signal.emit(frame)
                    height, width, _ = frame.shape
                    bytes_per_line = 3*width
                    q_image = QImage(frame.data, width, height, bytes_per_line,QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    if self._frame_number != self._current_frame_number:
                        self.signals.frame_signal.emit(pixmap)
                        self._current_frame_number = self._frame_number
        cap.release()
    
            

        