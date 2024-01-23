import sys
import logging
import threading
import json
import os

from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QTextEdit, QHBoxLayout, QFrame, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from cryptography.fernet import Fernet

from facebook import post_fb

app_data_directory = os.path.join(os.environ['APPDATA'], 'Social Media Automation')
os.makedirs(app_data_directory, exist_ok=True)
config_file_path = os.path.join(app_data_directory, "config.json")
log_file_path = os.path.join(app_data_directory, 'app.log')

# Configure logging with TimedRotatingFileHandler
log_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)  # Adjust the log level as needed


class MainWindow(QMainWindow):
    """Main window for the Social Media Automation application."""
    
    def __init__(self):
        """Initialize the main window."""
        super(MainWindow, self).__init__()
        self.setWindowTitle("Social Media Automation")
        self.groups_list_item = []
        self.current_images_index = 0
        self.images_path_list = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
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
        self.groups_input.returnPressed.connect(self.add_link) # connect enter to button
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
        """Add a new link to the groups list."""
        new_link = self.groups_input.text()
        
        if new_link:
            try:
                self.groups_list.addItem(new_link)
                self.groups_input.clear()
                self.get_groups_list_item()
            except Exception as e:
                logging.error(f"Error adding link: {e}")
                
    def get_groups_list_item(self):
        """Get the list of group items from the UI."""
        self.groups_list_item = [self.groups_list.item(i).text() for i in range(self.groups_list.count())]
        return self.groups_list_item
    
    def edit_link(self):
        """Edit the selected link in the groups list."""
        selected_item = self.groups_list.currentItem()
        
        if selected_item:
            try:
                current_link = selected_item.text()
                self.groups_input.setText(current_link)
                self.groups_list.takeItem(self.groups_list.row(selected_item))
            except Exception as e:
                logging.error(f"Error editing link: {e}")
    
    def remove_link(self):
        """Remove the selected link from the groups list."""
        selected_item = self.groups_list.currentItem()
        
        if selected_item:
            try:
                self.groups_list.takeItem(self.groups_list.row(selected_item))
                self.get_groups_list_item()
            except Exception as e:
                logging.error(f"Error removing link: {e}")
             
                
    # Image function
    def select_image(self):
        """Open a file dialog to select and add images."""
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        try:
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                self.images_path_list.extend(selected_files)
                self.show_image()
        except Exception as e:
            logging.error(f"Error selecting image: {e}")

    def remove_image(self):
        """Remove the currently displayed image."""
        try:
            if self.images_path_list:
                self.images_path_list.pop(self.current_images_index)
                if not self.images_path_list:
                    self.reset_viewer_state()
                else:
                    self.current_images_index = min(self.current_images_index, len(self.images_path_list) - 1)
                self.show_image()
        except Exception as e:
            logging.error(f"Error removing image: {e}")

    def show_previous(self):
        """Show the previous image in the list."""
        self.current_images_index = (self.current_images_index - 1) % len(self.images_path_list)
        self.show_image()

    def show_next(self):
        """Show the next image in the list."""
        self.current_images_index = (self.current_images_index + 1) % len(self.images_path_list)
        self.show_image()

    def show_image(self):
        """Display the currently selected image."""
        try:
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
        except Exception as e:
            logging.error(f"Error showing image: {e}")
            
    def reset_viewer_state(self):
        """Reset the state of the image viewer."""
        self.current_images_index = 0
        self.image_label.clear()
        self.indicator_label.clear()

    def resizeEvent(self, event):
        """Handle the window resize event."""
        super(MainWindow, self).resizeEvent(event)
        self.show_image()
 
    # save text function
    def save_config(self):
        """Save the current configuration to a JSON file."""
        config_data = {
            'email': self.email_input.text(),
            'password': self.encrypt_password(self.password_input.text()).decode(),
            'group': self.get_groups_list_item(),
        }

        try:
            with open(config_file_path, 'w') as config_file:
                json.dump(config_data, config_file, indent=2)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")

    def load_config(self):
        """Load the configuration from a JSON file."""
        try:
            # Clean up old log files
            self.cleanup_old_logs()
            
            with open(config_file_path, 'r') as config_file:
                config_data = json.load(config_file)

                # Update UI elements with loaded configuration
                self.email_input.setText(config_data.get('email', ''))
                encrypted_password = config_data.get('password', '')
                self.password_input.setText(self.decrypt_password(encrypted_password))

                # Load group list
                for link in config_data.get('group', []):
                    self.groups_list.addItem(link)
        except FileNotFoundError:
            logging.warning("Configuration file not found.")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in configuration file: {e}")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
 
    def cleanup_old_logs(self):
        """Remove log files older than 7 days."""
        try:
            # Iterate over files in the app_data_directory
            for file_name in os.listdir(app_data_directory):
                # Check if the file is a compressed log file (ends with '.gz' and starts with 'app.log.20')
                if file_name.startswith('app.log.20') and file_name.endswith('.gz'):
                    # Extract the date part from the file name and convert it to a datetime object
                    log_date_str = file_name.split('.')[-2]
                    log_date = datetime.strptime(log_date_str, "%Y-%m-%d")

                    # Check if the log file is older than 7 days
                    if datetime.now() - log_date > timedelta(days=7):
                        # Remove the log file
                        os.remove(os.path.join(app_data_directory, file_name))
        except Exception as e:
            # Log an error message if an exception occurs during log cleanup
            logging.error(f"Error cleaning up old logs: {e}")

    
    def encrypt_password(self, password):
        """Encrypt the given password using Fernet."""
        key = b'aWe0iHTtueNIZY3VJuJwozExOOXCqCd-tUJAUK0KaWI='  
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        """Decrypt the encrypted password using Fernet."""
        key = b'aWe0iHTtueNIZY3VJuJwozExOOXCqCd-tUJAUK0KaWI='
        cipher_suite = Fernet(key)
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password
 
    # posting function
    def on_post_button_click(self):
        """Handle the click event of the 'Post' button."""
        try:
            self.save_config()
            self.email = self.email_input.text()
            self.password = self.password_input.text()
            self.group = self.get_groups_list_item()
            self.post_text = self.post_text_text_edit.toPlainText()
            self.converted_images_path_list = [path.replace('\\', '\\\\') for path in self.images_path_list]
            thread = threading.Thread(target=self.post_to_facebook, args=(self.email, self.password, self.group, self.post_text, self.converted_images_path_list))
            thread.start()
        except Exception as e:
            logging.error(f"Error preparing post: {e}")

    def post_to_facebook(self, email, password, group, post_text, converted_images_path):
        """Post content to Facebook using the provided credentials and data."""
        try:
            post_fb(fb_email=email, fb_password=password, fb_group=group, fb_post_text=post_text, fb_files_path=converted_images_path)
        except Exception as e:
            logging.error(f"Error occurred while posting: {e}")


def main():
    """Entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error in main: {e}")
