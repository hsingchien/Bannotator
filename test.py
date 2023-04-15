seqfile = open("seqs/bottom_jpeg.seq", "rb")
jpg_byte_start = b"\xff\xd8"
jpg_byte_end = b"\xff\xd9"
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
    end = imdata.find(jpg_byte_end, _from)
    _from = end
    im_starts.append(start)
    im_ends.append(end + 2)

print(im_starts[0])
print(im_ends[0])
from PySide6.QtGui import QPixmap

seqfile.seek(1028)
im_data = seqfile.read(54670 - 1028)
pixmap = QPixmap().loadFromData(im_data, "JPEG")
