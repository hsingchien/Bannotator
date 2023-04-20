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
import re



class GenericTableModel(QAbstractTableModel):
    activated_row_changed = QtCore.Signal(int)

    def __init__(
        self,
        items: Optional[list] = None,
        properties: Optional[List[str]] = None,
        state: GuiState = None,
    ):
        super().__init__()
        self.properties = properties
        self.state = state
        self.item_list = items

        self.show_row_numbers = False
        self._activated_index = None
        self._selected_index = []  # Keep track of entries in the selected cell list
        self._current_selection = []  # Keep track of user's current selections

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties)

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]

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
                col_str = str(self.properties[idx])
                # use title case if key is lowercase
                if col_str == col_str.lower():
                    return col_str.title()
                # otherwise leave case as is
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self.show_row_numbers:
                    return str(idx + 1)
                return None

        return None

    def get_item_index(self, target):
        # Return row number of the target item
        for i, item in enumerate(self.item_list):
            if item is target:
                return i
        # Return -1 if not found
        return -1
    
    def get_property_index(self, target, key):
        # Return row number of the item with the target property
        for i, item in enumerate(self.item_list):
            if isinstance(item, dict) and item.get(key,None) == target:
                return i
            if hasattr(item, key) and getattr(item,key,None) == target:
                return i
        return -1
            
    
    def repaint(self):
        self.dataChanged.emit(self.index(0, 0),self.index(self.rowCount(), self.columnCount()))

    def change_layout(self):
        self.layoutChanged.emit()


class BehaviorTableModel(GenericTableModel):
    activated_behavior_changed = QtCore.Signal(str)
    def __init__(self, annotation=None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.annotation = annotation
        self.all_behaviors = self.annotation.get_behaviors()
        self.item_list = self.all_behaviors[0]

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]
        # Color background for color column
        if role == Qt.BackgroundRole and key == "color":
            return QtGui.QBrush(data_item.get_color())
        if role == Qt.BackgroundRole and key != "color" and idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        return super().data(index, role)
    
    def refresh_item_list(self):
        self.all_behaviors = self.annotation.get_behaviors()
        self.item_list = self.all_behaviors[0]
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        if self.properties[index.column()] in ["name"]:
            # Keybind and Color are editable
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif self.properties[index.column()] in ["ID","color","keybind"]:
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            flags = Qt.ItemIsEnabled
        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        if self.properties[index.column()] == "name":
            # Verify if the input is a valid name
            value = value.lower()
            if value in [behav.name for behav in self.item_list]:
                # Reject name that is already used
                return False
            else:
                for stream_behav in self.all_behaviors:
                    stream_behav[index.row()].name = value
                return True
    
    def double_click_action(self, row_idx, colum_idx = None):
        if colum_idx == 0:
            # Only clicking ID column activates the row, otherwise edit the entry
            self._activated_index = row_idx
            self.activated_behavior_changed.emit(self.item_list[row_idx].name)
            self.repaint()
        if colum_idx == 3:
            data_item = self.item_list[row_idx]
            current_color = data_item.get_color()
            new_color = QColorDialog.getColor(current_color,None,"Pick a color for this behavior")
            if new_color.isValid():
                for stream_behav in self.all_behaviors:
                    stream_behav[row_idx].set_color(new_color)
                self.dataChanged.emit(self.index(row_idx,colum_idx), self.index(row_idx,colum_idx))
        if colum_idx == 2:
            data_item = self.item_list[row_idx]
            current_key = data_item.get_keybind()
            all_key_binds = [behav.get_keybind() for behav in self.item_list]
            letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
            available_strokes = [current_key] + [l for l in letters if l not in all_key_binds] + [" "]
            new_keybind, ok = QInputDialog.getItem(None,"Select a new key", "key",available_strokes,0,False)
            if ok and new_keybind:
                for stream_behav in self.all_behaviors:
                    stream_behav[row_idx].set_keybind(new_keybind)
            self.dataChanged.emit(self.index(row_idx,colum_idx), self.index(row_idx,colum_idx))
        
    def receive_activate_behavior(self, behav_name):
        row_idx = self.get_property_index(behav_name,"name")
        self._activated_index = row_idx
        self.repaint()
        
    

class StatsTableModel(GenericTableModel):
    activated_behavior_changed = QtCore.Signal(str)
    def __init__(self, annotation=None,behav_lists: List = [], *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        # Reorganize behav_list into item_list
        self.annotation = annotation
        behav_lists = self.annotation.get_behaviors()
        for i in range(len(behav_lists)):
            self.properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-prct"
            )
        for i in range(len(behav_lists)):
            self.properties.append(
                "S" + str(behav_lists[i][0].get_stream_ID()) + "-epochs"
            )
        self.blist_dict = dict()
        for behav_list in behav_lists:
            self.blist_dict["S" + str(behav_list[0].get_stream_ID())] = behav_list
        self.item_list = behav_lists[0]
    
    def refresh_item_list(self):
        behav_lists = self.annotation.get_behaviors()
        self.item_list = behav_lists[0]
        self.blist_dict = dict()
        for behav_list in behav_lists:
            self.blist_dict["S" + str(behav_list[0].get_stream_ID())] = behav_list
        self.layoutChanged.emit()
        print("refreshed")


    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]
        # Color background for color column
        if role == Qt.BackgroundRole and key == "name":
            return QtGui.QBrush(data_item.get_color())
        if role == Qt.DisplayRole and "-prct" in key:
            cur_behav = self.blist_dict[key.split("-")[0]][idx]
            return str(round(100 * cur_behav.get_percentage(), 2)) + "%"
        if role == Qt.DisplayRole and "-epochs" in key:
            cur_behav = self.blist_dict[key.split("-")[0]][idx]
            return cur_behav.num_epochs()
        if role == Qt.BackgroundRole and idx == self._activated_index and key != "name":
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        return super().data(index, role)
    
    def double_click_action(self, row_idx, column_idx=None):
        self._activated_index = row_idx
        self.activated_behavior_changed.emit(self.item_list[row_idx].name)
        self.repaint()
    
    def receive_activate_behavior(self, behav_name):
        row_idx = self.get_property_index(behav_name,"name")
        self._activated_index = row_idx
        self.repaint()


class StreamTableModel(GenericTableModel):
    jump_to_frame = QtCore.Signal(int)
    def __init__(self, stream: Stream = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.stream = stream
        stream.behavior_name_changed.connect(self.repaint)
        stream.cur_epoch.connect(self.set_activated_epoch)
        self.item_list = stream.get_epochs()

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Override horizontal header to show stream ID
        streamID = self.stream.ID
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self.properties[idx]
                # Add stream ID to the middle column
                if idx == 1:
                    col_str = "S-" + str(streamID) + "\n" + col_str
                else:
                    col_str = "\n" + col_str
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self.show_row_numbers:
                    return str(idx + 1)
                return None
        return None

    def set_activated_epoch(self, epoch):
        cur_epoch_idx = self.get_item_index(epoch)
        self._activated_index = cur_epoch_idx
        self.activated_row_changed.emit(cur_epoch_idx)

    def data(self, index, role):
        row_idx = index.row()
        if role == Qt.BackgroundRole and row_idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        else:
            return super().data(index, role)
    
    def double_click_action(self, row_idx, column_idx = None):
        if self._activated_index != row_idx:
            cur_epoch = self.item_list[row_idx]
            self._activated_index = row_idx
            # Connect to scroll to make sure visible (may not be necessary)
            self.activated_row_changed.emit(row_idx)
            # Connect to set the current frame to the start of this epoch
            self.jump_to_frame.emit(cur_epoch.start-1)

class BehavEpochTableModel(GenericTableModel):
    jump_to_frame = QtCore.Signal(int)
    def __init__(self, stream: Stream=None, behavior_name = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.stream = stream
        behaviors = stream.get_behavior_dict()
        self.stream.cur_epoch.connect(self.set_activated_epoch)
        self.stream.behavior_name_changed.connect(self.repaint)
        self.stream.epoch_number_changed.connect(self.change_layout)
        if behavior_name in behaviors:
            self.behavior = behaviors[behavior_name]
        else:
            self.behavior = None
        if isinstance(self.behavior, Behavior):
            self.item_list = self.behavior.get_epochs()
        else:
            self.item_list = []
            
    @QtCore.Slot()
    def set_behavior(self, new_behavior_name):
        self.behavior = self.stream.get_behavior_dict()[new_behavior_name]
        self.item_list = self.behavior.get_epochs()
        self.layoutChanged.emit()
        self.stream.get_epoch_by_idx(self.state["current_frame"])
        
    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Override horizontal header to show stream ID
        streamID = self.stream.ID
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self.properties[idx]
                # Add stream ID to the middle column
                if idx == 1:
                    col_str = "S-" + str(streamID) + "\n" + col_str
                else:
                    col_str = "\n" + col_str
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self.show_row_numbers:
                    return str(idx + 1)
                return None
        return None
    
    def data(self, index, role):
        row_idx = index.row()
        if role == Qt.BackgroundRole and row_idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        else:
            return super().data(index, role)
    
    def double_click_action(self, row_idx, column_idx=None):
        # Called when row is double-clicked
        if self._activated_index != row_idx:
            cur_epoch = self.item_list[row_idx]
            self._activated_index = row_idx
            # Connect to scroll to make sure visible (may not be necessary)
            self.activated_row_changed.emit(row_idx)
            # Connect to set the current frame to the start of this epoch
            self.jump_to_frame.emit(cur_epoch.start-1)
    
    def set_activated_epoch(self, epoch):
        cur_epoch_idx = self.get_item_index(epoch)
        self._activated_index = cur_epoch_idx
        self.activated_row_changed.emit(cur_epoch_idx)
            
        

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
        self.doubleClicked.connect(self.activate_selected)
    
    def disconnect_scroll(self):
        self.model().activated_row_changed.disconnect(self.scroll_to_idx)
        self.model().activated_row_changed.connect(self.repaint_table)
    
    def connect_scroll(self):
        self.model().activated_row_changed.connect(self.scroll_to_idx)
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

    def scroll_to_idx(self, idx):
        if idx != -1:
            self.scrollTo(self.model().index(idx, 0), QAbstractItemView.EnsureVisible)

    def activate_selected(self):
        self.model().double_click_action(self.currentIndex().row(),self.currentIndex().column())
        self.selectionModel().clear()
        