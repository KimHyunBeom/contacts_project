from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget

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