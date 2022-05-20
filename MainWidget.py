import sys

from PyQt6 import uic, QtCore
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QApplication, QWidget, QStyledItemDelegate, QLineEdit, QTableWidgetItem, QLabel, QHBoxLayout

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

        uic.loadUi("ui.ui", self)
        self.configurate_fields()
        self.set_listeners()
        self.set_sizes(self.sizeSpin.value())

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
        self.clear_output()
        solve_thread = SolvingThread(get_element_list_from_table(self.inputTable), parent=self)
        solve_thread.threadFinish.connect(self.fill_output)

        solve_thread.start()
        self.runButton.setEnabled(False)

    def clear_output(self):
        pass
        # for _ in range(self.outputValuesLayout.count()):
        #     self.outputValuesLayout.itemAt(0).widget().setParent(None)
        # for _ in range(self.outputVectorsLayout.count()):
        #     self.outputVectorsLayout.itemAt(0).widget().setParent(None)

    def fill_output(self, result):
        self.runButton.setEnabled(True)
        for key in result.keys():
            hl = QHBoxLayout()
            hl.addWidget(QLabel(str(key)))
            hl.addWidget(QLabel(str(result[key])))
            self.resultLayout.addLayout(hl)

    @staticmethod
    def start_window():
        app = QApplication(sys.argv)
        ex = MainWidget()
        ex.show()
        sys.exit(app.exec())


class SolvingThread(QtCore.QThread):
    threadFinish = QtCore.pyqtSignal(dict)

    def __init__(self, matrix, parent=None):
        super().__init__(parent)
        self.solver = Solver(matrix)

    def run(self, *args, **kwargs):
        self.solver.solve()
        self.threadFinish.emit(self.solver.result)


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
