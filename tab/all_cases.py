from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QTableWidget , QHeaderView , QTableWidgetItem
from storage.excel import load_cases


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

        self.table = QTableWidget(0, 4)
        self.main_layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(['Client/Employee', 'Notes', 'Status', 'Deadline'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_insert()




    def table_insert(self):
        self.table.setRowCount(0)
        for row in load_cases():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position,0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(row[3])))










