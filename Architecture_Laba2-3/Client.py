import sys
import socket
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 600, 300)

        layout = QVBoxLayout()

        self.username_label = QLabel('Username:', self)
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:', self)
        self.password_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        font = QFont()
        font.setPointSize(16)
        self.username_label.setFont(font)
        self.password_label.setFont(font)
        self.username_input.setFont(font)
        self.password_input.setFont(font)
        self.login_button.setFont(font)
        self.register_button.setFont(font)
        self.statusBar().setFont(font)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        self.statusBar().showMessage(self.authenticate(username,password))

    def authenticate(self, username, password):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1', 9999))
                s.sendall(f'login,{username},{password}'.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                return response
            except Exception:
                return "No connection with server"

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        self.statusBar().showMessage(self.create_account(username,password))

    def create_account(self, username, password):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('127.0.0.1', 9999))
                s.sendall(f'register,{username},{password}'.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                return response
            except Exception:
                return "No connection with server"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())