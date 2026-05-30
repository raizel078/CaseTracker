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
        self.tab.addTab(all_case(), 'All Cases')
        self.tab.addTab(add_case(),'Add Case')
        self.tab.setStyleSheet((f"""
            QTabBar::tab {{ width: {800 // 2}px; }}
            QTabBar::tab:selected {{ border: 2px solid white; }}
        """))
        self.tab.tabBar().setUsesScrollButtons(False)















