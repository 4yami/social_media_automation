import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class MyApplication(QMainWindow):
    def __init__(self):
        super(MyApplication, self).__init__()

        self.setWindowTitle("Picture Viewer")
        self.setGeometry(100, 100, 600, 450)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self.central_widget)
        self.layout.addWidget(self.label)

        self.indicator_label = QLabel(self.central_widget)
        self.indicator_label.setMinimumHeight(10)  # Set the minimum height as low as possible
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.indicator_label.setSizePolicy(size_policy)
        self.layout.addWidget(self.indicator_label)

        self.button_select = QPushButton("Select Picture", self.central_widget)
        self.button_select.clicked.connect(self.select_picture)
        self.layout.addWidget(self.button_select)

        self.button_remove = QPushButton("Remove Picture", self.central_widget)
        self.button_remove.clicked.connect(self.remove_picture)
        self.layout.addWidget(self.button_remove)

        self.button_previous = QPushButton("Previous", self.central_widget)
        self.button_previous.clicked.connect(self.show_previous_picture)
        self.layout.addWidget(self.button_previous)

        self.button_next = QPushButton("Next", self.central_widget)
        self.button_next.clicked.connect(self.show_next_picture)
        self.layout.addWidget(self.button_next)

        self.current_index = 0
        self.picture_paths = []


    def select_picture(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.picture_paths.extend(selected_files)
            self.show_picture()

    def remove_picture(self):
        if self.picture_paths:
            self.picture_paths.pop(self.current_index)
            if not self.picture_paths:
                # If there are no pictures left, reset the current_index and clear the label
                self.current_index = 0
                self.label.clear()
                self.indicator_label.clear()
            else:
                # Ensure the current_index is within bounds
                self.current_index = min(self.current_index, len(self.picture_paths) - 1)
            self.show_picture()

    def show_previous_picture(self):
        if self.picture_paths:
            self.current_index = (self.current_index - 1) % len(self.picture_paths)
            self.show_picture()

    def show_next_picture(self):
        if self.picture_paths:
            self.current_index = (self.current_index + 1) % len(self.picture_paths)
            self.show_picture()

    def show_picture(self):
        if self.picture_paths:
            pixmap = QPixmap(self.picture_paths[self.current_index])
            self.label.setPixmap(pixmap.scaled(self.label.size(), aspectMode=Qt.KeepAspectRatio, mode=Qt.SmoothTransformation))
            self.indicator_label.setText(f"Picture {self.current_index + 1}/{len(self.picture_paths)}")

    def resizeEvent(self, event):
        # Override the resize event to handle picture resizing
        super(MyApplication, self).resizeEvent(event)
        self.show_picture()


def main():
    app = QApplication(sys.argv)
    my_app = MyApplication()
    my_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
