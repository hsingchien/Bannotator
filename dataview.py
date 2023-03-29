from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QTableView,
    QAbstractItemView,
    QHeaderView,
    QAbstractScrollArea,
)
from PySide6 import QtGui
from typing import Optional, List
from state import GuiState
import numpy as np
from data import Stream


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
        if role == Qt.DisplayRole:
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
        for i in range(header_view.count()):
            header_view.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        header_view.setSectionsClickable(False)

        super().setHorizontalHeader(header_view)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().item_list[idx.row()]

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )

    def resizeColumnsToContents(self) -> None:
        super().resizeColumnsToContents()
        viewport = self.viewport()
        min_width = (
            self.horizontalHeader().length()
            + self.verticalHeader().width() * 2
            + self.verticalScrollBar().width()
        )
        viewport.setFixedWidth(min_width)
        self.setFixedWidth(min_width)

    # def sizeHint(self):
    #     width = self.horizontalHeader().length() + self.verticalScrollBar().width()
    #     height = self.verticalHeader().length()
    #     return QSize(width, height)
