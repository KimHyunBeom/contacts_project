from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget
)
from .model import ContactsModel

class Window(QMainWindow):
    """메인 윈도우"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("주소록 프로그램")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """메인 윈도우 GUI 설정"""
        #  테이블 뷰 위젯 생성
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        #  버튼 생성
        self.addButten = QPushButton("추가...")
        self.deleteButten = QPushButton("삭제")
        self.clearAllButten = QPushButton("목록 초기화")
        #  레이아웃 GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButten)
        layout.addWidget(self.deleteButten)
        layout.addStretch()
        layout.addWidget(self.clearAllButten)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)