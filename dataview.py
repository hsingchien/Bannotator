from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
    QItemSelectionModel,
)
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6 import QtGui
from typing import Optional, List
from state import GuiState
import numpy as np
from data import Annotation


class BehaviorTableModel(QAbstractTableModel):
    def __init__(
        self,
        items: Optional[list] = None,
        state: GuiState = None,
    ):
        super().__init__()
        # Key "item" points to the Neuron object
        # Key "visits" keep track of number of past activations
        self.properties = ["ID", "name", "keybind", "color"]
        self.state = state
        self.item_list = items

        self.show_row_numbers = False

        self._selected_index = []  # Keep track of entries in the selected cell list
        # Default sorting order (value for reverse in sort) for ID, Label, Corr, Dist, dFF

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties)  # remove item & visits column

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]

        # Display content
        if role == Qt.DisplayRole and key != "color":
            if isinstance(data_item, dict) and key in data_item:
                return data_item[key]
            if hasattr(data_item, key):
                return getattr(data_item, key)
        # Color background for color column
        if role == Qt.BackgroundRole and key == "color":
            return QtGui.QBrush(getattr(data_item, "color"))
        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return flags

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        """Overrides Qt method, returns column (attribute) names."""
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


class StreamTableModel(QAbstractTableModel):
    def __init__(
        self,
        annotations: Optional[Annotation] = None,
        state: GuiState = None,
    ):
        super().__init__()
        # Key "item" points to the Neuron object
        # Key "visits" keep track of number of past activations
        self.properties = ["name", "start", "end"]
        self.state = state
        self.annotation = annotations

        self.show_row_numbers = False

        self._selected_index = []  # Keep track of entries in the selected cell list
        # Default sorting order (value for reverse in sort) for ID, Label, Corr, Dist, dFF

    def rowCount(self, parent=QModelIndex()):
        # Use the length of the longest epoch list
        return max(self.annotation.num_epochs())

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties) * self.annotation.num_stream()

    def data(self, index, role):
        streamIDs = list(self.annotation.streams.keys())
        key = self.properties[index.column() % 3]
        stream = self.annotation.streams[streamIDs[index.column() // 3]]
        print(streamIDs[index.column() // 3])
        epoch_list = stream.get_epochs()

        idx = index.row()
        if idx >= self.rowCount():
            return None
        if idx >= len(epoch_list):
            return None

        data_item = epoch_list[idx]

        # Display content
        if role == Qt.DisplayRole:
            if isinstance(data_item, dict) and key in data_item:
                return data_item[key]
            if hasattr(data_item, key):
                return getattr(data_item, key)
        # Color background based on activation/selection state
        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return flags

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        # Display first row
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self.properties[idx % 3]
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


class GenericTableView(QTableView):
    def __init__(self, state: GuiState = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeader()
        self.state = state

    def setHorizontalHeader(self):
        header_view = QHeaderView(Qt.Horizontal)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        header_view.setSectionsClickable(False)
        super().setHorizontalHeader(header_view)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().item_list[idx.row()]

    def setstate(self, state: GuiState):
        self.state = state

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
