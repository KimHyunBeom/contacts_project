"""이 모듈은 연락처 테이블을 관리하기 위한 모델을 제공함"""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """모델 생성 및 설정"""
        tableModel = QSqlTableModel()       # QSqlTableModel은 단일 테이블에서 데이터베이스 레코드를 읽고 쓰기 위한 고급 인터페이스임
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Job", "Email")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def addContact(self, data):
        """데이터베이스에 새 주소를 추가함"""
        rows = self.model.rowCount()            # 데이터 모델의 현재 행 수 가져옴
        self.model.insertRows(rows, 1)          # 새 행 삽입
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()                  # 변경 사항 데이터베이스에 반환. submitAll()이 실패해도 이미 제출된 변경 사항은 캐시에서 지워지지 않음(https://doc.qt.io/qt-6/qsqltablemodel.html#submitAll)
        self.model.select()                     # 데이터베이스에 모델로 데이터를 다시 로드

    def deleteContact(self, row):
        """데이터베이스에서 주소 제거함"""
        self.model.removeRow(row)               # 선택된 행을 제거함
        self.model.submitAll()
        self.model.select()

    def clearContacts(self):
        """모든 주소 정보를 데이터베이스에서 삭제함."""
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)  # submitAll()이 호출될 때까지 모든 변경 사항이 캐시됨
        self.model.removeRow(0, self.model.rowCount())             # 모델에서 모든 행을 제거함
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)   # .editStrategy 속성을 원래 값으로 재설정(안 그럼 주소 업데이트 불가능)
        self.model.select()

