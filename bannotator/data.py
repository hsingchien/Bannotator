from PySide6.QtGui import QColor
from PySide6 import QtCore
from typing import List, Dict
import re
import numpy as np
from scipy.io import savemat
import distinctipy as distc


class Epoch(object):
    # Defines unit behavior epoch
    def __init__(
        self,
        stream: "Stream" = None,
        behavior: "Behavior" = None,
        start: int = None,
        end: int = None,
    ) -> None:
        self._behavior = behavior
        self._stream = stream
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
        return self._behavior.name

    @property
    def color(self):
        return self._behavior.get_color()

    @property
    def streamID(self):
        return self._stream.ID

    def __str__(self) -> str:
        return (
            f"Stream {self.streamID} - {self._behavior.name}: {self.start} - {self.end}"
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
        return self._behavior

    def get_stream(self):
        return self._stream

    def set_stream(self, stream):
        self._stream = stream

    def set_behavior(self, new_behavior: "Behavior" = None):
        if new_behavior is None:
            return False
        if new_behavior is not self._behavior:
            self._behavior = new_behavior
            return True

    def set_start_end(self, start: int = None, end: int = None):
        if not (start or end):
            return False
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        return True

    def set_start(self, start: int = None):
        self.start = start

    def set_end(self, end: int = None):
        self.end = end


class Behavior(QtCore.QObject):
    keybind_changed = QtCore.Signal()
    color_changed = QtCore.Signal()
    epoch_changed = QtCore.Signal()
    name_changed = QtCore.Signal(object)

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
        self._keybind = keybind
        self._ID = ID
        self._color = color
        self._epochs = epochs
        self._stream = stream

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if self._name != new_name:
            old_name = self._name
            self._name = new_name
            self.name_changed.emit((old_name, new_name))

    @property
    def keybind(self):
        return self._keybind

    @keybind.setter
    def keybind(self, new_keybind: str = None):
        if self._keybind != new_keybind:
            self._keybind = new_keybind
            self.keybind_changed.emit()
            return True
        else:
            return False

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
        return f"stream: {self._stream}, {self.name}, ID: {self.ID}, keybind: {self._keybind}, color: {self.color}"

    def set_ID(self, new_ID: int = None):
        self.ID = new_ID
        return True

    def set_stream(self, new_stream: "Stream" = None):
        self._stream = new_stream
        return True

    def set_color(self, new_color: QColor = None):
        if self._color != new_color:
            self._color = new_color
            self.color_changed.emit()
            return True
        else:
            return False

    def get_stream_ID(self):
        return self._stream.ID

    def get_color(self):
        return self._color

    def num_epochs(self):
        return len(self._epochs)

    def duration(self):
        if not self._epochs:
            return 0
        duration = 0
        for epo in self._epochs:
            duration += epo.get_length()
        return duration

    def append_epoch(self, epoch: Epoch = None):
        self._epochs.append(epoch)
        self._epochs.sort(key=lambda x: x.start)
        self.epoch_changed.emit()

    def remove_epoch(self, epoch: Epoch = None):
        self._epochs.remove(epoch)
        self.epoch_changed.emit()

    def get_percentage(self):
        dur = self.duration()
        stream_length = self._stream.get_length()
        return dur / stream_length

    def get_epochs(self):
        self._epochs.sort(key=lambda x: x.start)
        return self._epochs

    def remove_redundant_epochs(self):
        def _merge_redundant_epochs(e_list):
            if len(e_list) <= 1:
                return e_list
            else:
                epoch0 = e_list[0]
                the_rest = _merge_redundant_epochs(e_list[1:])
                epoch1 = the_rest[0]
                if epoch1.start - epoch0.end == 1:
                    # Merge 1 and 0
                    epoch1.set_start(epoch0.start)
                    epoch1.get_stream().remove_epoch(epoch0)
                    return the_rest
                else:
                    return [epoch0] + the_rest

        self._epochs = _merge_redundant_epochs(self._epochs)
        self.epoch_changed.emit()


class Stream(QtCore.QObject):
    # Date changed signal, emit updated epoch vector
    data_changed = QtCore.Signal(object)
    # Color changed signal, emit updated color dictionary
    color_changed = QtCore.Signal(object)
    # Current behavior signal, link to the behavior label
    cur_behavior_name = QtCore.Signal(object)
    # Current epoch signal, link to the stream table highlight and scrolling
    cur_epoch = QtCore.Signal(object)
    # Behavior name changed, emit to Annotation to reconstruct its color_dict
    behavior_name_changed = QtCore.Signal(object)
    # Layout change signal, when the NUMBER of epochs/behavior changes
    # Emit to instruct the table to reform the layout
    epoch_number_changed = QtCore.Signal()

    # Defines class Stream to store annotation data
    def __init__(self, ID: int = None, epochs: List = [], behaviors: Dict = {}) -> None:
        super().__init__()
        self._ID = ID
        self._epochs = epochs
        self._behaviors = behaviors
        self._length = self.get_length()
        if not self._behaviors:
            self._keymap = dict()
        else:
            self._map_behav_key()
            for _, be in self._behaviors.items():
                be.keybind_changed.connect(self._map_behav_key)
                be.color_changed.connect(
                    lambda: self.color_changed.emit(self.get_color_dict())
                )
                be.name_changed.connect(self._reconstruct_behavior_dict)
                be.name_changed.connect(lambda x: self.behavior_name_changed.emit(x))

    @property
    def length(self):
        return self._length

    @property
    def ID(self):
        return self._ID

    def sort_epoch(self):
        self._epochs.sort(reverse=False)
        return True

    def _reconstruct_behavior_dict(self):
        # Reconstruct behavior dictionary after behavior name change
        # Key: name, Value: behavior object
        behav_list = [behav for _, behav in self._behaviors.items()]
        behav_list.sort(key=lambda x: x.ID)
        new_dict = {behav.name: behav for behav in behav_list}
        self._behaviors = new_dict

    def validate_epoch(self):
        # Validate epochs to make sure no overlap, no repetitive behavior and no blank
        self.sort_epoch()
        if self._epochs[0].start != 1:
            return False
        for i in range(len(self._epochs) - 1):
            epoch1 = self._epochs[i]
            epoch2 = self._epochs[i + 1]
            if epoch1.name == epoch2.name:
                print("repetitive behavior")
                print(epoch1)
                print(epoch2)
                return False
            if epoch2.start - epoch1.end != 1:
                print("overlap epoch or blank")
                print(epoch1)
                print(epoch2)
                return False
        return True

    def add_behavior(self, name, keybind):
        behav_list = [behav for _, behav in self._behaviors.items()]
        behav_list.sort(key=lambda x: x.ID)
        if name not in [behav.name for behav in behav_list]:
            new_behavior = Behavior(
                name=name,
                keybind=keybind,
                ID=behav_list[-1].ID + 1,
                color=QColor("#000000"),
                epochs=[],
                stream=self,
            )
            self._behaviors[new_behavior.name] = new_behavior
            new_behavior.keybind_changed.connect(self._map_behav_key)
            new_behavior.color_changed.connect(
                lambda: self.color_changed.emit(self.get_color_dict())
            )
            new_behavior.name_changed.connect(self._reconstruct_behavior_dict)
            new_behavior.name_changed.connect(
                lambda x: self.behavior_name_changed.emit(x)
            )
            self._map_behav_key()
            self.color_changed.emit(self.get_color_dict())
            return True
        else:
            return False

    def delete_behavior(self, to_del, to_rep):
        # Remove behavior and merge its epochs with other behaviors
        del_behav = self._behaviors[to_del]
        rep_behav = self._behaviors[to_rep]
        # Move all the epochs from del to rep
        for epoch in del_behav.get_epochs():
            epoch.set_behavior(rep_behav)
            rep_behav.append_epoch(epoch)
        del_behav.get_epochs().clear()
        # If there are neighbor epochs, merge them into one
        rep_behav.remove_redundant_epochs()
        # Remove behavior
        self._behaviors.pop(to_del)
        self._map_behav_key()
        # Emit signal
        self.data_changed.emit(self.get_stream_vect())
        self.color_changed.emit(self.get_color_dict())
        self.epoch_number_changed.emit()

    def remove_epoch(self, epoch):
        # Simply remove epoch from epochs list
        self._epochs.remove(epoch)

    def _map_behav_key(self):
        try:
            self._keymap = dict()
            for _, behav in self._behaviors.items():
                self._keymap[behav.keybind] = behav
        except Exception:
            self._keymap = dict()

    def construct_behavior_from_config(self, config):
        behav_names = []
        keybinds = []
        for i, behav in enumerate(config):
            behav = behav.strip()
            if not behav:
                break
            try:
                behav_name, keybind = behav.split()
            except Exception:
                raise ValueError("Invalid behavior - keybind pair. Check your config file!")
            if behav_name in behav_names or keybind in keybinds:
                raise ValueError("conflict behavior name/keybind assignment")
            behav_names.append(behav_name)
            keybinds.append(keybind)

            self._behaviors[behav_name] = Behavior(
                name=behav_name,
                keybind=keybind,
                ID=i,
                stream=self,
                epochs=[],
                color=QColor("black"),
            )
            self._behaviors[behav_name].keybind_changed.connect(self._map_behav_key)
            self._behaviors[behav_name].color_changed.connect(
                lambda: self.color_changed.emit(self.get_color_dict())
            )
            self._behaviors[behav_name].name_changed.connect(
                self._reconstruct_behavior_dict
            )
            self._behaviors[behav_name].name_changed.connect(
                lambda x: self.behavior_name_changed.emit(x)
            )
        self._map_behav_key()

    def fill_stream(self, behav, length=100):
        if isinstance(behav, str):
            behavior = self._behaviors.get(behav)
        elif isinstance(behav, int):
            behavior = self.get_behavior_list()[behav]
        elif behav is None:
            behavior = self.get_behavior_list()[0]
        if self._epochs and self._epochs[-1].end < length:
            self.sort_epoch()
            last_epoch = self._epochs[-1]
            epoch = Epoch(
                stream=self, behavior=behavior, start=last_epoch.end + 1, end=length
            )
        else:
            self._epochs.clear()
            epoch = Epoch(stream=self, behavior=behavior, start=1, end=length)
        self._epochs.append(epoch)
        behavior.append_epoch(epoch)
        self._length = self.get_length()
        self.data_changed.emit(self.get_stream_vect())

    def truncate(self, start, length):
        end = start + length - 1
        self.sort_epoch()
        # Find the last epoch and its index in the epoch list
        last_epoch = self.get_epoch_by_idx(end - 1, False)
        last_epoch_index = self._epochs.index(last_epoch)
        # Change the end of last epoch
        last_epoch.set_end(end)
        # Find the first epoch and its index in the epoch list
        first_epoch = self.get_epoch_by_idx(start - 1, False)
        first_epoch_index = self._epochs.index(first_epoch)
        # Change the start of the first epoch
        first_epoch.set_start(start)
        # Remove the excessive epochs
        epoch_to_remove = (
            self._epochs[0:first_epoch_index]
            + self._epochs[last_epoch_index + 1 : len(self._epochs)]
        )
        for epoch in epoch_to_remove:
            behavior = epoch.get_behavior()
            behavior.remove_epoch(epoch)
            self._epochs.remove(epoch)
        for epoch in self._epochs:
            epoch.set_start(epoch.start - start + 1)
            epoch.set_end(epoch.end - start + 1)
        self.validate_epoch()
        self._length = self.get_length()
        if self.length == length:
            self.epoch_number_changed.emit()
            return True
        else:
            raise IndexError("Failed to truncate stream")

    def get_stream_vect(self):
        # Returns 1 x stream length vector with each entry being behavior ID
        vec = np.zeros(self.length)
        for epoch in self._epochs:
            start = epoch.start - 1
            end = epoch.end
            vec[start:end] = epoch.get_behavior().ID
        return vec

    def assign_color(self, color_dict):
        for _, behav in self._behaviors.items():
            behav.set_color(color_dict[behav.name])
        self.color_changed.emit(self.get_color_dict())

    def get_color_dict(self):
        color_dict = dict()
        for _, behav in self._behaviors.items():
            color_dict[behav.ID] = behav.get_color()
        return color_dict

    def construct_epochs_from_sequence(self, sequence):
        for i, annot in enumerate(sequence):
            start, end, behav_name = annot.split()
            start = int(start)
            end = int(end)
            epoch = Epoch(
                stream=self, behavior=self._behaviors[behav_name], start=start, end=end
            )
            self._epochs.append(epoch)
            self._behaviors[behav_name].append_epoch(epoch)
        self._length = self.get_length()

        validation = self.validate_epoch()
        if not validation:
            raise ValueError("Invalid annotation. See console for more info!")
        self.data_changed.emit(self.get_stream_vect())

    def get_behavior_list(self):
        behavior_list = [behavior for _, behavior in self._behaviors.items()]
        behavior_list.sort(reverse=False, key=lambda x: x.ID)
        return behavior_list

    def get_behavior_dict(self):
        return self._behaviors

    def get_epochs(self):
        return self._epochs

    def get_epoch_by_idx(self, idx: int, allow_emit=True):
        # Index is frame index, start from 0
        idx = idx + 1
        epochs = self._epochs
        epoch = epochs[int(len(self._epochs) / 2)]
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
            self.cur_behavior_name.emit(epoch.get_behavior())
        return epoch

    def get_behavior_by_idx(self, idx: int):
        epoch = self.get_epoch_by_idx(idx, False)
        return epoch.get_behavior()

    def get_length(self):
        if self._epochs:
            self.sort_epoch()
            last_epoch = self._epochs[len(self._epochs) - 1]
            return last_epoch.end
        else:
            return 0

    def set_behavior(self, fidx: int = None, keypressed: str = None):
        old_length = len(self._epochs)
        # Set behavior upon user keypress
        if not keypressed in self._keymap.keys():
            return False
        epoch = self.get_epoch_by_idx(fidx)
        if epoch.get_behavior().keybind == keypressed:
            return False
        if fidx == epoch.start - 1:
            # Change the whole epoch
            # Check both sides for merge
            old_behavior = epoch.get_behavior()
            old_behavior.remove_epoch(epoch)
            new_behavior = self._keymap[keypressed]
            prev_epoch = self.get_epoch_by_idx(fidx - 1)
            next_epoch = self.get_epoch_by_idx(epoch.end)
            epoch.set_behavior(new_behavior)
            if prev_epoch and epoch.name == prev_epoch.name:
                epoch.set_start_end(prev_epoch.start, epoch.end)
                # Del prev_epoch references
                self._epochs.remove(prev_epoch)
                new_behavior.remove_epoch(prev_epoch)
            if next_epoch and epoch.name == next_epoch.name:
                epoch.set_start_end(epoch.start, next_epoch.end)
                self._epochs.remove(next_epoch)
                new_behavior.remove_epoch(next_epoch)
            new_behavior.append_epoch(epoch)
        else:
            # Make the rest of the current epoch a new epoch
            # Truncate the current epoch to the frame before
            new_start_1 = epoch.start
            new_start_2 = fidx + 1
            new_end_1 = fidx
            new_end_2 = epoch.end
            new_behavior = self._keymap[keypressed]
            epoch.set_start_end(start=new_start_1, end=new_end_1)
            next_epoch = self.get_epoch_by_idx(new_end_2)
            if next_epoch and new_behavior.name == next_epoch.name:
                next_epoch.set_start_end(start=new_start_2, end=next_epoch.end)
            else:
                new_epoch = Epoch(
                    stream=self, behavior=new_behavior, start=new_start_2, end=new_end_2
                )
                new_behavior.append_epoch(new_epoch)
                self._epochs.append(new_epoch)
        validated = self.validate_epoch()
        if not validated:
            raise Exception(
                f"Stream-{self.ID} has problematic epochs (overlapped epoch, repetitive behaviors or unfilled spaces)!"
            )
        if len(self._epochs) != old_length:
            self.epoch_number_changed.emit()
        self.data_changed.emit(self.get_stream_vect())


class Annotation(QtCore.QObject):
    construct_from_file = QtCore.Signal(str)
    content_changed = QtCore.Signal()
    content_layout_changed = QtCore.Signal()
    saved_in_file = QtCore.Signal(str)

    @QtCore.Slot()
    def streams_changed(self):
        self.content_changed.emit()

    @QtCore.Slot()
    def change_layout(self):
        self.content_layout_changed.emit()

    def __init__(self, streams={}):
        super().__init__()
        # breakpoint()
        # Use dict to organize streams
        self._streams = streams
        for _, stream in self._streams.items():
            stream.data_changed.connect(self.streams_changed)
            stream.color_changed.connect(self.streams_changed)
            # stream.behavior_name_changed.connect(self.streams_changed)
            stream.behavior_name_changed.connect(self._rename_color_dict_key)
        # Behvior-color dict
        self._behav_color = dict()
        # self.file_path = os.path.join(os.getcwd(), "annotation.txt")
        self._file_path = None

    def _rename_color_dict_key(self, names):
        # Called after behavior name change.
        # Key: name, value: color.
        old_name = names[0]
        new_name = names[1]
        if old_name in self._behav_color.keys():
            self._behav_color[new_name] = self._behav_color.pop(old_name)

    def _construct_streams(self, config, annots):
        for stream_id, annotation_sequence in annots.items():
            # Create behaviors for the stream
            self._streams[stream_id] = Stream(ID=stream_id, epochs=[], behaviors={})
            self._streams[stream_id].construct_behavior_from_config(config)
            self._streams[stream_id].construct_epochs_from_sequence(annotation_sequence)
            self._streams[stream_id].data_changed.connect(self.streams_changed)
        return True

    def _validate_stream(self):
        for _, stream in self._streams.items():
            if stream.validate_epoch():
                continue
            else:
                return False
        return True

    def _validate_stream_behavior(self):
        # Validate the streams have the same behavior setting
        behav_list = [stream.get_behavior_list() for _, stream in self._streams.items()]
        for i in range(len(behav_list[0])):
            bname = behav_list[0][i].name
            bID = behav_list[0][i].ID
            bcolor = behav_list[0][i].color
            bkbind = behav_list[0][i].keybind
            for j in range(len(behav_list)):
                cur_behav = behav_list[j][i]
                if (
                    cur_behav.name != bname
                    or cur_behav.ID != bID
                    or cur_behav.color != bcolor
                    or cur_behav.keybind != bkbind
                ):
                    return False
        return True

    def get_behaviors(self):
        if self._validate_stream_behavior():
            # Return a list of Behavior objects
            ks = sorted(list(self._streams.keys()))
            return [self._streams[k].get_behavior_list() for k in ks]
        else:
            raise Exception("Inconsisten behaviors across streams")

    def read_config_from_file(self, config_path):
        # Called by mainwindow open configuration
        config = []
        with open(config_path) as file:
            while True:
                k = file.readline()
                if not k:
                    break
                if "nStream" in k:
                    match = re.search(r"nStream\s*(\d+)", k)
                    if match:
                        n_streams = int(match.group(1))
                    else:
                        raise ValueError("invalid stream number in the config file")
                else:
                    config.append(k.strip())
        # Construct empty streams
        for i in range(n_streams):
            self._streams[i+1] = Stream(ID=i + 1, epochs=[], behaviors={})
            self._streams[i+1].construct_behavior_from_config(config)
            self._streams[i+1].data_changed.connect(self.streams_changed)
            self._streams[i+1].color_changed.connect(self.streams_changed)
            self._streams[i+1].behavior_name_changed.connect(self._rename_color_dict_key)

    def set_length(self, length):
        for _, stream in self._streams.items():
            stream.fill_stream(None, length)

    def truncate(self, start, length):
        for _, stream in self._streams.items():
            stream.truncate(start, length)

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
                elif current_anno is not None and "----" not in k:
                    annots[current_anno].append(k.strip())
        success = self._construct_streams(config, annots)
        if success:
            self._file_path = txt_path
            self.construct_from_file.emit(
                "Annotation successfully contructed from file"
            )
        else:
            self.construct_from_file.emit("Failed to construct annotation from file")

    def add_behavior(self, name, keybind):
        for _, stream in self._streams.items():
            stream.add_behavior(name, keybind)
        self._behav_color[name] = QColor("black")
        self.content_layout_changed.emit()

    def delete_behavior(self, to_del, to_rep):
        for _, stream in self._streams.items():
            stream.delete_behavior(to_del, to_rep)
        self.content_layout_changed.emit()

    def num_stream(self):
        return len(self._streams)

    def add_stream(self, behavior=None):
        IDs = sorted(list(self._streams.keys()))
        all_behaviors = self._streams[IDs[0]].get_behavior_list()
        length = self.get_length()
        behav_dict = dict()
        # Create copies of behaviors for the new stream
        for exist_behavior in all_behaviors:
            new_behavior = Behavior(
                name=exist_behavior.name,
                keybind=exist_behavior.keybind,
                ID=exist_behavior.ID,
                color=exist_behavior.get_color(),
                epochs=[],
                stream=None,
            )
            if exist_behavior.name == behavior:
                epoch = Epoch(stream=None, behavior=new_behavior, start=1, end=length)
                new_behavior.append_epoch(epoch)
            behav_dict[new_behavior.name] = new_behavior
        new_stream = Stream(ID=IDs[-1] + 1, epochs=[epoch], behaviors=behav_dict)
        for _, behav in behav_dict.items():
            behav.set_stream(new_stream)
        epoch.set_stream(new_stream)
        # Add stream to the annotation and make connections
        self._streams[new_stream.ID] = new_stream
        new_stream.data_changed.connect(self.streams_changed)
        new_stream.color_changed.connect(self.streams_changed)
        new_stream.behavior_name_changed.connect(self._rename_color_dict_key)
        self.content_layout_changed.emit()
        return new_stream

    def delete_stream(self, del_id):
        if del_id not in self._streams.keys():
            return False
        if len(self._streams) == 1:
            return False
        stream = self._streams.pop(del_id)
        self.content_layout_changed.emit()
        return stream

    def num_epochs(self):
        epoch_lens = []
        for _, stream in self._streams.items():
            epoch_lens.append(len(stream.get_epochs()))
        return epoch_lens

    def assign_behavior_color(self, rng=None):
        self._behav_color.clear()
        behaviors = self.get_behaviors()
        behavior_names = [i.name for i in behaviors[0]]
        non_blank_behaviors = [
            name for name in behavior_names if name not in ("other", "blank")
        ]
        colors = distc.get_colors(
            len(non_blank_behaviors),
            exclude_colors=[(0.47, 0.47, 0.47), (1, 1, 1), (0, 0, 0)],
            n_attempts=500,
            pastel_factor=0.1,
            rng=rng,
        )
        i = 0
        for behav in behavior_names:
            if behav not in ("other", "blank"):
                self._behav_color[behav] = QColor.fromRgbF(*colors[i])
                i += 1
            else:
                self._behav_color[behav] = QColor.fromRgbF(0.47, 0.47, 0.47)
        # Assign colors to the behavior objects for all the streams
        for _, stream in self._streams.items():
            stream.assign_color(self._behav_color)
        self.streams_changed()

    def get_stream_vects(self):
        vec_dict = dict()
        for i in self._streams.keys():
            vec_dict[i] = self._streams[i].get_stream_vect()
        return vec_dict

    def get_streams(self):
        return self._streams

    def get_stream(self, id):
        return self._streams.get(id, None)

    def get_length(self):
        length = 0
        for _, i in self._streams.items():
            length = max(i.length, length)
        return length

    def save_to_matfile(self, filename):
        valid = self._validate_stream()
        if not valid:
            Warning(
                "Annotation might contain blank, overlaping epoches, or repetitive epochs."
            )
        # Generate t x nstream vector, save stream vector into it
        t = self.get_length()
        vect = np.zeros((t, len(self._streams)))
        stream_ids = []
        i = 0
        for id, stream in self._streams.items():
            stream_ids.append(id)
            vect[:, i] = stream.get_stream_vect()
            i += 1
        behavior_dict = dict()
        for behavior in self.get_behaviors()[0]:
            behavior_dict[behavior.name] = behavior.ID
        mat_file = {"annotation": dict()}
        mat_file["annotation"]["stream_ID"] = stream_ids
        mat_file["annotation"]["annotation"] = vect
        mat_file["annotation"]["behaviors"] = behavior_dict
        savemat(filename, mat_file)
        self.saved_in_file.emit(f"Saved annotation to {filename} successfully!")
        return True

    def save_to_file(self, filename, auto_save=False):
        valid = self._validate_stream()
        if not valid:
            Warning(
                "Annotation might contain blank, overlaping epoches, or repetitive epochs."
            )
        # try:
        with open(filename, "w") as f:
            f.write("Caltech Behavior Annotator - Annotation File\n")
            f.write("\nConfiguration file:\n")
            self.write_behavior(f)
            f.write("\n")
            self.write_streams(f)
        if not auto_save:
            self.saved_in_file.emit(f"Saved annotation to {filename} successfully!")
            # If save is not from auto save, set the annotation path to the saved path
            self._file_path = filename
        return True
        # except Exception:
        #     return False

    def save_config_to_file(self, filename):
        num_streams = len(self._streams)
        # try:
        with open(filename, "w") as f:
            f.write("nStream " + str(num_streams) + "\n")
            self.write_behavior(f)
        self.saved_in_file.emit(f"Saved config to {filename} successfully!")
        return True

    def write_behavior(self, f):
        config = self.get_behaviors()[0]
        lines = []
        for behav in config:
            lines.append(behav.name + "\t" + behav.keybind + "\n")
        if f:
            f.writelines(lines)

    def write_streams(self, f):
        lines = []
        for _, stream in self._streams.items():
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

    def get_file_path(self):
        return self._file_path
