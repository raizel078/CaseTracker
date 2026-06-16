from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QLabel
from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox
from storage.excel import load_cases, update_case
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from datetime import datetime, date


class all_case(QWidget):
    def __init__(self):
        super().__init__()
        self.pending_changes = {}

        #main layout
        self.main_layout = QVBoxLayout()
        self.second_layout = QHBoxLayout()
        self.main_layout.addLayout(self.second_layout)
        self.setLayout(self.main_layout)

        #for the search bar in ui.
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search by client or note...')
        self.second_layout.addWidget(self.search_bar)
        self.search_bar.textChanged.connect(self.apply_search) # connecting to function.
        #all status comboBox
        self.status = QComboBox()
        self.second_layout.addWidget(self.status)
        self.status.addItem('All Status')
        self.status.addItem('Done')
        self.status.addItem('Waiting Dep')
        self.status.addItem('Waiting Me')
        self.status.addItem('Waiting Client')
        self.status.currentTextChanged.connect(self.apply_status_filter) # connecting to another function.

        self.table = QTableWidget(0, 4)
        self.main_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(['Client/Employee', 'Notes', 'Status', 'Deadline'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setMinimumHeight(100)
        self.table_insert()

        self.third_layout = QHBoxLayout()
        self.status_label = QLabel()
        self.third_layout.addWidget(self.status_label)
        self.save_btn = QPushButton('Save')
        self.save_btn.setVisible(False)
        self.third_layout.addWidget(self.save_btn)
        self.main_layout.addLayout(self.third_layout)

        self.save_btn.clicked.connect(self.save_handler)
        self.table.cellChanged.connect(self.show_save_btn)
        self.count_status()

    def parse_deadline(self, deadline_text):
        try:
            return datetime.strptime(str(deadline_text), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None

    def apply_row_style(self, row):
        deadline_item = self.table.item(row, 3)
        combo = self.table.cellWidget(row, 2)
        status_value = combo.currentText() if combo else ''
        deadline_value = self.parse_deadline(deadline_item.text() if deadline_item else None)
        is_done = status_value == 'Done'

        text_color = QColor('black')
        if is_done:
            text_color = QColor('gray')
        elif deadline_value and deadline_value < date.today():
            text_color = QColor('red')

        for column in [0, 1, 3]:
            item = self.table.item(row, column)
            if item:
                item.setForeground(text_color)
                font = item.font()
                font.setStrikeOut(is_done)
                item.setFont(font)

        self.table.setRowHeight(row, 24)

        if combo:
            combo_font = combo.font()
            combo_font.setStrikeOut(is_done)
            combo.setFont(combo_font)
            combo.setStyleSheet(f'color: {text_color.name()};')

    def apply_search(self):
        search_text = self.search_bar.text().lower()
        for row in range(self.table.rowCount()):
            client_item = self.table.item(row, 0)
            note_item = self.table.item(row, 1)

            client = client_item.text().lower() if client_item else ''
            note = note_item.text().lower() if note_item else ''

            if search_text in client or search_text in note:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def count_status(self):
        all_status = []
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 2)
            if combo:
                status_value = combo.currentText()
                all_status.append(status_value)

        done = all_status.count('Done')
        dep = all_status.count('Waiting Dep')
        me = all_status.count('Waiting Me')
        client = all_status.count('Waiting Client')
        self.status_label.setText(f'Done:{done}  Waiting Dep:{dep}  Waiting Me:{me}  Waiting Client: {client}')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def apply_status_filter(self):
        self.status_filter = self.status.currentText()
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 2)
            if not combo:
                continue

            status_value = combo.currentText()
            if self.status_filter == 'All Status' or status_value == self.status_filter:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def show_save_btn(self, row, column):
        item = self.table.item(row, column)
        if item is None:
            return

        if row >= len(self.row_source_map):
            return

        source_row = self.row_source_map[row]
        self.pending_changes[(source_row, column)] = item.text()
        self.save_btn.setVisible(True)

    def save_handler(self):
        if not self.pending_changes:
            self.save_btn.setVisible(False)
            return

        try:
            for (source_row, column), value in self.pending_changes.items():
                update_case(source_row, column, value)
        except PermissionError:
            QMessageBox.critical(
                self,
                'Excel file is open',
                'Please close cases.xlsx in Excel, then try saving again.'
            )
            return
        except Exception as error:
            QMessageBox.critical(
                self,
                'Save failed',
                f'Could not save changes:\n{error}'
            )
            return

        self.pending_changes.clear()
        self.save_btn.setVisible(False)

        for row in range(self.table.rowCount()):
            self.apply_row_style(row)

        self.count_status()

    def combo_changed(self, text):
        combo = self.sender()
        if combo is None:
            return

        changed_row = -1
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 2) == combo:
                changed_row = row
                break

        if changed_row == -1:
            return

        if changed_row >= len(self.row_source_map):
            return

        source_row = self.row_source_map[changed_row]
        self.pending_changes[(source_row, 2)] = text

        self.save_btn.setVisible(True)
        self.apply_row_style(changed_row)
        self.count_status()

    def table_insert(self):
        self.table.setRowCount(0)
        raw_rows = list(enumerate(load_cases()))
        raw_rows.sort(key=lambda x: self.parse_deadline(x[1][3]) or date.max)
        self.row_source_map = []

        for source_row, row in raw_rows:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.row_source_map.append(source_row)

            self.table.setItem(row_position, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(row[1])))

            combo = QComboBox()
            combo.addItems(['Done', 'Waiting Dep', 'Waiting Me', 'Waiting Client'])

            status_text = str(row[2])
            if status_text == 'Waiting Me.':
                status_text = 'Waiting Me'

            combo.setCurrentText(status_text)
            combo.currentTextChanged.connect(self.combo_changed)
            self.table.setCellWidget(row_position, 2, combo)

            self.table.setItem(row_position, 3, QTableWidgetItem(str(row[3])))
            self.apply_row_style(row_position)