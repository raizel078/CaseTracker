from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from tab.all_cases import all_case
from tab.add_cases import add_case


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Case follow up Tracker')
        self.resize(800, 500)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.tab = QTabWidget()
        self.main_layout.addWidget(self.tab)

        self.all_tab = all_case()
        case = add_case()
        self.add_tab = case
        self.tab.addTab(self.all_tab, 'All Cases')
        self.tab.addTab(self.add_tab, 'Add Case')
        self.add_tab.case_signal.connect(self.all_tab.table_insert)

        self.tab.tabBar().setExpanding(True)
        self.tab.tabBar().setDocumentMode(True)
        self.tab.setStyleSheet("""
            QTabBar::tab { 
                border: 1px solid #C4C4C3;
                min-width: 50px;
            }
            QTabBar::tab:selected { border: 2px solid white; }
        """)