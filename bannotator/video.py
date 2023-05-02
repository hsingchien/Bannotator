import cv2
import numpy as np
import struct
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRunnable, Signal, Slot, QObject, QThreadPool, QThread, QTimer, QEventLoop


class BehavVideo(QObject):
    fetch_frame_number = Signal(object)
    new_frame_fetched = Signal(object)
    run_worker = Signal(bool)
    request_fetch = Signal()
    
    @Slot()
    def emit_new_frame(self,new_frame):
        self.new_frame_fetched.emit(new_frame)
        
    def __init__(self, video_path) -> None:
        super().__init__()
        vid = cv2.VideoCapture(video_path)
        self._num_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self._video_path = video_path
        self._FPS = int(vid.get(cv2.CAP_PROP_FPS))
        vid.release()
        self._worker = VideoWorker(video_path)
        self._threadpool = QThreadPool()
        # Use fetch_frame_number to send the frame request
        self.fetch_frame_number.connect(self._worker.receive_frame_number)
        # Run/Stop worker
        self.run_worker.connect(self._worker.receive_run_state)
        # Worker send fram through result_signal, connect it to the self signal to the mainwindow
        self._worker.signals.result_signal.connect(self.emit_new_frame)
        # A gate keeper for fetcher thread emitting, to avoid fetcher taking too much resource
        self.request_fetch.connect(self._worker.request_emit)
        # Use a timer to periodically request emission
        self._timer = QTimer(self)
        self._timer.timeout.connect(lambda: self.request_fetch.emit())
        self._threadpool.start(self._worker)
        # Set refreshing rate at 60Hz
        self._timer.start(1000/60)

        
    def get_pixmap(self,frame):
        self.fetch_frame_number.emit(frame)

    def file_name(self):
        return self._video_path

    def num_frame(self):
        return self._num_frame
    
    def frame_rate(self):
        return self._FPS

    def stop_worker(self):
        self.run_worker.emit(False)
        self._threadpool.waitForDone()
        self.clear_threads()

    def clear_threads(self):
        self._threadpool.clear()

class VideoSignals(QObject):
    result_signal = Signal(object)
    progress_signal = Signal(int)
    finished_signal = Signal()
    
    
class VideoWorker(QRunnable):
    @Slot()
    def receive_frame_number(self, frameN:int):
        self._frame_number = frameN
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running
    @Slot()
    def request_emit(self):
        self._emit_flag = True

    def __init__(self, url):
        super(VideoWorker, self).__init__()
        self._url = url
        self.signals = VideoSignals()
        self._frame_number = None
        self._run = True
        self._emit_flag = True
    @Slot()
    def run(self):
        cap = cv2.VideoCapture(self._url)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return None

        while self._run:
            if self._frame_number is not None :
                cap.set(cv2.CAP_PROP_POS_FRAMES, self._frame_number)
                # Read the frame
                ret, frame = cap.read()
                # if ret and self._frame_number != self._current_frame_number:
                if ret and self._emit_flag:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, _ = frame.shape
                    bytes_per_line = 3*width
                    q_image = QImage(frame.data, width, height, bytes_per_line,QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    self.signals.result_signal.emit(pixmap)
                    # self._current_frame_number = self._frame_number
                    self._emit_flag = False
                else:
                    QThread.msleep(20)
            else:
                QThread.msleep(20)
        


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

class SeqBehavVideo(QObject):
    finished_signal = Signal()
    fetch_index = Signal(object)
    run_worker = Signal(bool)
    request_fetch = Signal()
    new_frame_fetched = Signal(object)
    
    def __init__(self, filename, outlet=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self._outlet = outlet
        self._video_path = filename
        self._file = open(filename, 'rb')
        self._header_dict = self._read_header(HEADER_FIELDS)
        self._file.close()
        self._frame_num = self._header_dict["allocated_frames"]
        self._width = self._header_dict['width']
        self._height = self._header_dict['height']
        self._threadpool = QThreadPool()
        if self._header_dict["compression_format"] == 0:
            self._jpeg = False
            self._image_block_size = self._header_dict["true_image_size"]
            self._image_offset = 8192
        elif self._header_dict["compression_format"] == 1:
            self._jpeg = True
            self._imstarts = None
            self._imends = None
            # Jpeg compression, search for frames by looking for the head and tail signatures
            self._timestamp_struct = struct.Struct('<LH')
            self._timestamp_micro = False
            # Use a separate thread to find starts and ends
            frame_finder = FindingFrameWorker(self._video_path, self._frame_num)
            # Signal to find start and end
            frame_finder.signals.result_signal.connect(self._set_im_indices)
            # Emit progress and display in the statusbar
            frame_finder.signals.progress_signal.connect(self._update_progress)
            # Connect run state signal to frame fetcher
            self.run_worker.connect(frame_finder.receive_run_state)
            self._waiting_loop = QEventLoop()
            self.finished_signal.connect(self._waiting_loop.quit)
            self._threadpool.start(frame_finder)
        else:
            raise IOError("Only uncompressed or JPEG images are supported at this point")
        

    def file_name(self):
        return self._video_path
        
    def start_frame_fetcher(self):
        # First wait for frame finding worker done searching
        if self._jpeg and self._imstarts is None:
            self._waiting_loop.exec()
        if self._jpeg and len(self._imstarts) != self._frame_num:
            raise IOError("Number of frames does not match header data")
        self.worker = SeqVideoWorker(self._video_path, self._jpeg, self._header_dict)
        # Signal to send the fetching instruction (start, end, next_start)
        self.fetch_index.connect(self.worker.receive_read_position)
        # Run/Stop signal
        self.run_worker.connect(self.worker.receive_run_state)
        # Receive emitted frame from the fetcher
        self.worker.signals.result_signal.connect(self._emit_new_frame)
        # Gate keeper for fetcher emission
        self.request_fetch.connect(self.worker.request_emit)
        # Set a timer to regulate emit frequency
        self._timer = QTimer(self)
        self._timer.timeout.connect(lambda: self.request_fetch.emit())
        self._threadpool.start(self.worker)
        
        # Start the worker
        self._threadpool.start(self.worker)
        # Start the loop
        self.run_worker.emit(True)
        # Set refreshing rate at 60Hz
        self._timer.start(1000/60)
    
    def _read_header(self,header_fields):
        self._file.seek(0)
        header = dict()
        for name, format in header_fields:
            value = self._unpack(format)
            header[name] = value
        return header
    
    def is_jpeg(self):
        return self._jpeg
    
    def _unpack(self, fs):
        s = struct.Struct("<"+fs)
        values = s.unpack(self._file.read(s.size))
        if len(values) == 1:
            return values[0]
        else:
            return values

    def _set_im_indices(self, output):
        self._imstarts, self._imends = output
        self.finished_signal.emit()
        
    def _update_progress(self, value):
        self._outlet.clearMessage()
        self._outlet.showMessage(f"Finding frames, {value}%...",2000)
            
    def _emit_new_frame(self, new_frame):
        self.new_frame_fetched.emit(new_frame)
             
    def get_pixmap(self, i):
        if i >= self._frame_num:
            return False
        
        if self._jpeg and self._imstarts is not None:
            this_start = self._imstarts[i]
            this_end = self._imends[i]
            next_start = None # Reserved for time stamp alignment in future use
            self.fetch_index.emit((this_start,this_end,next_start))
        elif not self._jpeg:
            this_start = self._image_block_size*i+self._image_offset
            this_end = this_start + self._image_block_size+self._image_offset
            next_start = None
            self.fetch_index.emit((this_start,this_end,next_start))
            
    def stop_worker(self):
        self._timer.stop()
        self.run_worker.emit(False)
        self._threadpool.waitForDone()
        self._threadpool.clear()   

    def num_frame(self):
        return self._frame_num

    def frame_rate(self):
        return self._header_dict["suggested_frame_rate"]        
    
class FindingFrameWorker(QRunnable):
    def __init__(self, url, total_frames):
        super().__init__()
        self.signals = VideoSignals()
        self._url = url
        self._total_frame = total_frames
        self._run = True
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running
    @Slot()
    def run(self):
        seqfile = open(self._url, "rb")
        im_starts = []
        im_ends = []
        seqfile.seek(0)
        imdata = seqfile.read()
        _from = 0
        while self._run:
            start = imdata.find(jpg_byte_start, _from)
            if start < 0:
                break
            _from = start
            end = imdata.find(jpg_byte_end,_from)
            _from = end
            im_starts.append(start)
            im_ends.append(end+2) 
            # The length of jpeg ending mark is 2
            progress = round(len(im_ends)*100/self._total_frame)
            if progress % 2:
                self.signals.progress_signal.emit(progress)
        if self._run:
            # Searching is successfully finished and is not aborted
            self.signals.result_signal.emit((im_starts, im_ends))
            self.signals.finished_signal.emit()
        seqfile.close()
        
             
class SeqVideoWorker(QRunnable):
    @Slot()
    def receive_read_position(self, idices):
        self._start, self._end, self._next_start = idices
    @Slot()
    def receive_run_state(self, running:bool):
        self._run = running
    @Slot()
    def request_emit(self):
        self._emit_flag = True
    
    def __init__(self, url, jpeg, header):
        super(SeqVideoWorker, self).__init__()
        self._url = url
        self._jpeg = jpeg
        self._header = header
        self.signals = VideoSignals()
        self._start = None
        self._end = None
        self._next_start = None
        self._run = True
        self._emit_flag = False
    @Slot()
    def run(self):
        seqfile = open(self._url, "rb")
        # with open(self._url, "rb") as seqfile:
        while self._run:
            if self._start is not None and self._jpeg and self._emit_flag:
                # Set the current frame position to the requested frame
                seqfile.seek(self._start)
                # imdata = seqfile.read(self._end-self._start)                
                # # Read the frame
                # pixmap = QPixmap()
                # try:
                #     pixmap.loadFromData(imdata)
                # except Exception as err:
                #     print(f"Failed fetching frame! {err}")

                # self.signals.result_signal.emit(pixmap)
                # self._emit_flag = False
                # Use cv2 to decode binary jpeg
                imdata = seqfile.read(self._end-self._start)
                jpg_image = bytearray()
                jpg_image += imdata
                frame = np.asarray(jpg_image, dtype="uint8")
                try:
                    frame = cv2.imdecode(frame, 0)
                    height, width = frame.shape
                    q_image = QImage(frame.data, width, height, QImage.Format_Grayscale8)
                    pixmap = QPixmap(q_image)
                    self.signals.result_signal.emit(pixmap)
                    self._emit_flag = False
                except Exception as err:
                    self._emit_flag = False
                    print(f"Failed fetching frame! {err}")
                
            elif self._start is not None and self._emit_flag:
                seqfile.seek(self._start)
                _pixel_type = "uint8"
                _pixel_count = self._header["image_size_bytes"]
                imdata = seqfile.read(_pixel_count)
                _shape = (self._header["height"], int(_pixel_count/self._header["height"]))
                pixmap = QPixmap()
                try:
                    frame = np.fromfile(seqfile,_pixel_type,_pixel_count).reshape(_shape)
                    q_image = QImage(frame.data, _shape[1], _shape[0],QImage.Format_Grayscale8)
                    pixmap.convertFromImage(q_image)
                    self.signals.result_signal.emit(pixmap)
                    self._emit_flag = False
                except Exception as err:
                    self._emit_flag = False
                    print(f"Failed fetching frame! {err}")
            else:
                QThread.msleep(20)
        seqfile.close()

    
    
            

        