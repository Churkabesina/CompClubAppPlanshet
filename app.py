import sys
import os

from PyQt6 import QtCore
from PyQt6.QtCore import QSize, QThread, QObject, pyqtSignal, pyqtSlot, QTimer, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton

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
        self.login_frame.login_frame.enter_pushbutton.clicked.connect(self.check_data_by_login)

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
        self.login_frame.login_frame.enter_pushbutton.setText('ВОЙТИ')
        self.login_frame.login_frame.lineEdit_login.setEnabled(True)
        self.login_frame.login_frame.lineEdit_password.setEnabled(True)
        self.login_frame.login_frame.enter_pushbutton.setEnabled(True)
        self.login_frame.login_frame.lineEdit_login.setText('')
        self.login_frame.login_frame.lineEdit_password.setText('')
        
        self.main_window.pushButton.setEnabled(True)
        
        current_widget = self.main_window.centralwidget.layout().itemAt(2).widget()
        current_widget.hide()
        
        self.main_window.pushButton.hide()
        self.main_window.centralwidget.layout().replaceWidget(current_widget, self.main_frame)
        self.main_frame.show()

    # перехват даблкликов на мышке
    # def mouseDoubleClickEvent(self, a0):
    #     if a0.button() == Qt.MouseButton.LeftButton:
    #         self.biometric_frame.biometric_frame.pushButton.setIcon(QIcon('src/finger_print_green.png'))
    #     else:
    #         self.biometric_frame.biometric_frame.pushButton.setIcon(QIcon('src/finger_print_red.png'))

    # перехват нажатия на F11
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
    
    def check_data_by_login(self):
        try:
            login = self.login_frame.login_frame.lineEdit_login.text()
            password = self.login_frame.login_frame.lineEdit_password.text()
            api_response = API.check_data_login(login=login, password=password)
            if api_response[0]:
                os.system(f'{SETTINGS["path_to_bat"]}')
                self.lock_login_interface(api_response[1])
            else:
                self.lock_login_interface(api_response[1])
        except Exception as e:
            utils.write_error_log(e)
            exit()

    def lock_login_interface(self, text_for_button: str):
        self.login_frame.login_frame.enter_pushbutton.setText(text_for_button)
        self.login_frame.login_frame.enter_pushbutton.setEnabled(False)
        self.login_frame.login_frame.lineEdit_login.setEnabled(False)
        self.login_frame.login_frame.lineEdit_password.setEnabled(False)
        self.main_window.pushButton.setEnabled(False)
        QTimer.singleShot(2000, self.back_button_click)

    def check_data_by_biometric(self):
        pass


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
    try:
        SETTINGS = utils.load_settings_app()
        IP = f'{SETTINGS["ip"]}:{SETTINGS["port"]}'
        API = api_requests.CompClubRequests(IP, limit_balance=float(SETTINGS["limit_balance"]))
    except Exception as e:
        utils.write_error_log(e)
        utils.execute_error_msg()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())