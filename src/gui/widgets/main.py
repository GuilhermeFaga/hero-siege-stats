from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel


class MainView(QWidget):
    def __init__(self, text: str):
        QWidget.__init__(self)

        self.setLayout(QVBoxLayout())
        self.label = QLabel(text)
        self.layout().addWidget(self.label)

    def update(self, text):
        self.label.setText(text)


class MainWidget(QWidget):
    def __init__(self, engine):
        QWidget.__init__(self)

        self.engine = engine

        self.setLayout(QVBoxLayout())
        self.view = MainView("No events yet")
        self.layout().addWidget(self.view)

        self.refresh()

        timer = QTimer(self)
        timer.timeout.connect(self.refresh)
        timer.start(500)

    def refresh(self):
        t = self.engine.get_stats()
        self.view.update(str(t))
