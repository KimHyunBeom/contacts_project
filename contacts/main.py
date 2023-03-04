import sys

from PyQt5.QtWidgets import QApplication

from .views import Window

def main():
    """주소록 프로그램  메인 함수"""
    # 앱을 생성함
    app = QApplication(sys.argv)
    # main window 호출
    win = Window()
    win.show()
    # 이벤트 루프 발생
    sys.exit(app.exec_())