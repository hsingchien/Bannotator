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
        # Horizontal header
        streamIDs = list(self.annotation.streams.keys())
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = self.properties[idx % 3]
                # use title case if key is lowercase
                if idx % 3 == 1:
                    col_str = "Stream " + str(streamIDs[idx // 3]) + "\n" + col_str
                else:
                    col_str = "\n" + col_str
                # otherwise leave case as is
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self.show_row_numbers:
                    return str(idx + 1)
                return None

        return None

    # def get_item_index(self, target_stream, prop):
    #     # Return row number of the target item
    #     for i, item in enumerate(self.item_list):
    #         if item[prop] is target:
    #             return i
    #     return None


class GenericTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        header_view = QHeaderView(Qt.Horizontal, self)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
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


class StreamHeaderView(QHeaderView):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setSectionResizeMode(QHeaderView.Stretch)
        self.setSectionsClickable(False)
        self.line_pos = set()

    def paintSection(self, painter, rect, logicalIndex):
        if logicalIndex % 3 == 0 and logicalIndex // 3 > 0:
            painter.save()
            painter.setPen(QtGui.QPen(QtGui.QColor("black"), 2, Qt.SolidLine))
            painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
            painter.restore()
            self.line_pos.add(rect.left())
        super().paintSection(painter, rect, logicalIndex)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self.viewport())
        painter.save()
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 2, Qt.SolidLine))
        for lpos in self.line_pos:
            painter.drawLine(
                lpos,
                self.rect().top(),
                lpos,
                self.rect().bottom(),  # self.sectionViewportPosition(0)
            )
        painter.restore()
        painter.end()


class StreamTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        header_view = StreamHeaderView(Qt.Horizontal, self)
        self.setHorizontalHeader(header_view)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QtGui.QPainter(self.viewport())

        solid_pen = QtGui.QPen(Qt.SolidLine)
        solid_pen.setWidth(2)
        painter.setPen(solid_pen)
        try:
            for column in range(3, self.model().columnCount(), 3):
                column_left = self.columnViewportPosition(column)
                painter.drawLine(column_left, 0, column_left, self.viewport().height())
        except Exception:
            pass
        painter.end()
