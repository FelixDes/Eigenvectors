from PyQt6.QtWidgets import QMessageBox

message_type = {0: "Information", 1: "Error", 2: "Warning", 3: "Question"}


class InfoWidget:

    def __init__(self, case, text, details=None):
        self.case = case
        self.text = text
        self.details = details

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle(message_type.get(self.case))
        self.set_icon(msg)
        msg.setText(self.text)
        if self.details is not None:
            msg.setDetailedText(self.details)

        msg.exec()

    def set_icon(self, msg):
        match self.case:
            case 0:
                msg.setIcon(QMessageBox.Icon.Information)
            case 1:
                msg.setIcon(QMessageBox.Icon.Critical)
            case 2:
                msg.setIcon(QMessageBox.Icon.Warning)
            case 3:
                msg.setIcon(QMessageBox.Icon.Question)
