from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QDateEdit, QComboBox, QPushButton
from storage.excel import save_cases
from PySide6.QtCore import QDate, Signal


class add_case(QWidget):
    case_signal = Signal()
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.form = QFormLayout()
        self.main_layout.addLayout(self.form)
        self.client = QLineEdit()
        self.form.addRow('Client/Employee', self.client)
        self.status = QComboBox()
        self.status.addItems(['Waiting Me', 'Waiting Client', 'Waiting Dep', 'Done'])
        self.form.addRow('Status', self.status)
        self.deadline = QDateEdit()
        self.deadline.setCalendarPopup(True)
        self.deadline.setDate(QDate.currentDate())
        self.form.addRow('Deadline', self.deadline)
        self.note = QTextEdit()
        self.note.setMinimumHeight(60)
        self.form.addRow('Notes', self.note)
        self.save_btn = QPushButton('Save Case')
        self.main_layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_handler)
        self.save_btn.setEnabled(False)
        self.client.textChanged.connect(self.check_form)
        self.note.textChanged.connect(self.check_form)

    def check_form(self):
        if self.client.text() and self.note.toPlainText():
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)

    def save_handler(self):
        try:
            client = self.client.text()
            notes = self.note.toPlainText()
            status = self.status.currentText()
            deadline = self.deadline.date()
        except Exception as e:
            print(f'cannot save: {e}')
        save_cases(client, notes, status, deadline)
        self.client.clear()
        self.note.clear()
        self.status.setCurrentIndex(0)
        self.deadline.setDate(QDate.currentDate())
        self.case_signal.emit()


