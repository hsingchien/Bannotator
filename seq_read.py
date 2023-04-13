import pims
import numpy as np
class SeqReader(pims.FramesSequence):
    def __init__(self, filename):
        self.filename = filename
        self.seq_file = pims.open(filename, as_raw = True)
        self._len = self.seq_file.header_dict["allocated_frames"] # however many frames there will be
        self._dtype =  np.uint8 # the numpy datatype of the frames
        self._frame_shape =  (self.seq_file.header_dict["width"],self.seq_file.header_dict["height"])# the shape, like (512, 512), of an
                             # individual frame -- maybe get this by
                             # opening the first frame
        # Do whatever setup you need to do to be able to quickly access
        # individual frames later.

    def get_frame(self, i):
        # Access the data you need and get it into a numpy array.
        # Then return a Frame like so:
        return Frame(my_numpy_array, frame_no=i)

     def __len__(self):
         return self._len

     @property
     def frame_shape(self):
         return self._frame_shape

     @property
     def pixel_type(self):
         return self._dtype