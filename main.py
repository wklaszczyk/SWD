from gui import Window
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox


def main():
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    try:
        app.exec()
    except Exception:
        QMessageBox.critical(window, "Krytyczny błąd", "Aplikacja napotkała straszny błąd",
                             buttons=QMessageBox.StandardButton.Abort)

if __name__ == '__main__':
    main()