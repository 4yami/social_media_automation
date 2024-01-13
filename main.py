import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QTextEdit, QHBoxLayout, QFrame, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Social Media Automation")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setAlignment(Qt.Alignment.AlignLeft)

        # Left frame for input
        left_frame = QFrame()
        left_frame.setMaximumWidth(300)
        main_layout.addWidget(left_frame)

        left_layout = QVBoxLayout(left_frame)
        left_layout.setAlignment(Qt.Alignment.AlignTop | Qt.Alignment.AlignLeft)

        # Create labels, text inputs, buttons, and list for the left layout
        self.title_label = self.create_label(left_layout, 'FACEBOOK')
        self.email_label = self.create_label(left_layout, 'Email:')
        self.email_input = self.create_text_input(left_layout)
        self.password_label = self.create_label(left_layout, 'Password:')
        self.password_input = self.create_text_input(left_layout, is_password=True)
        self.groups_label = self.create_label(left_layout, 'Groups URL:')
        self.groups_input = self.create_text_input(left_layout)
        self.groups_button = self.create_button(left_layout, 'Add URL', self.add_link)
        self.groups_list = self.create_list(left_layout)

        # Edit and Remove buttons layout
        edit_remove_layout = QHBoxLayout()
        left_layout.addLayout(edit_remove_layout)
        edit_remove_layout.setAlignment(Qt.Alignment.AlignLeft)

        self.groups_link_edit_button = self.create_button(edit_remove_layout, 'Edit Link', self.edit_link)
        self.groups_link_remove_button = self.create_button(edit_remove_layout, 'Remove Link', self.remove_link)

        # Post Text section
        self.post_text_label = self.create_label(left_layout, 'Post Text:')
        self.post_text_text_edit = self.create_text_edit(left_layout)
        
        # Right frame
        right_frame = QFrame()
        main_layout.addWidget(right_frame)
        
        right_layout = QVBoxLayout(right_frame)
        right_layout.setAlignment(Qt.Alignment.AlignCenter)
        
        # Right layout image and indicator
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.image_label)
        self.indicator_label = QLabel()
        self.indicator_label.setMinimumHeight(10)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.indicator_label.setSizePolicy(size_policy)
        right_layout.addWidget(self.indicator_label)  # Use right_layout here

        
        # Right layout button
        self.select_image_button = self.create_button(right_layout, 'Select Image', self.select_image)
        self.remove_image_button = self.create_button(right_layout, 'Remove Image', self.remove_image)
        self.next_button = self.create_button(right_layout, 'Next', self.show_next)
        self.previous_button = self.create_button(right_layout, 'Previous', self.show_previous)
        
        self.current_index = 0
        self.picture_paths = []
        
        # Initialize viewer state
        self.reset_viewer_state()
        
    # UI functions
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
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        return list_widget
    
    def create_text_edit(self, layout):
        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        return text_edit

    # Functions
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
                
    # ///// new function no use yet
    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.picture_paths.extend(selected_files)
            self.show_picture()

    def remove_image(self):
        if self.picture_paths:
            self.picture_paths.pop(self.current_index)
            if not self.picture_paths:
                self.reset_viewer_state()
            else:
                self.current_index = min(self.current_index, len(self.picture_paths) - 1)
            self.show_picture()

    def show_previous(self):
        if self.picture_paths:
            self.current_index = (self.current_index - 1) % len(self.picture_paths)
            self.show_picture()

    def show_next(self):
        if self.picture_paths:
            self.current_index = (self.current_index + 1) % len(self.picture_paths)
            self.show_picture()

    def show_picture(self):
        if self.picture_paths:
            pixmap = QPixmap(self.picture_paths[self.current_index])
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                aspectMode=Qt.KeepAspectRatio, 
                mode=Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.indicator_label.setText(f"Picture {self.current_index + 1}/{len(self.picture_paths)}")

    
    def reset_viewer_state(self):
        self.current_index = 0
        self.image_label.clear()
        self.indicator_label.clear()

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.show_picture()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
