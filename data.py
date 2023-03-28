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
            self.behavior = new_behavior

    def change_behavior(self, new_behavior: "Behavior" = None):
        if new_behavior is None:
            return False
        if new_behavior is not self.behavior:
            self.behavior = new_behavior

    def set_start_end(self, start: int = None, end: int = None):
        if not (start or end):
            return False
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        return True


class Behavior(object):
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
        self._name = name
        self.keybind = keybind
        self._ID = ID
        self.color = color
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

    def __str__(self) -> str:
        return f"stream: {self.stream}, {self.name}, ID: {self.ID}, keybind: {self.keybind}"
        # # color: {self.color.name()}"

    def get_name(self):
        return self.name

    def set_ID(self, new_ID: int = None):
        self.ID = new_ID
        return True

    def set_keybind(self, new_keybind: str = None):
        self.keybind = new_keybind
        return True

    def set_stream(self, new_stream: "Stream" = None):
        self.stream = new_stream
        return True

    def set_color(self, new_color: QColor = None):
        self.color = new_color
        return True

    def get_color(self):
        return self.color

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


class Stream(object):
    # Defines class Stream to store annotation data
    def __init__(self, ID: int = None, epochs: List = [], behaviors: Dict = {}) -> None:
        self.ID = ID
        self.epochs = epochs
        self.behaviors = behaviors
        self._length = self.get_length()

    @property
    def length(self):
        return self._length

    def sort_epoch(self):
        self.epochs = sorted(self.epochs, reverse=False)
        return True

    def validate_epoch(self):
        # Validate epochs to make sure no overlap
        self.sort_epoch()
        for i in range(len(self.epochs) - 1):
            epoch1 = self.epochs[i]
            epoch2 = self.epochs[i + 1]
            if epoch1.end >= epoch2.start:
                return False
        return True

    def construct_behavior_from_config(self, config):
        for i, behav in enumerate(config):
            behav_name, keybind = behav.split()
            self.behaviors[behav_name] = Behavior(
                name=behav_name, keybind=keybind, ID=i, stream=self
            )

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

    def get_behaviors(self):
        return [behavior for _, behavior in self.behaviors.items()]

    def get_epochs(self):
        return self.epochs

    def get_length(self):
        if self.epochs:
            self.sort_epoch()
            last_epoch = self.epochs[len(self.epochs) - 1]
            return last_epoch.end
        else:
            return 0


class Annotation(QtCore.QObject):
    construct_from_file = QtCore.Signal(str)
    content_changed = QtCore.Signal()

    def __init__(self, streams: Dict = {}):
        super().__init__()
        # Use dict to organize streams
        self._streams = streams
        # Behvior-color dict
        self.behav_color = dict()

    @property
    def streams(self):
        return self._streams

    @streams.setter
    def streams(self, new_streams):
        self._streams = new_streams

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
        try:
            for stream_id, annotation_sequence in annots.items():
                # Create behaviors for the stream
                self._streams[stream_id] = Stream(ID=stream_id, epochs=[], behaviors={})
                self._streams[stream_id].construct_behavior_from_config(config)
                self._streams[stream_id].construct_epochs_from_sequence(
                    annotation_sequence
                )
            return True
        except Exception:
            return False

    def get_behaviors(self):
        try:
            streamIDs = list(self.streams.keys())
            stream = self.streams[streamIDs[0]]
            return stream.get_behaviors()
        except Exception:
            return []

    def num_stream(self):
        return len(self.streams)

    def num_epochs(self):
        epoch_lens = []
        for _, stream in self.streams.items():
            epoch_lens.append(len(stream.get_epochs()))
        return epoch_lens

    def assign_behavior_color(self):
        behaviors = self.get_behaviors()
        behavior_names = [i.name for i in behaviors]
        for i, behav in enumerate(behavior_names):
            hue = int(255 * i / len(behavior_names))
            saturation = 200
            value = 255
            self.behav_color[behav] = QColor.fromHsv(hue, saturation, value)
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
