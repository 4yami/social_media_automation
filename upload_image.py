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
    IMAGE_FORMAT = "PNG"  # Define image format as a class constant

    def __init__(self):
        super().__init__()

        self.images = []  # To store loaded images
        self.current_image_index = 0

        self.setWindowTitle("Image Slider")
        self.setGeometry(100, 100, 800, 600)

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.load_button = QPushButton("Load Image")
        self.save_button = QPushButton("Save Image")
        self.save_all_button = QPushButton("Save All Images")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.save_all_button)

        self.index_label = QLabel(alignment=Qt.AlignCenter)

        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.index_label)
        main_layout.addLayout(button_layout)

    def setup_connections(self):
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_current_image)
        self.save_all_button.clicked.connect(self.save_all_images)

    def load_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        filenames, _ = file_dialog.getOpenFileNames(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if filenames:
            images_loaded = ImageLoader.load_images_from_files(filenames)
            self.images.extend(images_loaded)

            if self.images:
                self.show_current_image()

    def show_current_image(self):
        if self.images:
            current_pixmap = self.images[self.current_image_index]
            self.image_label.setPixmap(
                current_pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
            self.index_label.setText(f"Image {self.current_image_index + 1}/{len(self.images)}")

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
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix(self.IMAGE_FORMAT.lower())
            filename, _ = file_dialog.getSaveFileName(
                self,
                "Save Image",
                "",
                f"{self.IMAGE_FORMAT} Files (*.{self.IMAGE_FORMAT.lower()})"
            )

            if filename:
                current_pixmap.save(filename, format=self.IMAGE_FORMAT)

    def save_all_images(self):
        if self.images:
            directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Images")

            if directory:
                for i, pixmap in enumerate(self.images):
                    filename = f"{directory}/image_{i + 1}.{self.IMAGE_FORMAT.lower()}"
                    pixmap.save(filename, format=self.IMAGE_FORMAT)


class ImageLoader:
    @staticmethod
    def load_images_from_files(filenames):
        images = []
        for filename in filenames:
            pixmap = QPixmap(filename)
            if not pixmap.isNull():
                images.append(pixmap)
            else:
                print(f"Failed to load image: {filename}")
        return images


def main():
    app = QApplication(sys.argv)
    window = ImageSliderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
