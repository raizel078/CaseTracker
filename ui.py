from PySide6.QtWidgets import QWidget , QLabel , QVBoxLayout, QHBoxLayout, QTabWidget
from PySide6.QtCore import Qt
from tab.all_cases import all_case
from tab.add_cases import add_case
#code for the ui will go here,
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Case follow up Tracker')  # this will be the window title etc.
        self.setFixedSize(800, 500)
        self.main_layout = QVBoxLayout() #setting up the main layout.
        self.setLayout(self.main_layout)

        # now setting all case add cases and stats button these are the tabs.
        self.tab = QTabWidget()
        self.main_layout.addWidget(self.tab)
        self.all_tab = all_case()
        self.add_tab = add_case()
        self.tab.addTab(self.all_tab, 'All Cases')
        self.tab.addTab(self.add_tab,'Add Case')
        self.add_tab.case_signal.connect(self.all_tab.table_insert)
        self.tab.setStyleSheet((f"""
            QTabBar::tab {{ width: {800 // 2}px; }}
            QTabBar::tab:selected {{ border: 2px solid white; }}
        """))
        self.tab.tabBar().setUsesScrollButtons(False)

















