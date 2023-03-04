from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    """주소록 테이블 데이터베이스 생성"""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(    # 쿼리문 내 의도에 맞게 수정 필요함!
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            job VARCHAR(50),
            email VARCHAR(40) NOT NULL
        )
        """
    )
def createConnection(databaseName):
    """DB connection 생성"""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.Warning(
            None,   # 본래는 self가 들어가는 자리인데 매개 변수가 없어서 None으로 표시한?듯
            "주소록 프로그램",
            f"데이터베이스 오류: {connection.lastError().text()}",  # 맨 앞에 f 는 도대체 정체를 모르겠음;;
        )
        return False
    _createContactsTable()
    return True