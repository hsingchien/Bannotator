import cv2
import numpy as np
import struct
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRunnable, Signal, Slot, QObject, QThreadPool, Qt
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
    fetch_index = Signal(object)
    run_worker = Signal(bool)
    new_frame_fetched = Signal(object)
    progress_signal = Signal(int)
    finished_signal = Signal()
    
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
        self._frame_number = 0
        self._run = True
        self._current_frame_number = 0
        
    @Slot()
    def run(self):
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        while self._run:
            if self._frame_number is not None :
                # print(f"requested {self._frame_number}")
                # print(f"fulfilled {self._current_frame_number}")
                cap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_number)
                # Read the frame
                ret, frame = cap.read()
                # if ret and self._frame_number != self._current_frame_number:
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, _ = frame.shape
                    bytes_per_line = 3*width
                    q_image = QImage(frame.data, width, height, bytes_per_line,QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    self.signals.frame_signal.emit(pixmap)
                    # self._current_frame_number = self._frame_number
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

    

class SeqBehavVideo(NorpixSeq):
    def __init__(self, filename, outlet=None):
        self.outlet = outlet
        self._filename = filename
        self._file = open(filename, 'rb')
        self.header_dict = self._read_header(HEADER_FIELDS)
        self.threadpool = QThreadPool()
        self.signals = VideoSignals()
        # self.worker = Worker()
        if self.header_dict["compression_format"] == 0:
            # If the seq file is uncompressed, let pims NorpixSeq handle the file read and load
            super().__init__(filename, True)
            self._jpeg = False
            self.start_frame_fetcher()
        elif self.header_dict["compression_format"] == 1:
            self._jpeg = True
            self._imstarts = None
            self._imends = None
            # Jpeg compression, search for frames by looking for the head and tail signatures
            self._timestamp_struct = struct.Struct('<LH')
            self._timestamp_micro = False
            self._image_count = self.header_dict["allocated_frames"]
            self._width = self.header_dict['width']
            self._height = self.header_dict['height']
            # Use a separate thread to find starts and ends
            frame_finder = FindingFrameWorker(self._filename, self._image_count)
            frame_finder.signals.fetch_index.connect(self.set_im_indices)
            frame_finder.signals.progress_signal.connect(self.update_progress)
            frame_finder.signals.finished_signal.connect(self.start_frame_fetcher)
            self.threadpool.start(frame_finder)
        else:
            raise IOError("Only uncompressed or JPEG images are supported at this point")
        self._file.close()
        
        
        
    def start_frame_fetcher(self):
        # At this point should have imstart and imend
        if self._jpeg and len(self._imstarts) != self._image_count:
                raise IOError("Number of frames does not match header data")
        self.worker = SeqVideoWorker(self._filename, self._jpeg, self.header_dict)
        self.signals.fetch_index.connect(self.worker.receive_read_position)
        self.signals.run_worker.connect(self.worker.receive_run_state)
        self.worker.signals.frame_signal.connect(self.emit_new_frame)
        self.threadpool.start(self.worker)
        self.signals.run_worker.emit(True)

    def set_im_indices(self, output):
        self._imstarts, self._imends = output
        
    def update_progress(self, value):
        self.outlet.clearMessage()
        self.outlet.showMessage(f"Finding frames, {value}%...",2000)
            
    def emit_new_frame(self, new_frame):
        self.signals.new_frame_fetched.emit(new_frame)
             
    def get_pixmap(self, i):
        if i >= self._image_count:
            return False
        
        if self._jpeg and self._imstarts is not None:
            this_start = self._imstarts[i]
            this_end = self._imends[i]
            next_start = None # Edit this for time stamp
            self.signals.fetch_index.emit((this_start,this_end,next_start))
        elif not self._jpeg:
            this_start = self._image_block_size*i+self._image_offset
            this_end = this_start + self._image_block_size+self._image_offset
            next_start = None
            self.signals.fetch_index.emit((this_start,this_end,next_start))
            
    def stop_worker(self):
        self.signals.run_worker.emit(False)
        self.threadpool.waitForDone()
        self.threadpool.clear()

    def num_frame(self):
        return self._image_count

    def frame_rate(self):
        return self.header_dict["suggested_frame_rate"]        
    
    def header(self):
        return self.header_dict
    
class FindingFrameWorker(QRunnable):
    def __init__(self, url, total_frames):
        super().__init__()
        self.signals = VideoSignals()
        self.url = url
        self.total_frame = total_frames
    @Slot()
    def run(self):
        seqfile = open(self.url, "rb")
        im_starts = []
        im_ends = []
        seqfile.seek(0)
        imdata = seqfile.read()
        _from = 0
        while True:
            start = imdata.find(jpg_byte_start, _from)
            if start < 0:
                break
            _from = start
            end = imdata.find(jpg_byte_end,_from)
            _from = end
            im_starts.append(start)
            im_ends.append(end+2) 
            # The length of jpeg ending mark is 2
            progress = round(len(im_ends)*100/self.total_frame)
            if progress % 2:
                self.signals.progress_signal.emit(progress) 
        self.signals.fetch_index.emit((im_starts, im_ends))
        self.signals.finished_signal.emit()
        
            
class SeqVideoWorker(QRunnable):
    @Slot()
    def receive_read_position(self, idices):
        self._start, self._end, self._next_start = idices
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running

    def __init__(self, url, _jpeg, header):
        super(SeqVideoWorker, self).__init__()
        self._url = url
        self._jpeg = _jpeg
        self.header = header
        self.signals = VideoSignals()
        self._start = None
        self._end = None
        self._next_start = None
        self._run = True
        self._current_start = None
    @Slot()
    def run(self):
        seqfile = open(self._url, "rb")
        while self._run:
            if self._start is not None and self._jpeg:
                # Set the current frame position to the requested frame
                seqfile.seek(self._start)
                imdata = seqfile.read(self._end-self._start)
                # Read the frame
                jpg_image = bytearray()
                jpg_image += imdata
                if self._current_start != self._start:
                    frame = np.asarray(jpg_image, dtype="uint8")
                    frame = cv2.imdecode(frame, 0)
                    height, width = frame.shape
                    q_image = QImage(frame.data, width, height, QImage.Format_Grayscale8)
                    pixmap = QPixmap(q_image)
                    self.signals.frame_signal.emit(pixmap)
                    self._current_start = self._start
            elif self._start is not None:
                seqfile.seek(self._start)
                if self._current_start != self._start:
                    _pixel_type = "uint8"
                    _pixel_count = self.header["image_size_bytes"]
                    _shape = (self.header["height"], int(_pixel_count/self.header["height"]))
                    frame = np.fromfile(seqfile,_pixel_type,_pixel_count).reshape(_shape)
                    q_image = QImage(frame.data, _shape[1], _shape[0],QImage.Format_Grayscale8)
                    pixmap = QPixmap(q_image)
                    self.signals.frame_signal.emit(pixmap)
                    self._current_start = self._start

        seqfile.close()

    
    
            

        