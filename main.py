import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QTextEdit, QHBoxLayout, QFrame
from PySide6.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Social Media Automation")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        parent_h_layout = QHBoxLayout()
        parent_h_layout.setAlignment(Qt.Alignment.AlignLeft)
        central_widget.setLayout(parent_h_layout)
        
        frame = QFrame()
        frame.setMaximumWidth(300)  # Set the maximum width of the frame (and v_layout)
        parent_h_layout.addWidget(frame)
        v_layout = QVBoxLayout(frame)
        v_layout.setAlignment(Qt.Alignment.AlignTop | Qt.Alignment.AlignLeft)  # Align to top-left
        
        
        self.title_label = self.create_label(v_layout, 'FACEBOOK')
        self.email_label = self.create_label(v_layout, 'Email:')
        self.email_input = self.create_text_input(v_layout)
        self.password_label = self.create_label(v_layout, 'Password:')
        self.password_input = self.create_text_input(v_layout, True)
        self.groups_label = self.create_label(v_layout, 'Groups URL:')
        self.groups_input = self.create_text_input(v_layout)
        self.groups_button = self.create_button(v_layout, 'Add URL', self.add_link)
        self.groups_list = self.create_list(v_layout)
        
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout.setAlignment(Qt.Alignment.AlignLeft)
        
        self.groups_link_edit_button = self.create_button(h_layout, 'Edit Link', self.edit_link)
        self.groups_link_remove_button = self.create_button(h_layout, 'Remove Link', self.remove_link)
        
        self.post_text_label = self.create_label(v_layout, 'Post Text:')
        self.post_text_text_edit = self.create_text_edit(v_layout)
        
        v2_layout = QVBoxLayout()
        
        
    # UI function
    def create_label(self, layout, text):
        label = QLabel(text)
        layout.addWidget(label)
        return label
        
    def create_text_input(self, layout, is_password=False):
        text_input = QLineEdit()
        if is_password:
            text_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(text_input)
        return text_input

    def create_button(self, layout, text, button_function):
        button = QPushButton(text)
        button.clicked.connect(button_function)
        layout.addWidget(button)
        return button

    def create_list(self, layout):
        list = QListWidget()
        layout.addWidget(list)
        return list
    
    def create_text_edit(self, layout):
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        return text_edit

    
    # function
    def add_link(self):
        new_link = self.groups_input.text()
        
        if new_link:
            try:
                self.groups_list.addItem(new_link)
                self.groups_input.clear()
            except Exception as e:
                print(f"Error: {e}")
    
    def edit_link(self):
        selected_item = self.groups_list.currentItem()
        
        if selected_item:
            try:
                current_link = selected_item.text()
                self.groups_input.setText(current_link)
                self.groups_list.takeItem(self.groups_list.row(selected_item))
            except Exception as e:
                print(f"Error: {e}")
    
    def remove_link(self):
        selected_item = self.groups_list.currentItem()
        
        if selected_item:
            try:
                self.groups_list.takeItem(self.groups_list.row(selected_item))
            except Exception as e:
                print(f"Error: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
