import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFileDialog
)


class ImageSliderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.images = []  # To store loaded images
        self.current_image_index = 0

        self.setWindowTitle("Image Slider")
        self.setGeometry(100, 100, 800, 600)

        # Widgets
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.load_button = QPushButton("Load Image")
        self.save_button = QPushButton("Save Image")
        self.save_all_button = QPushButton("Save All Images")

        # Layouts
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.save_all_button)

        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)

        # Connections
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_current_image)
        self.save_all_button.clicked.connect(self.save_all_images)

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        filenames, _ = file_dialog.getOpenFileNames(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")

        for filename in filenames:
            pixmap = QPixmap(filename)
            self.images.append(pixmap)

        if self.images:
            self.show_current_image()

    def show_current_image(self):
        if self.images:
            current_pixmap = self.images[self.current_image_index]
            self.image_label.setPixmap(current_pixmap)

    def show_previous_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_current_image()

    def show_next_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_current_image()

    def save_current_image(self):
        if self.images:
            current_pixmap = self.images[self.current_image_index]
            image_format = "PNG"  # Change this to the desired image format
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix(image_format.lower())
            filename, _ = file_dialog.getSaveFileName(
                self, "Save Image", "", f"{image_format} Files (*.{image_format.lower()})"
            )
            if filename:
                current_pixmap.save(filename, format=image_format)

    def save_all_images(self):
        if self.images:
            image_format = "PNG"  # Change this to the desired image format
            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Images")
            if directory:
                for i, pixmap in enumerate(self.images):
                    filename = f"{directory}/image_{i + 1}.{image_format.lower()}"
                    pixmap.save(filename, format=image_format)


def main():
    app = QApplication(sys.argv)
    window = ImageSliderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
