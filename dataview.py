from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QTableView,
    QAbstractItemView,
    QHeaderView,
)
from PySide6 import QtGui, QtCore
from typing import Optional, List
from state import GuiState
import numpy as np
from data import Stream
import re


class GenericTableModel(QAbstractTableModel):
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

    def get_item_index(self, target, prop):
        # Return row number of the target item
        for i, item in enumerate(self.item_list):
            if item[prop] is target:
                return i
        return None


class BehaviorTableModel(GenericTableModel):
    def __init__(self, behav_list: List = [], *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.item_list = behav_list[0]
        self.all_behaviors = behav_list

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]
        # Color background for color column
        if role == Qt.BackgroundRole and key == "color":
            return QtGui.QBrush(data_item.get_color())
        return super().data(index, role)

    def flags(self, index: QModelIndex):
        if self.properties[index.column()] in ["color", "keybind"]:
            # Keybind and Color are editable
            flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            flags = Qt.ItemIsEnabled
        return flags

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        if self.properties[index.column()] == "color":
            # Verify if the input is a valid hex code
            pattern = re.compile("^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$")
            if bool(pattern.match(value)):
                for stream_behav in self.all_behaviors:
                    stream_behav[index.row()].set_color(QtGui.QColor(value))
                self.dataChanged.emit(index, index)
                return True
            else:
                return False
        if self.properties[index.column()] == "keybind":
            # Verify if the input is a single letter
            pattern = r"^[a-zA-Z]$"
            if bool(re.match(pattern, value)):
                value = value.lower()
            else:
                return False
            # Check if the keybind is occupied
            all_keysbinds = [behav.keybind for behav in self.item_list]
            for i, keybind in enumerate(all_keysbinds):
                if value == keybind:
                    return False
            # Accept the change
            for stream_behav in self.all_behaviors:
                stream_behav[index.row()].set_keybind(value)
            return True


class StatsTableModel(GenericTableModel):
    def __init__(self, behav_lists: List = [], *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        # Reorganize behav_list into item_list
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

        return super().data(index, role)


class StreamTableModel(GenericTableModel):
    def __init__(self, stream: Stream = None, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.stream = stream
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


class GenericTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        header_view = QHeaderView(Qt.Horizontal, self)
        header_view.setSectionsClickable(False)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        super().setHorizontalHeader(header_view)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.SizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.installEventFilter(self)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().item_list[idx.row()]

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )

    def set_columns_fixed(self, columns: List = []):
        for column in columns:
            self.horizontalHeader().setSectionResizeMode(column, QHeaderView.Fixed)
        self.resizeColumnsToContents()
