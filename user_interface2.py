import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox
from facebook2 import post_fb

class FacebookPosterApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_ui()

    def on_post_button_click(self):
        """Callback for the 'Start Post' button click."""
        self.email = self.email_input.text()
        self.password = self.password_input.text()
        self.group = self.group_input.text()
        self.post_text = self.post_text_input.toPlainText()
        self.save_to_file(self.email, self.password, self.group)

        thread = threading.Thread(target=self.post_to_facebook, args=(self.email, self.password, self.group, self.post_text))
        thread.start()

    def post_to_facebook(self, email, password, group, post_text):
        """Posts to Facebook with provided credentials and text."""
        try:
            post_fb(fb_email=email, fb_password=password, fb_group=group, fb_post_text=post_text)
        except Exception as e:
            print(f"Error occurred while posting: {e}")
            # Consider using logging for more detailed error handling

    def setup_ui(self):
        """Sets up the user interface."""
        self.window = QWidget()
        self.window.setWindowTitle("Post on Facebook Group")
        layout = QVBoxLayout(self.window)

        self.email_input = self.create_input_field(layout, "Email:", "scowhp@gmail.com")
        self.password_input = self.create_input_field(layout, "Password:", "fre3flip1ng", is_password=True)
        self.group_input = self.create_input_field(layout, "Group:", "https://www.facebook.com/groups/bobyss")
        
        self.create_label(layout, "Post Text:")
        self.post_text_input = self.create_text_edit(layout, 100)

        self.create_button(layout, "Start Post", self.on_post_button_click)

        self.window.setLayout(layout)
        self.window.show()

        sys.exit(self.app.exec_())

    def create_input_field(self, layout, label_text, default_text, is_password=False):
        """Creates input fields with labels."""
        label = QLabel(label_text)
        layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setText(default_text)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(input_field)
        return input_field

    def create_label(self, layout, text):
        """Creates labels."""
        label = QLabel(text)
        layout.addWidget(label)

    def create_text_edit(self, layout, height):
        """Creates a text edit field."""
        text_edit = QTextEdit()
        text_edit.setFixedHeight(height)
        layout.addWidget(text_edit)
        return text_edit

    def create_button(self, layout, text, on_click_function):
        """Creates a button."""
        button = QPushButton(text)
        button.clicked.connect(on_click_function)
        layout.addWidget(button)
        
    def save_to_file(self, email, password, group):
        try:
            with open('output.txt', 'w') as file:
                file.write(f"Email: {email}\nPassword: {password}\nURL: {group}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")

    def load_previous_text(self):
        try:
            with open('output.txt', 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    self.line_edit1.setText(lines[0].strip().split(': ')[1])
                    self.line_edit2.setText(lines[1].strip().split(': ')[1])
                    self.line_edit3.setText(lines[2].strip().split(': ')[1])
        except FileNotFoundError:
            pass 

if __name__ == "__main__":
    facebook_poster = FacebookPosterApp()
