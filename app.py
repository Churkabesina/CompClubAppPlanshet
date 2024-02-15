import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QSize, QThread, QObject, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame

from ui import main_window, main_frame, sign_in_by_login_frame, sign_in_by_biometric_frame, background

import api_requests
import utils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = main_window.Ui_MainWindow()
        self.main_window.setupUi(self)
        self.setWindowTitle('UltraCyberArena')
        self.main_window.pushButton.setIcon(QIcon('src/back_icon.png'))
        self.main_window.pushButton.setIconSize(QSize(70, 90))
        self.main_window.pushButton.hide()

        self.main_frame = MainFrame()
        self.main_window.centralwidget.layout().insertWidget(2, self.main_frame)
        # self.main_frame.show()

        self.login_frame = LoginFrame()

        self.biometric_frame = BiometricFrame()
        self.biometric_frame.biometric_frame.pushButton.setIcon(QIcon('src/finger_print_white.png'))
        self.biometric_frame.biometric_frame.pushButton.setIconSize(QSize(350, 350))

        self.main_window.pushButton.clicked.connect(self.back_button_click)
        self.main_frame.main_frame.sign_in_by_login_button.clicked.connect(self.sign_in_by_login_click)
        self.main_frame.main_frame.sign_in_by_biometric_button.clicked.connect(self.sign_in_by_biometric_click)

    # slot войти по логину
    def sign_in_by_login_click(self):
        self.main_window.pushButton.show()
        self.main_frame.hide()
        self.main_window.centralwidget.layout().replaceWidget(self.main_frame, self.login_frame)
        self.login_frame.show()

    # slot войти по биометрии
    def sign_in_by_biometric_click(self):
        self.main_window.pushButton.show()
        self.main_frame.hide()
        self.main_window.centralwidget.layout().replaceWidget(self.main_frame, self.biometric_frame)
        self.biometric_frame.show()

    # slot вернуться назад
    def back_button_click(self):
        current_widget = self.main_window.centralwidget.layout().itemAt(2).widget()
        current_widget.hide()
        self.main_window.pushButton.hide()
        self.main_window.centralwidget.layout().replaceWidget(current_widget, self.main_frame)
        self.main_frame.show()

    # перехват даблкликов на мышке
    def mouseDoubleClickEvent(self, a0):
        if a0.button() == Qt.MouseButton.LeftButton:
            self.biometric_frame.biometric_frame.pushButton.setIcon(QIcon('src/finger_print_green.png'))
        else:
            self.biometric_frame.biometric_frame.pushButton.setIcon(QIcon('src/finger_print_red.png'))

    # перехват нажатия на F11
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()


class MainFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.main_frame = main_frame.Ui_Frame()
        self.main_frame.setupUi(self)


class LoginFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.login_frame = sign_in_by_login_frame.Ui_Frame()
        self.login_frame.setupUi(self)


class BiometricFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.biometric_frame = sign_in_by_biometric_frame.Ui_Frame()
        self.biometric_frame.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())