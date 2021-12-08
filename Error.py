from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QLabel


# This Class is for Displaying error window
class Wrapper_Error:
    def __init__(self, window, message):
        dia = QDialog(window)
        dia.setWindowTitle('Error !')
        dia.setFixedSize(400, 100)

        icon = QLabel(dia)
        icon.setFixedSize(50, 50)
        pix = QPixmap('images/error.png')
        icon.setPixmap(pix.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        icon.move(50, 25)

        label = QLabel(dia)
        label.setText(message)
        label.setFixedSize(300, 90)
        label.setWordWrap(True)
        label.move(110, 5)
        font = label.font()
        font.setBold(True)
        font.setPointSize(11)
        font.setFamily('Helvetica')
        label.setFont(font)

        dia.show()
