import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog
from cryptography.fernet import Fernet

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()

        self.key = None
        self.cipher_suite = None
        self.file_path = "encrypted_password.txt"

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.encrypt_button = QPushButton("Encrypt & Save")
        self.encrypt_button.clicked.connect(self.encrypt_and_save_password)
        layout.addWidget(self.encrypt_button)

        self.load_button = QPushButton("Load & Decrypt")
        self.load_button.clicked.connect(self.load_and_decrypt_password)
        layout.addWidget(self.load_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle("Password Manager")

    def encrypt_and_save_password(self):
        password = self.password_input.text().encode()
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        encrypted_password = self.cipher_suite.encrypt(password)

        with open(self.file_path, "wb") as file:
            file.write(b"KEY:" + self.key + b"\n")
            file.write(b"PASSWORD:" + encrypted_password)

        self.result_label.setText("Password encrypted and saved.")

    def load_and_decrypt_password(self):
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Select Encrypted File")
        file_dialog.setNameFilter("Text files (*.txt)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                with open(file_path, "rb") as file:
                    lines = file.readlines()

                key = None
                encrypted_password = None
                for line in lines:
                    if line.startswith(b"KEY:"):
                        key = line.replace(b"KEY:", b"").strip()
                    elif line.startswith(b"PASSWORD:"):
                        encrypted_password = line.replace(b"PASSWORD:", b"")

                if key and encrypted_password:
                    self.key = key
                    self.cipher_suite = Fernet(self.key)
                    try:
                        decrypted_password = self.cipher_suite.decrypt(encrypted_password)
                        self.result_label.setText(f"Decrypted: {decrypted_password.decode()}")
                    except Exception as e:
                        self.show_error_message("Error", "Invalid password or encryption key.")
                else:
                    self.show_error_message("Error", "Invalid file format.")
            else:
                self.show_error_message("Error", "No file selected.")
                
    def show_error_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec()

def run_app():
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
