from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget , QHeaderView , QTableWidgetItem , QPushButton
from storage.excel import load_cases , update_case


class all_case(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.second_layout = QHBoxLayout()
        self.main_layout.addLayout(self.second_layout)
        self.setLayout(self.main_layout)


        self.search_bar = QLineEdit()
        self.second_layout.addWidget(self.search_bar)

        self.status = QComboBox()
        self.second_layout.addWidget(self.status)
        self.status.addItem('All Status')
        self.status.addItem('Done')
        self.status.addItem('Waiting Dep')
        self.status.addItem('Waiting Me.')
        self.status.addItem('Waiting Client')
        self.status.currentTextChanged.connect(self.apply_status_filter)

        self.table = QTableWidget(0, 4)
        self.main_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(['Client/Employee', 'Notes', 'Status', 'Deadline'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_insert()

        # save button.
        self.save_btn = QPushButton('Save')
        self.main_layout.addWidget(self.save_btn)
        self.save_btn.setVisible(False)
        self.save_btn.clicked.connect(self.save_handler)
        self.table.cellChanged.connect(self.show_save_btn)

    def apply_status_filter(self):
        self.status_filter = self.status.currentText()
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 2)
            status_value = combo.currentText()
            if self.status_filter =='All Status' or status_value ==self.status_filter:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def show_save_btn(self, row , column):
        self.save_btn.setVisible(True)
        self.edited_row = row
        self.edited_column = column
        self.edited_value = self.table.item(row, column).text()

    def save_handler(self):
        update_case(self.edited_row, self.edited_column, self.edited_value)
        self.save_btn.setVisible(False)

    def combo_changed(self, row, column, text):
        self.save_btn.setVisible(True)
        self.edited_row = row
        self.edited_column = column
        self.edited_value = text

    def table_insert(self):
        self.table.setRowCount(0)
        for row in load_cases():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(row[1])))

            combo = QComboBox()
            combo.addItems(['Done', 'Waiting Dep', 'Waiting Me.', 'Waiting Client'])
            combo.setCurrentText(str(row[2]))
            combo.currentTextChanged.connect(lambda text, r=row_position: self.combo_changed(r, 2, text))
            self.table.setCellWidget(row_position, 2, combo)

            self.table.setItem(row_position, 3, QTableWidgetItem(str(row[3])))










