import sys

from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QApplication, QWidget, QStyledItemDelegate, QLineEdit, QTableWidgetItem, QLabel, QHBoxLayout

from InfoWidget import InfoWidget
from Solver import Solver
from Exceptions import *


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
        solve_thread.threadExceptionCaught.connect(self.on_error)

        solve_thread.start()
        self.runButton.setEnabled(False)

    def on_error(self, e: CustomException):
        self.runButton.setEnabled(True)
        show_info_widget(1, e.message, e.details)

    def clear_output(self):
        for _ in range(self.resultLayout.count()):
            layout = self.resultLayout.itemAt(0).layout()
            for _ in range(layout.count()):
                layout.itemAt(0).widget().setParent(None)
            layout.setParent(None)

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


def show_info_widget(code, message, details=None):
    i = InfoWidget(code, message, details)
    i.show_popup()


class SolvingThread(QtCore.QThread):
    threadFinish = QtCore.pyqtSignal(dict)
    threadExceptionCaught = QtCore.pyqtSignal(CustomException)

    def __init__(self, matrix, parent=None):
        super().__init__(parent)
        self.solver = Solver(matrix)

    def run(self, *args, **kwargs):
        try:
            self.solver.solve()
            self.threadFinish.emit(self.solver.result)
        except CustomException as e:
            self.threadExceptionCaught.emit(e)


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

# import sys
# import traceback
# import logging
#
# # basic logger functionality
# log = logging.getLogger(__name__)
# handler = logging.StreamHandler(stream=sys.stdout)
# log.addHandler(handler)
#
#
# def show_exception_box(log_msg):
#     """Checks if a QApplication instance is available and shows a messagebox with the exception message.
#     If unavailable (non-console application), log an additional notice.
#     """
#     if QtWidgets.QApplication.instance() is not None:
#         # errorbox = QtWidgets.QMessageBox()
#         # errorbox.setText("Oops. An unexpected error occured:\n{0}".format(log_msg))
#         # errorbox.exec()
#         errorbox = InfoWidget(1, "Error", "Oops. An unexpected error occured:\n{0}".format(log_msg))
#         errorbox.show_popup()
#     else:
#         log.debug("No QApplication instance available.")
#
#
# class UncaughtHook(QtCore.QObject):
#     _exception_caught = QtCore.pyqtSignal(object)
#
#     def __init__(self, *args, **kwargs):
#         super(UncaughtHook, self).__init__(*args, **kwargs)
#
#         # this registers the exception_hook() function as hook with the Python interpreter
#         sys.excepthook = self.exception_hook
#
#         # connect signal to execute the message box function always on main thread
#         self._exception_caught.connect(show_exception_box)
#
#     def exception_hook(self, exc_type, exc_value, exc_traceback):
#         """Function handling uncaught exceptions.
#         It is triggered each time an uncaught exception occurs.
#         """
#         if issubclass(exc_type, KeyboardInterrupt):
#             # ignore keyboard interrupt to support console applications
#             sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         else:
#             exc_info = (exc_type, exc_value, exc_traceback)
#             log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
#                                  '{0}: {1}'.format(exc_type.__name__, exc_value)])
#             log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)
#
#             # trigger message box show
#             self._exception_caught.emit(log_msg)
#
#
# # create a global instance of our class to register the hook
# qt_exception_hook = UncaughtHook()
