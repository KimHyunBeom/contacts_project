import sys

from PyQt5.QtWidgets import QApplication

from .database import createConnection
from .views import Window

def main():
    """주소록 프로그램  메인 함수"""
    # 앱을 생성함
    app = QApplication(sys.argv)
    # 창 만들기 전에 DB 연결
    if not createConnection("contacts.sqlite"):
        sys.exit(1)  # 애플리케이션이 연결을 생성할 수 없는 경우 sys.exit(1) 은 그래픽 요소 생성 않고 앱 닫은 후 오류 발생을 표시함
    # main window 호출
    win = Window()
    win.show()
    # 이벤트 루프 발생
    sys.exit(app.exec_())