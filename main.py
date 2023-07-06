from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent

class ImageView(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPixmap(QPixmap("placeholder.jpg"))
        self.setScaledContents(True)
        self.setFixedSize(200,200)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = event.mimeData().urls()
        if len(files) > 0:
            file_path = files[0].toLocalFile()
            self.setPixmap(QPixmap(file_path))

            if isinstance(self.parent(), MainWindow):
                self.parent().file_textfield.setText(file_path)
                self.parent().text_label.setText(file_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encode/Decode")
        self.setFixedSize(600, 400)  # Imposta dimensioni fisse per la finestra

        self.option_combo = QtWidgets.QComboBox(self)
        self.option_combo.setGeometry(QtCore.QRect(60, 60, 220, 30))
        self.option_combo.addItems(["Encode", "Decode"])

        self.file_textfield = QLineEdit(self)
        self.file_textfield.setGeometry(QtCore.QRect(60, 100, 220, 30))
        self.file_textfield.setPlaceholderText("Testo da codificare")

        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setGeometry(QtCore.QRect(410, 250, 90, 30))
        self.file_button.setText("Seleziona file")
        self.file_button.clicked.connect(self.select_file)

        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setGeometry(QtCore.QRect(20, 130, 560, 30))
        self.file_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.image_label = ImageView(self)
        self.image_label.setGeometry(QtCore.QRect(350, 20, 400, 200))
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setText("Trascina qui l'immagine")
        self.text_label.setGeometry(QtCore.QRect(350, 180, 200, 110))
        self.text_label.setWordWrap(True)

        self.process_button = QtWidgets.QPushButton(self)
        self.process_button.setGeometry(QtCore.QRect(110, 250, 100, 30))
        self.process_button.setText("Processa")
        self.process_button.clicked.connect(self.process_action)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona file")
        if file_path:
            self.image_label.setPixmap(QPixmap(file_path))
            self.text_label.setText(file_path)

    def process_action(self):
        selected_option = self.option_combo.currentText()
        if selected_option == "Encode":
            # Logica per l'encoding dell'immagine
            pass
        elif selected_option == "Decode":
            # Logica per il decoding dell'immagine
            pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
