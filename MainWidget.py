import sys

from PyQt6 import uic
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QPushButton, QTableWidget, QScrollArea, QApplication, QWidget, \
    QStyledItemDelegate, QLineEdit, QTableWidgetItem

from Solver import Solver


class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            reg_ex = QRegularExpression("([+-]?\d+(?:\.\d+)?)")
            validator = QRegularExpressionValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.solver = Solver()

        uic.loadUi("ui.ui", self)
        self.configurate_fields()
        self.set_listeners()

    def configurate_fields(self):
        delegate = NumericDelegate(self.inputTable)
        self.inputTable.setItemDelegate(delegate)

    def set_listeners(self):
        self.sizeSpin.valueChanged.connect(lambda x: self.set_sizes(x))
        self.runButton.clicked.connect(self.run)

    def set_sizes(self, size):
        self.inputTable.setRowCount(size)
        self.inputTable.setColumnCount(size)

    def run(self):
        fill_empty_cells_with_zeroes(self.inputTable)
        self.solver.solve(get_element_list_from_table(self.inputTable))

    @staticmethod
    def start_window():
        app = QApplication(sys.argv)
        ex = MainWidget()
        ex.show()
        sys.exit(app.exec())


def fill_empty_cells_with_zeroes(table):  # пустые ячейки заполяем нулями
    for i in range(table.rowCount()):
        for j in range(table.columnCount()):
            if not (table.item(i, j) is not None) or not (table.item(i, j).text() != ''):
                table.setItem(i, j, QTableWidgetItem("0"))


def get_element_list_from_table(table) -> list:
    lst = list()
    for i in range(table.rowCount()):
        sub_lst = list()
        for j in range(table.columnCount()):
            sub_lst.append(float(table.item(i, j).text()))
        lst.append(sub_lst)
    return lst

