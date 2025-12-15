import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt


class GameMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Меню игры")
        self.bg_path = "./ui/background.png"
        self.showFullScreen()
        self.set_background()

        self.label = QLabel("Cowboy-Shootout")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 120px;
                font-weight: bold;
                color: black;
                background: rgba(255,255,255,150);
                padding: 20px;
                border-radius: 20px;
            }
        """)

        self.play_btn = QPushButton("Играть")
        self.settings_btn = QPushButton("Настройки")
        self.exit_btn = QPushButton("Выход")

        self.buttons = (self.play_btn, self.settings_btn, self.exit_btn)

        for b in self.buttons:
            b.setMinimumHeight(100)
            b.setStyleSheet("""
                QPushButton {
                    font-size: 48px;
                    color: white;
                    background: rgba(0,0,0,150);
                    border-radius: 20px;
                    width: 600px
                }
                QPushButton:hover {
                    background: rgba(0,0,0,200);
                }
            """)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(self.play_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

        self.exit_btn.clicked.connect(self.close)
        self.play_btn.clicked.connect(lambda: print("Старт игры"))
        self.settings_btn.clicked.connect(lambda: print("Открыть настройки"))

    def set_background(self):
        pixmap = QPixmap(self.bg_path).scaled(  
            self.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio
        )
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background()
        return super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameMenu()
    window.show()
    sys.exit(app.exec())
