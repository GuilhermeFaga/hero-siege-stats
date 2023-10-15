
from PySide6.QtWidgets import QLabel

from PySide6.QtGui import QImage
from PySide6.QtGui import QPixmap


class ImageWidget(QLabel):
    def __init__(self, image_path: str):
        QLabel.__init__(self)

        icon = QImage(image_path)
        self.setPixmap(QPixmap.fromImage(icon))
