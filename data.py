from PySide6.QtGui import QColor
from PySide6 import QtCore
from typing import List, Dict
import re
import numpy as np


class Epoch(object):
    # Defines unit behavior epoch
    def __init__(
        self,
        stream: "Stream" = None,
        behavior: "Behavior" = None,
        start: int = None,
        end: int = None,
    ) -> None:
        self.behavior = behavior
        self.stream = stream
        # [start, end] is the inclusive index range
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start: int = None):
        self._start = new_start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_end: int = None):
        self._end = new_end

    @property
    def name(self):
        return self.behavior.name

    @property
    def color(self):
        return self.behavior.get_color()

    def __str__(self) -> str:
        return (
            f"Stream {self.streamID} - {self.behavior.name}: {self.start} - {self.end}"
        )

    def __lt__(self, other: "Epoch") -> bool:
        return self.start < other.start

    def __le__(self, other: "Epoch") -> bool:
        return self.start <= other.start

    def __eq__(self, other: "Epoch") -> bool:
        return self.start == other.start and self.end == other.end

    def get_length(self):
        return self.end - self.start + 1

    def get_range(self):
        return [self.start, self.end]

    def get_behavior(self):
        return self.behavior

    def get_stream(self):
        return self.stream

    def set_behavior(self, new_behavior: "Behavior" = None):
        if new_behavior is None:
            return False
        else:
            old_behavior = self.behavior
            old_behavior.remove_epoch(self)
            self.behavior = new_behavior
            new_behavior.append_epoch(self)

    def change_behavior(self, new_behavior: "Behavior" = None):
        if new_behavior is None:
            return False
        if new_behavior is not self.behavior:
            self.behavior = new_behavior
            return True

    def set_start_end(self, start: int = None, end: int = None):
        if not (start or end):
            return False
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        return True

    def get_behavior(self):
        return self.behavior


class Behavior(QtCore.QObject):
    keybind_changed = QtCore.Signal()
    color_changed = QtCore.Signal()
    epoch_changed = QtCore.Signal()

    # Defines behaviors
    def __init__(
        self,
        name: str = None,
        keybind: str = None,
        ID: int = None,
        color: QColor = QColor("black"),
        epochs: List = [],
        stream: "Stream" = None,
    ):
        super().__init__()
        self._name = name
        self.keybind = keybind
        self._ID = ID
        self._color = color
        self.epochs = epochs
        self.stream = stream

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, new_ID: int = None):
        self._ID = new_ID

    @property
    def color(self):
        return self._color.name()

    def __str__(self) -> str:
        return f"stream: {self.stream}, {self.name}, ID: {self.ID}, keybind: {self.keybind}, color: {self.color}"

    def get_name(self):
        return self.name

    def get_keybind(self):
        return self.keybind

    def set_ID(self, new_ID: int = None):
        self.ID = new_ID
        return True

    def set_keybind(self, new_keybind: str = None):
        if self.keybind != new_keybind:
            self.keybind_changed.emit()
            return True
        else:
            return False

    def set_stream(self, new_stream: "Stream" = None):
        self.stream = new_stream
        return True

    def set_color(self, new_color: QColor = None):
        if self._color != new_color:
            self._color = new_color
            self.color_changed.emit()
            return True
        else:
            return False

    def get_stream_ID(self):
        return self.stream.ID

    def get_color(self):
        return self._color

    def num_epochs(self):
        return len(self.epochs)

    def duration(self):
        if not self.epochs:
            return 0
        duration = 0
        for epo in self.epochs:
            duration += epo.get_length()
        return duration

    def append_epoch(self, epoch: Epoch = None):
        self.epochs.append(epoch)
        self.epochs.sort(key=lambda x: x.start)
        self.epoch_changed.emit()

    def remove_epoch(self, epoch: Epoch = None):
        self.epochs.remove(epoch)
        self.epoch_changed.emit()

    def get_percentage(self):
        dur = self.duration()
        stream_length = self.stream.get_length()
        return dur / stream_length
    
    def get_epochs(self):
        self.epochs.sort(key= lambda x: x.start)
        return self.epochs


class Stream(QtCore.QObject):
    # Date changed signal, emit updated epoch vector
    data_changed = QtCore.Signal(object)
    # Color changed signal, emit updated color dictionary
    color_changed = QtCore.Signal(object)
    # Current behavior signal, link to the behavior label
    cur_behavior_name = QtCore.Signal(object)
    # Current epoch signal, link to the stream table highlight and scrolling
    cur_epoch = QtCore.Signal(object)

    # Defines class Stream to store annotation data
    def __init__(self, ID: int = None, epochs: List = [], behaviors: Dict = {}) -> None:
        super().__init__()
        self._ID = ID
        self.epochs = epochs
        self.behaviors = behaviors
        self._length = self.get_length()
        if not self.behaviors:
            self.keymap = dict()
        else:
            self.map_behav_key()
            for _, be in self.behaviors.items():
                be.keybind_changed.connect(self.map_behav_key)
                be.color_changed.connect(lambda: self.color_changed.emit())

    @property
    def length(self):
        return self._length

    @property
    def ID(self):
        return self._ID

    def sort_epoch(self):
        self.epochs.sort(reverse=False)
        return True

    def validate_epoch(self):
        # Validate epochs to make sure no overlap, no repetitive behavior
        self.sort_epoch()
        for i in range(len(self.epochs) - 1):
            epoch1 = self.epochs[i]
            epoch2 = self.epochs[i + 1]
            if epoch1.end >= epoch2.start:
                return False
            if epoch1.name == epoch2.name:
                return False
        return True

    def map_behav_key(self):
        try:
            for _, behav in self.behaviors.items():
                self.keymap[behav.keybind] = behav
        except Exception:
            self.keymap = dict()

    def construct_behavior_from_config(self, config):
        for i, behav in enumerate(config):
            behav_name, keybind = behav.split()
            self.behaviors[behav_name] = Behavior(
                name=behav_name,
                keybind=keybind,
                ID=i,
                stream=self,
                epochs=[],
                color=QColor("black"),
            )
            self.behaviors[behav_name].keybind_changed.connect(self.map_behav_key)
            self.behaviors[behav_name].color_changed.connect(
                lambda: self.color_changed.emit(self.get_color_dict())
            )
        self.map_behav_key()

    def get_stream_vect(self):
        # Returns 1 x stream length vector with each entry being behavior ID
        vec = np.zeros(self.length)
        for epoch in self.epochs:
            start = epoch.start - 1
            end = epoch.end
            vec[start:end] = epoch.get_behavior().ID
        return vec

    def assign_color(self, color_dict):
        for _, behav in self.behaviors.items():
            behav.set_color(color_dict[behav.name])
        self.color_changed.emit(self.get_color_dict())

    def get_color_dict(self):
        color_dict = dict()
        for _, behav in self.behaviors.items():
            color_dict[behav.ID] = behav.get_color()
        return color_dict

    def construct_epochs_from_sequence(self, sequence):
        for i, annot in enumerate(sequence):
            start, end, behav_name = annot.split()
            start = int(start)
            end = int(end)
            epoch = Epoch(
                stream=self, behavior=self.behaviors[behav_name], start=start, end=end
            )
            self.epochs.append(epoch)
            self.behaviors[behav_name].append_epoch(epoch)
        self._length = self.get_length()
        self.validate_epoch()
        self.data_changed.emit(self.get_stream_vect())

    def get_behaviors(self):
        behavior_list = [behavior for _, behavior in self.behaviors.items()]
        behavior_list.sort(reverse=False, key=lambda x: x.ID)
        return behavior_list
    
    def get_behavior_dict(self):
        return self.behaviors
    
    def get_epochs(self):
        return self.epochs

    def get_epoch_by_idx(self, idx: int, allow_emit=True):
        # Index is frame index, start from 0
        idx = idx + 1
        epochs = self.epochs
        epoch = epochs[int(len(self.epochs) / 2)]
        # Edge case
        if idx < 1 or idx > self.length:
            return None
        while epoch.start > idx or epoch.end < idx:
            if epoch.start > idx:
                epochs = epochs[0 : int(1 / 2 * len(epochs))]
                epoch = epochs[int(1 / 2 * len(epochs))]
            elif epoch.end < idx:
                epochs = epochs[int(1 / 2 * len(epochs)) : len(epochs)]
                epoch = epochs[int(1 / 2 * len(epochs))]
        if allow_emit:
            self.cur_epoch.emit(epoch)
        return epoch

    def get_behavior_by_idx(self, idx: int):
        epoch = self.get_epoch_by_idx(idx, False)
        self.cur_behavior_name.emit(epoch.get_behavior())
        return epoch.get_behavior()

    def get_length(self):
        if self.epochs:
            self.sort_epoch()
            last_epoch = self.epochs[len(self.epochs) - 1]
            return last_epoch.end
        else:
            return 0

    def set_behavior(self, fidx: int = None, keypressed: str = None):
        if not keypressed in self.keymap.keys():
            return False
        epoch = self.get_epoch_by_idx(fidx)
        if epoch.get_behavior().get_keybind() == keypressed:
            return False
        if fidx == epoch.start - 1:
            # Change the whole epoch
            # Check both sides for merge
            old_behavior = epoch.get_behavior()
            old_behavior.remove_epoch(epoch)
            new_behavior = self.keymap[keypressed]
            prev_epoch = self.get_epoch_by_idx(fidx - 1)
            next_epoch = self.get_epoch_by_idx(epoch.end)
            epoch.change_behavior(new_behavior)
            if prev_epoch and epoch.name == prev_epoch.name:
                epoch.set_start_end(prev_epoch.start, epoch.end)
                # Del prev_epoch references
                self.epochs.remove(prev_epoch)
                new_behavior.remove_epoch(prev_epoch)
            if next_epoch and epoch.name == next_epoch.name:
                epoch.set_start_end(epoch.start, next_epoch.end)
                self.epochs.remove(next_epoch)
                new_behavior.remove_epoch(next_epoch)
            new_behavior.append_epoch(epoch)
        else:
            # Make the rest of the current epoch a new epoch
            # Truncate the current epoch to the frame before
            new_start_1 = epoch.start
            new_start_2 = fidx + 1
            new_end_1 = fidx
            new_end_2 = epoch.end
            new_behavior = self.keymap[keypressed]
            epoch.set_start_end(start=new_start_1, end=new_end_1)
            next_epoch = self.get_epoch_by_idx(new_end_2)
            if next_epoch and new_behavior.name == next_epoch.name:
                next_epoch.set_start_end(start=new_start_2, end=next_epoch.end)
            else:
                new_epoch = Epoch(
                    stream=self, behavior=new_behavior, start=new_start_2, end=new_end_2
                )
                new_behavior.append_epoch(new_epoch)
                self.epochs.append(new_epoch)
        validated = self.validate_epoch()
        if not validated:
            raise Exception(
                f"Stream-{self.ID} has problematic epochs (overlapped epoch or repetitive behaviors)!"
            )
        self.data_changed.emit(self.get_stream_vect())


class Annotation(QtCore.QObject):
    construct_from_file = QtCore.Signal(str)
    content_changed = QtCore.Signal()
    saved_in_file = QtCore.Signal(str)

    @QtCore.Slot()
    def streams_changed(self):
        self.content_changed.emit()

    def __init__(self, streams: Dict = {}):
        super().__init__()
        # Use dict to organize streams
        self.streams = streams
        for _, stream in self.streams:
            stream.data_changed.connect(self.streams_changed)
            stream.color_changed.connect(self.streams_changed)
        # Behvior-color dict
        self.behav_color = dict()

    def read_from_file(self, txt_path):
        config = []
        annots = dict()
        with open(txt_path) as file:
            in_config = False
            current_anno = None
            while True:
                k = file.readline()
                if not k:
                    break
                if k.isspace():
                    in_config = False
                    current_anno = None
                elif "Configuration file:" in k:
                    # Onto configuration file section
                    in_config = True
                    current_anno = None
                    config.append(next(file).strip())
                elif "type" in k and "start" in k:
                    # Onto a new stream
                    in_config = False
                    match = re.search(r"S(\d+)", k)
                    current_anno = int(match.group(1))
                    if annots.get(current_anno):
                        raise ValueError("conflict stream number")
                    else:
                        annots[current_anno] = []
                elif in_config:
                    config.append(k.strip())
                elif current_anno and "----" not in k:
                    annots[current_anno].append(k.strip())
        success = self.construct_streams(config, annots)
        if success:
            self.construct_from_file.emit(
                "Annotation successfully contructed from file"
            )
        else:
            self.construct_from_file.emit("Failed to construct annotation from file")

    def construct_streams(self, config, annots):
        for stream_id, annotation_sequence in annots.items():
            # Create behaviors for the stream
            self.streams[stream_id] = Stream(ID=stream_id, epochs=[], behaviors={})
            self.streams[stream_id].construct_behavior_from_config(config)
            self.streams[stream_id].construct_epochs_from_sequence(annotation_sequence)
            self.streams[stream_id].data_changed.connect(self.streams_changed)
        return True

    def validate_streams(self):
        behav_list = [stream.get_behaviors() for _, stream in self.streams.items()]
        # Validate the streams have the same behavior setting
        for i in range(len(behav_list[0])):
            bname = behav_list[0][i].name
            bID = behav_list[0][i].ID
            bcolor = behav_list[0][i].color
            bkbind = behav_list[0][i].get_keybind()
            for j in range(len(behav_list)):
                cur_behav = behav_list[j][i]
                if (
                    cur_behav.name != bname
                    or cur_behav.ID != bID
                    or cur_behav.color != bcolor
                    or cur_behav.get_keybind() != bkbind
                ):
                    return False
        return True

    def get_behaviors(self):
        if self.validate_streams():
            # Return a list of Behavior objects
            ks = sorted(list(self.streams.keys()))
            return [self.streams[k].get_behaviors() for k in ks]
        else:
            raise Exception("Inconsisten behaviors across streams")

    def num_stream(self):
        return len(self.streams)

    def num_epochs(self):
        epoch_lens = []
        for _, stream in self.streams.items():
            epoch_lens.append(len(stream.get_epochs()))
        return epoch_lens

    def assign_behavior_color(self):
        behaviors = self.get_behaviors()
        behavior_names = [i.name for i in behaviors[0]]
        for i, behav in enumerate(behavior_names):
            hue = int(255 * i / len(behavior_names))
            saturation = 180
            value = 200
            if behav not in ["other", "blank"]:
                self.behav_color[behav] = QColor.fromHsv(hue, saturation, value)
            else:
                self.behav_color[behav] = QColor("#9d9d9d")
        # Assign colors to the behavior objects for all the streams
        for _, stream in self.streams.items():
            stream.assign_color(self.behav_color)

    def get_stream_vects(self):
        vec_dict = dict()
        for i in self.streams.keys():
            vec_dict[i] = self.streams[i].get_stream_vect()
        return vec_dict

    def get_streams(self):
        return self.streams

    def get_length(self):
        length = 0
        for _, i in self.streams.items():
            length = max(i.length, length)
        return length

    def save_to_file(self, filename):
        try:
            with open(filename, "w") as f:
                f.write("Caltech Behavior Annotator - Annotation File\n")
                f.write("\nConfiguration file:\n")
                self.write_behavior(f)
                f.write("\n")
                self.write_streams(f)
            self.saved_in_file.emit(f"Saved annotation to {filename} successfully!")
            return True
        except Exception:
            return False

    def save_config_to_file(self, filename):
        num_streams = len(self.streams)
        try:
            with open(filename, "w") as f:
                f.write("nStream " + str(num_streams) + "\n")
                self.write_behavior(f)
            self.saved_in_file.emit(f"Saved config to {filename} successfully!")
            return True
        except Exception:
            return False

    def write_behavior(self, f):
        config = self.get_behaviors()[0]
        lines = []
        for behav in config:
            lines.append(behav.name + "\t" + behav.keybind + "\n")
        if f:
            f.writelines(lines)

    def write_streams(self, f):
        lines = []
        for _, stream in self.streams.items():
            lines.append("S" + str(stream.ID) + ":\tstart\tend\ttype\n")
            lines.append("-" * 29 + "\n")
            stream.sort_epoch()
            for epoch in stream.get_epochs():
                lines.append(
                    "   \t"
                    + "\t".join([str(epoch.start), str(epoch.end), epoch.name])
                    + "\n"
                )
            lines.append("  \n")
        if f:
            f.writelines(lines)
