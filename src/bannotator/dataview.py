from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QTableView,
    QAbstractItemView,
    QHeaderView,
    QColorDialog,
    QInputDialog
)
from PySide6 import QtGui, QtCore
from typing import Optional, List
from bannotator.state import GuiState
from bannotator.data import Stream, Behavior



class GenericTableModel(QAbstractTableModel):
    activated_row_changed = QtCore.Signal(int)
    state_change = QtCore.Signal(object)
    def __init__(
        self,
        items: Optional[list] = None,
        properties: Optional[List[str]] = None,
        state: GuiState = None,
    ):
        super().__init__()
        self._properties = properties
        self.state = state
        self._item_list = items

        self._show_row_numbers = False
        self._activated_index = None
        self._selected_index = []  # Keep track of entries in the selected cell list
        self._current_selection = []  # Keep track of user's current selections

    def _get_item_index(self, target):
        # Return row number of the target item
        for i, item in enumerate(self._item_list):
            if item is target:
                return i
        # Return -1 if not found
        return -1
    
    def _get_property_index(self, target, key):
        # Return row number of the item with the target property
        for i, item in enumerate(self._item_list):
            if isinstance(item, dict) and item.get(key,None) == target:
                return i
            if hasattr(item, key) and getattr(item,key,None) == target:
                return i
        return -1
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._item_list)

    def columnCount(self, parent=QModelIndex()):
        return len(self._properties)

    def data(self, index, role):
        key = self._properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self._item_list[idx]

        # Display content
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if isinstance(data_item, dict) and key in data_item:
                return data_item[key]
            if hasattr(data_item, key):
                return getattr(data_item, key)
        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable  # | Qt.ItemIsEditable
        return flags

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Display property names for each column
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = str(self._properties[idx])
                # use title case if key is lowercase
                if col_str == col_str.lower():
                    return col_str.title()
                # otherwise leave case as is
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self._show_row_numbers:
                    return str(idx + 1)
                return None

        return None

    
    def repaint(self):
        self.dataChanged.emit(self.index(0, 0),self.index(self.rowCount(), self.columnCount()))

    def change_layout(self):
        self.layoutChanged.emit()

class BehaviorTableModel(GenericTableModel):
    activated_behavior_changed = QtCore.Signal(str)
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self._annotation = annotation
        self._all_behaviors = self._annotation.get_behaviors()
        self._item_list = self._all_behaviors[0]

    def _double_click_action(self, row_idx, colum_idx = None):
        if colum_idx == 0:
            # Only clicking ID column activates the row, otherwise edit the entry
            self._activated_index = row_idx
            self.activated_behavior_changed.emit(self._item_list[row_idx].name)
            self.repaint()
        if colum_idx == 3:
            data_item = self._item_list[row_idx]
            current_color = data_item.get_color()
            self.state_change.emit(QAbstractItemView.EditingState)
            new_color = QColorDialog.getColor(current_color,None,"Pick a color for this behavior")
            if new_color.isValid():
                for stream_behav in self._all_behaviors:
                    stream_behav[row_idx].set_color(new_color)
                self.dataChanged.emit(self.index(row_idx,colum_idx), self.index(row_idx,colum_idx))
            self.state_change.emit(QAbstractItemView.NoState)
        if colum_idx == 2:
            data_item = self._item_list[row_idx]
            current_key = data_item.keybind
            all_key_binds = [behav.keybind for behav in self._item_list]
            letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
            available_strokes = [current_key] + [l for l in letters if l not in all_key_binds] + [" "]
            self.state_change.emit(QAbstractItemView.EditingState)
            new_keybind, ok = QInputDialog.getItem(None,"Select a new key", "key",available_strokes,0,False)
            if ok and new_keybind:
                for stream_behav in self._all_behaviors:
                    stream_behav[row_idx].keybind = new_keybind
            self.dataChanged.emit(self.index(row_idx,colum_idx), self.index(row_idx,colum_idx))
            self.state_change.emit(QAbstractItemView.NoState)
        
    def data(self, index, role):
        key = self._properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self._item_list[idx]
        # Color background for color column
        if role == Qt.BackgroundRole and key == "color":
            return QtGui.QBrush(data_item.get_color())
        if role == Qt.BackgroundRole and key != "color" and idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        return super().data(index, role)
    
    def refresh_item_list(self):
        self._all_behaviors = self._annotation.get_behaviors()
        self._item_list = self._all_behaviors[0]
    
    def change_layout(self):
        self.refresh_item_list()
        return super().change_layout()

    def flags(self, index: QModelIndex):
        if self._properties[index.column()] in ["name"]:
            # Keybind and Color are editable
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif self._properties[index.column()] in ["ID","color","keybind"]:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            flags = Qt.ItemIsEnabled
        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        if self._properties[index.column()] == "name":
            # Verify if the input is a valid name
            value = value.lower()
            if value in [behav.name for behav in self._item_list]:
                # Reject name that is already used
                return False
            else:
                for stream_behav in self._all_behaviors:
                    stream_behav[index.row()].name = value
                return True
    
    def receive_activate_behavior(self, behav_name):
        row_idx = self._get_property_index(behav_name,"name")
        self._activated_index = row_idx
        self.repaint()
        
class StatsTableModel(GenericTableModel):
    activated_behavior_changed = QtCore.Signal(str)
    def __init__(self, annotation=None,behav_lists: List = [], *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        # Reorganize behav_list into item_list
        self._annotation = annotation
        behav_lists = self._annotation.get_behaviors()
        for i in range(len(behav_lists)):
            self._properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-prct"
            )
        for i in range(len(behav_lists)):
            self._properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-epochs"
            )
        self._blist_dict = dict()
        for behav_list in behav_lists:
            self._blist_dict["S" + str(behav_list[0].get_stream_ID())] = behav_list
        self._item_list = behav_lists[0]
    
    def _refresh_item_list(self):
        behav_lists = self._annotation.get_behaviors()
        self._item_list = behav_lists[0]
        self._blist_dict = dict()
        for behav_list in behav_lists:
            self._blist_dict["S" + str(behav_list[0].get_stream_ID())] = behav_list
        self._properties = self._properties[0:2]
        for i in range(len(behav_lists)):
            self._properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-prct"
            )
        for i in range(len(behav_lists)):
            self._properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-epochs"
            )

    def _double_click_action(self, row_idx, column_idx=None):
        self._activated_index = row_idx
        self.activated_behavior_changed.emit(self._item_list[row_idx].name)
        self.repaint()
        
    def change_layout(self):
        self._refresh_item_list()
        return super().change_layout()

    def data(self, index, role):
        key = self._properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self._item_list[idx]
        # Color background for color column
        if role == Qt.BackgroundRole and key == "name":
            return QtGui.QBrush(data_item.get_color())
        if role == Qt.DisplayRole and "-prct" in key:
            cur_behav = self._blist_dict[key.split("-")[0]][idx]
            return str(round(100 * cur_behav.get_percentage(), 2)) + "%"
        if role == Qt.DisplayRole and "-epochs" in key:
            cur_behav = self._blist_dict[key.split("-")[0]][idx]
            return cur_behav.num_epochs()
        if role == Qt.BackgroundRole and idx == self._activated_index and key != "name":
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        return super().data(index, role)
    
    def set_activate_by_name(self, behav_name):
        idx = self._get_property_index(behav_name,"name")
        self._double_click_action(idx)
    
    def receive_activate_behavior(self, behav_name):
        row_idx = self._get_property_index(behav_name,"name")
        self._activated_index = row_idx
        self.repaint()
    
    def current_activate_property(self,prop):
        if self._activated_index is not None:
            return getattr(self._item_list[self._activated_index],prop)
        else:
            return None

class StreamTableModel(GenericTableModel):
    jump_to_frame = QtCore.Signal(int)
    def __init__(self, stream: Stream = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self._stream = stream
        stream.behavior_name_changed.connect(self.repaint)
        stream.cur_epoch.connect(self._set_activated_epoch)
        self._item_list = stream.get_epochs()

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Override horizontal header to show stream ID
        streamID = self._stream.ID
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self._properties[idx]
                # Add stream ID to the middle column
                if idx == 1:
                    col_str = "S-" + str(streamID) + "\n" + col_str
                else:
                    col_str = "\n" + col_str
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self._show_row_numbers:
                    return str(idx + 1)
                return None
        return None

    def _set_activated_epoch(self, epoch):
        cur_epoch_idx = self._get_item_index(epoch)
        self._activated_index = cur_epoch_idx
        self.activated_row_changed.emit(cur_epoch_idx)

    
    def _double_click_action(self, row_idx, column_idx = None):
        if self._activated_index != row_idx:
            cur_epoch = self._item_list[row_idx]
            self._activated_index = row_idx
            # Connect to scroll to make sure visible (may not be necessary)
            self.activated_row_changed.emit(row_idx)
            # Connect to set the current frame to the start of this epoch
            self.jump_to_frame.emit(cur_epoch.start-1)

    def data(self, index, role):
        row_idx = index.row()
        if role == Qt.BackgroundRole and row_idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        else:
            return super().data(index, role)
        
class BehavEpochTableModel(GenericTableModel):
    jump_to_frame = QtCore.Signal(int)
    def __init__(self, stream: Stream=None, behavior_name = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self._stream = stream
        behaviors = stream.get_behavior_dict()
        self._stream.cur_epoch.connect(self._set_activated_epoch)
        self._stream.behavior_name_changed.connect(self.repaint)
        if behavior_name in behaviors:
            self._behavior = behaviors[behavior_name]
            self._behavior.epoch_changed.connect(self.change_layout)
        else:
            self._behavior = None
        if isinstance(self._behavior, Behavior):
            self._item_list = self._behavior.get_epochs()
            
        else:
            self._item_list = []
            
    def _double_click_action(self, row_idx, column_idx=None):
        # Called when row is double-clicked
        if self._activated_index != row_idx:
            cur_epoch = self._item_list[row_idx]
            self._activated_index = row_idx
            # Connect to scroll to make sure visible (may not be necessary)
            self.activated_row_changed.emit(row_idx)
            # Connect to set the current frame to the start of this epoch
            self.jump_to_frame.emit(cur_epoch.start-1)
            
    def _set_activated_epoch(self, epoch):
        cur_epoch_idx = self._get_item_index(epoch)
        self._activated_index = cur_epoch_idx
        self.activated_row_changed.emit(cur_epoch_idx)
        
    def _refresh_item_list(self):
        self._item_list = self._behavior.get_epochs()
    
    @QtCore.Slot()
    def set_behavior(self, new_behavior_name):
        if self._behavior is not None:
            self._behavior.epoch_changed.disconnect(self.change_layout)
        self._behavior = self._stream.get_behavior_dict()[new_behavior_name]
        self._behavior.epoch_changed.connect(self.change_layout)
        self.change_layout()
        self._stream.get_epoch_by_idx(self.state["current_frame"])
        
    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Override horizontal header to show stream ID
        streamID = self._stream.ID
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self._properties[idx]
                # Add stream ID to the middle column
                if idx == 1:
                    col_str = "S-" + str(streamID) + "\n" + col_str
                else:
                    col_str = "\n" + col_str
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self._show_row_numbers:
                    return str(idx + 1)
                return None
        return None
    
    def data(self, index, role):
        row_idx = index.row()
        if role == Qt.BackgroundRole and row_idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        else:
            return super().data(index, role)
    
    def jump_to_next(self, frame_number):
        frame_number += 1
        if self._item_list:
            # Find the current epoch
            starts = [epoch.start for epoch in self._item_list]
            idx = list(filter(lambda x: x > frame_number, starts))
            if idx:
                next_epoch = self._item_list[starts.index(idx[0])]
                self._activated_index = starts.index(idx[0])
                self.activated_row_changed.emit(starts.index(idx[0]))
            else:
                next_epoch = self._item_list[0]
                self._activated_index = 0
                self.activated_row_changed.emit(0)
            self.jump_to_frame.emit(next_epoch.start-1)
    
    def jump_to_prev(self, frame_number):
        frame_number+=1
        if self._item_list:
            # Find the current epoch
            starts = [epoch.start for epoch in self._item_list]
            idx = list(filter(lambda x: x < frame_number, starts))
            if idx:
                next_epoch = self._item_list[starts.index(idx[-1])]
                self._activated_index = starts.index(idx[-1])
                self.activated_row_changed.emit(starts.index(idx[-1]))
            else:
                next_epoch = self._item_list[-1]
                self._activated_index = len(self._item_list)-1
                self.activated_row_changed.emit(len(self._item_list)-1)
            self.jump_to_frame.emit(next_epoch.start-1)
                
    def change_layout(self):
        self._refresh_item_list()
        return super().change_layout()

class GenericTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        header_view = QHeaderView(Qt.Horizontal, self)
        header_view.setSectionsClickable(False)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        super().setHorizontalHeader(header_view)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.doubleClicked.connect(self._activate_selected)
    
    def _scroll_to_idx(self, idx):
        if idx != -1:
            self.scrollTo(self.model().index(idx, 0), QAbstractItemView.EnsureVisible)

    def _activate_selected(self):
        self.model()._double_click_action(self.currentIndex().row(),self.currentIndex().column())
        self.selectionModel().clear()
        
    def setModel(self, model) -> None:
        if isinstance(model, GenericTableModel):
            model.state_change.connect(self.setState)
        return super().setModel(model)
    
    def disconnect_scroll(self):
        self.model().activated_row_changed.disconnect(self._scroll_to_idx)
        self.model().activated_row_changed.connect(self.repaint_table)
    
    def connect_scroll(self):
        self.model().activated_row_changed.connect(self._scroll_to_idx)
        self.model().activated_row_changed.connect(self.repaint_table)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().item_list[idx.row()]

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
    
    def change_layout(self):
        self.model().layoutChanged.emit()

    def set_columns_fixed(self, columns: List = []):
        for column in columns:
            self.horizontalHeader().setSectionResizeMode(column, QHeaderView.Fixed)
        self.resizeColumnsToContents()
