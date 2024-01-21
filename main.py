import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QTextEdit, QHBoxLayout, QFrame, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import threading
from facebook2 import post_fb
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Social Media Automation")
        self.groups_list_item = []
        self.current_images_index = 0
        self.images_path_list = []
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
        self.email_input = self.create_text_input(left_layout, False)
        self.password_label = self.create_label(left_layout, 'Password:')
        self.password_input = self.create_text_input(left_layout, True)
        self.groups_label = self.create_label(left_layout, 'Groups URL:')
        self.groups_input = self.create_text_input(left_layout, False)
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
        right_layout.addWidget(self.indicator_label)

        
        # Right layout button
        self.select_image_button = self.create_button(right_layout, 'Select Image', self.select_image)
        self.remove_image_button = self.create_button(right_layout, 'Remove Image', self.remove_image)
        self.next_button = self.create_button(right_layout, 'Next', self.show_next)
        self.previous_button = self.create_button(right_layout, 'Previous', self.show_previous)
        self.post_button = self.create_button(right_layout, 'Post', self.on_post_button_click)
          
          
        # Call load_config at the beginning to load the saved configuration
        self.load_config()
          
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
                self.get_groups_list_item()
            except Exception as e:
                print(f"Error: {e}")
                
    def get_groups_list_item(self):
        self.groups_list_item = [self.groups_list.item(i).text() for i in range(self.groups_list.count())]
        return self.groups_list_item
    
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
                self.get_groups_list_item()
            except Exception as e:
                print(f"Error: {e}")
             
                
    # Image function
    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.images_path_list.extend(selected_files)
            self.show_image()

    def remove_image(self):
        if self.images_path_list:
            self.images_path_list.pop(self.current_images_index)
            if not self.images_path_list:
                self.reset_viewer_state()
            else:
                self.current_images_index = min(self.current_images_index, len(self.images_path_list) - 1)
            self.show_image()

    def show_previous(self):
        self.current_images_index = (self.current_images_index - 1) % len(self.images_path_list)
        self.show_image()

    def show_next(self):
        self.current_images_index = (self.current_images_index + 1) % len(self.images_path_list)
        self.show_image()

    def show_image(self):
        if self.images_path_list:
            pixmap = QPixmap(self.images_path_list[self.current_images_index])
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                aspectMode=Qt.KeepAspectRatio, 
                mode=Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            def update_indicator_label():
                self.indicator_label.setText(f"image {self.current_images_index + 1}/{len(self.images_path_list)}")
            update_indicator_label()
            
    def reset_viewer_state(self):
        self.current_images_index = 0
        self.image_label.clear()
        self.indicator_label.clear()

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.show_image()
 
    # save text function
    def save_config(self):
        config_data = {
            'email': self.email_input.text(),
            'password': self.password_input.text(),
            'group': self.get_groups_list_item(),
        }

        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file)

    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config_data = json.load(config_file)
                self.email_input.setText(config_data.get('email', ''))
                self.password_input.setText(config_data.get('password', ''))
                
                # Load group list
                for link in config_data.get('group', []):
                    self.groups_list.addItem(link)
        except FileNotFoundError:
            pass  # File not found, it's okay
 
    # posting function
    def on_post_button_click(self):
        self.save_config()
        """Callback for the 'Start Post' button click."""
        self.email = self.email_input.text()
        self.password = self.password_input.text()
        self.group = self.get_groups_list_item()
        self.post_text = self.post_text_text_edit.toPlainText()
        self.converted_images_path = [path.replace('\\', '\\\\') for path in self.images_path_list]
        # self.save_to_file(self.email, self.password, self.group)

        thread = threading.Thread(target=self.post_to_facebook, args=(self.email, self.password, self.group, self.post_text, self.converted_images_path))
        thread.start()

    def post_to_facebook(self, email, password, group, post_text, converted_images_path):
        """Posts to Facebook with provided credentials and text."""
        try:
            post_fb(fb_email=email, fb_password=password, fb_group=group, fb_post_text=post_text, fb_files_path=converted_images_path)
        except Exception as e:
            print(f"Error occurred while posting: {e}")
            # Consider using logging for more detailed error handling


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
