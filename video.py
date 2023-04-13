import cv2
import numpy as np
import struct
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRunnable, Signal, Slot, QObject, QThreadPool
from pims.norpix_reader import NorpixSeq

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
                    # self.signals.frame_signal.emit(frame)
                    height, width, _ = frame.shape
                    bytes_per_line = 3*width
                    q_image = QImage(frame.data, width, height, bytes_per_line,QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    if self._frame_number != self._current_frame_number:
                        self.signals.frame_signal.emit(pixmap)
                        self._current_frame_number = self._frame_number
        cap.release()


DWORD = 'L'
LONG = 'l'
DOUBLE = 'd'
USHORT = 'H'

HEADER_FIELDS = [
    ('magic', DWORD),
    ('name', '24s'),
    ('version', LONG),
    ('header_size', LONG),
    ('description', '512s'),
    ('width', DWORD),
    ('height', DWORD),
    ('bit_depth', DWORD),
    ('bit_depth_real', DWORD),
    ('image_size_bytes', DWORD),
    ('image_format', DWORD),
    ('allocated_frames', DWORD),
    ('origin', DWORD),
    ('true_image_size', DWORD),
    ('suggested_frame_rate', DOUBLE),
    ('description_format', LONG),
    ('reference_frame', DWORD),
    ('fixed_size', DWORD),
    ('flags', DWORD),
    ('bayer_pattern', LONG),
    ('time_offset_us', LONG),
    ('extended_header_size', LONG),
    ('compression_format', DWORD),
    ('reference_time_s', LONG),
    ('reference_time_ms', USHORT),
    ('reference_time_us', USHORT)
    # More header values not implemented
]

jpg_byte_start = b'\xff\xd8'
jpg_byte_end = b'\xff\xd9'

class SeqBehaveVideo(NorpixSeq):
    def __init__(self, filename):
        self._filename = filename
        self._file = open(filename, 'rb')
        self.header_dict = self._read_header(HEADER_FIELDS)
        if self.header_dict["compression_format"] == 0:
            # If the seq file is uncompressed, let pims NorpixSeq handle the file read and load
            super().__init__(filename, True)
            self._jpeg = False
        elif self.header_dict["compression_format"] == 1:
            self._jpeg = True
            # Jpeg compression, search for frames
            if self.header_dict['version'] >= 5:  # StreamPix version 6
                self._image_offset = 8192
                # Timestamp = 4-byte unsigned long + 2-byte unsigned short (ms)
                #   + 2-byte unsigned short (us)
                self._timestamp_struct = struct.Struct('<LHH')
                self._timestamp_micro = True
            else:  # Older versions
                self._image_offset = 1024
                self._timestamp_struct = struct.Struct('<LH')
                self._timestamp_micro = False
                self._imstarts, self._imends = self.find_jpeg_blocks()
                self._image_count = self.header_dict["allocated_frames"]
                if len(self._imstarts) != self._image_count:
                    raise IOError("Number of frames does not match header data")
                self._width = self.header_dict['width']
                self._height = self.header_dict['height']
        else:
            raise IOError("Only uncompressed or JPEG images are supported at this point")

    def find_jpeg_blocks(self):
        im_starts = []
        im_ends = []
        self._file.seek(self._image_offset)
        imdata = self._file.read()
        _from = 0
        while True:
            start = imdata.find(jpg_byte_start, _from)
            if start < 0:
                break
            end = imdata.find(jpg_byte_end, _from)
            _from = end
            im_starts.append(start)
            im_ends.append(end)
        return (im_starts, im_ends)
            
            
            
        
    
    def header(self):
        return self.header_dict
        
            
            
class SeqVideoSignals(QObject):
    frame_signal = Signal(object)
class SeqVideoWorker(QRunnable):
    @Slot()
    def receive_frame_number(self, frameN:int):
        self._frame_number = frameN
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running

    def __init__(self, _file, _jpeg):
        super(VideoWorker, self).__init__()
        self._file = _file
        self._jpeg = _jpeg
        self.signals = SeqVideoSignals()
        self._frame_number = None
        self._run = True
        self._current_frame_number = -10
    @Slot()
    def run(self):
        if self._file.closed:
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
  
        
    
    
            

        