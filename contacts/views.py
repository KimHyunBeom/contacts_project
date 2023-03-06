from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
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
        self.addButten.clicked.connect(self.openAddDialog)          # .clicked() 버튼의 신호를 새로 생성된 슬롯에 연결함 이렇게 하면 버튼을 클릭하면 추가 대화상자가 자동으로 호출됨(.openAddDialog)
        self.deleteButten = QPushButton("삭제")
        self.deleteButten.clicked.connect(self.deleteContact)       # 삭제 버튼의 신호를 슬롯에 연결함
        self.clearAllButten = QPushButton("목록 초기화")
        self.clearAllButten.clicked.connect(self.clearContacts)     # 목록 초기화 버튼을 clearContacts 메소드와 연결함
        #  레이아웃 GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButten)
        layout.addWidget(self.deleteButten)
        layout.addStretch()
        layout.addWidget(self.clearAllButten)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddDialog(self):   # 슬롯을 정의함
        """주소록 추가 대화상자를 열음"""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:               # 대화가 수락되었는지 확인하는 조건문을 정의함
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteContact(self):
        """선택한 주소록을 데이터베이스에서 삭제함"""
        row = self.table.currentIndex().row() # 현재 선택된 행의 인덱스를 가져옴
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "경고!",
            "선택한 주소를 제거하시겠습니까?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)   # 메시지 박스로부터 사용자가 수락을 할 경우 해당 행을 삭제함

    def clearContacts(self):
        """데이터베이스에서 모든 주소를 제거함"""
        messageBox = QMessageBox.warning(
            self,
            "경고!",
            "모든 주소를 제거 하시겠습니까?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clearContacts()

class AddDialog(QDialog):
    """주소록 추가 대화상자"""
    def __init__(self, parent=None):
        """생성자"""
        super().__init__(parent=parent)
        self.setWindowTitle("주소 추가")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None    # 이거도 데이터 리셋인?가??? (+사용자가 제공하는 데이터 보유하는데 사용함)

        self.setupUI()

    def setupUI(self):
        """추가 대화상자 GUI 설정"""
        # 데이터 필드 라인 편집기 생성
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        # 데이터 필드 레이아웃
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Job:", self.jobField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)
        # 대화상자에 버튼 추가 및 연결
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """대화상자 수락 시 동작"""
        self.data = [] # 사용자의 입력데이터 저장함
        for field in (self.nameField, self.jobField, self.emailField):      # 대화 상자에서 다음 세 줄 편집 및 필드를 반복하는 루프를 정의함
            if not field.text():
                QMessageBox.critical(
                    self,
                    "경고!",
                    f"{field.objectName()} 항목의 내용이 입력되지 않았습니다.",   # 무엇무엇의 내용을 기입해야 합니다! 라는 뜻 대충 실행시켜보고 다시 수정할 것(수정완료)
                )
                self.data = None  # .data 리셋
                return

            self.data.append(field.text())                                  # 각 필드에 사용자 입력을 추가함
        if not self.data:
            return

        super().accept()                                                    # 수퍼클래스 슬롯 호출하여 사용자가 OK를 클릭한 뒤 대화상자를 닫는 표준 동작을 제공함
