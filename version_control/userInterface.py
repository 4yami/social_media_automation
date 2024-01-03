import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from facebook2 import post_fb

def on_button_click():
    # Function to start the Selenium task when the button is clicked
    thread = threading.Thread(target=post_fb(fbEmail=emailInput.text(), fbPassword=password_input.text(), fbGroup=groupInput.text(), fbPostText=postTextInput.toPlainText()))
    thread.start()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Post on fb group")

layout = QVBoxLayout()

# Email
emailLabel = QLabel("Email:")
layout.addWidget(emailLabel)
emailInput = QLineEdit()
emailInput.setText('scowhp@gmail.com')
layout.addWidget(emailInput)

# Password
passwordLabel = QLabel("Password:")
layout.addWidget(passwordLabel)
password_input = QLineEdit()
password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hides the input text for password
password_input.setText("fre3flip1ng")  # Set default text
layout.addWidget(password_input)

# Group
groupLabel = QLabel("Group:")
layout.addWidget(groupLabel)
groupInput = QLineEdit()
groupInput.setText('https://www.facebook.com/groups/bobyss')
layout.addWidget(groupInput)

# Custom field with 3 lines
postTextLabel = QLabel("Post Text:")
layout.addWidget(postTextLabel)
postTextInput = QTextEdit()
postTextInput.setFixedHeight(100)  # Set the height to accommodate 3 lines
layout.addWidget(postTextInput)

# Button to trigger Selenium task
postButton = QPushButton("Start post")
postButton.clicked.connect(on_button_click)
layout.addWidget(postButton)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
