from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QLineEdit, QRadioButton, QButtonGroup, QHBoxLayout
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
import steganos as st

file_path = ""
keys_path = ""

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
        global file_path
        files = event.mimeData().urls()
        if len(files) > 0:
            file_path = files[0].toLocalFile()
            self.setPixmap(QPixmap(file_path))

            if isinstance(self.parent(), MainWindow):
                self.parent().text_label.setText(file_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steganos")
        self.setFixedSize(600, 400)  # Imposta dimensioni fisse per la finestra

        self.jsonField = QLineEdit(self)
        self.jsonField.setGeometry(QtCore.QRect(60, 155, 150, 30))
        self.jsonField.setPlaceholderText("Percorso chiave...")
        self.jsonField.setVisible(False)

        self.jsonButton = QtWidgets.QPushButton(self)
        self.jsonButton.setGeometry(QtCore.QRect(215, 155, 70, 30))
        self.jsonButton.setText("Sfoglia")
        self.jsonButton.clicked.connect(self.select_dictionary)
        self.jsonButton.setVisible(False)

        self.option_combo = QtWidgets.QComboBox(self)
        self.option_combo.setGeometry(QtCore.QRect(60, 60, 220, 30))
        self.option_combo.addItems(["Encode", "Decode"])
        self.option_combo.currentIndexChanged.connect(self.combobox_index_changed)

        self.file_textfield = QLineEdit(self)
        self.file_textfield.setGeometry(QtCore.QRect(60, 100, 220, 30))
        self.file_textfield.setPlaceholderText("Testo da codificare")

        self.decodedtext = QtWidgets.QLabel(self)
        self.decodedtext.setGeometry(QtCore.QRect(60, 140, 160, 30))
        self.decodedtext.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.decodedtext.hide()

        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setGeometry(QtCore.QRect(410, 260, 90, 30))
        self.file_button.setText("Seleziona file")
        self.file_button.clicked.connect(self.select_file)

        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setGeometry(QtCore.QRect(20, 130, 560, 30))
        self.file_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.image_label = ImageView(self)
        self.image_label.setGeometry(QtCore.QRect(350, 20, 400, 200))
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setText("Trascina qui l'immagine")
        self.text_label.setGeometry(QtCore.QRect(350, 220, 200, 30))
        self.text_label.setWordWrap(True)

        self.dizionario_label = QtWidgets.QLabel(self)
        self.dizionario_label.setGeometry(QtCore.QRect(60, 135, 150, 30))
        self.dizionario_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.dizionario_label.setText("Chiave di criptazione:")

        self.radio1 = QRadioButton("Sistema", self)
        self.radio2 = QRadioButton("Generato casualmente", self)
        self.radio1.setChecked(True)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio1)
        self.button_group.addButton(self.radio2)
        self.button_group.buttonClicked.connect(self.radio_clicked)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.radio1)
        # self.hbox.addSpacing(5)
        self.hbox.addWidget(self.radio2)
        self.hbox.setGeometry(QtCore.QRect(60, 148, 220, 30))
        self.hbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.process_button = QtWidgets.QPushButton(self)
        self.process_button.setGeometry(QtCore.QRect(110, 250, 100, 30))
        self.process_button.setText("Processa")
        self.process_button.clicked.connect(self.process_action)

        self.result = QtWidgets.QLabel(self)
        self.result.setGeometry(QtCore.QRect(10, 290, 580, 70))
        self.result.setText("Testo decriptato: ")
        self.result.setVisible(False)
        self.result.setWordWrap(True)

    def radio_clicked(self, button):
        if button == self.radio1:
            self.jsonButton.setVisible(False)
            self.jsonField.setVisible(False)
        elif button == self.radio2:
            if self.radio2.text() == "Importa da file":
                # Devo aggiungere un altro tasto per importare il dizionario
                self.jsonField.setVisible(True)
                self.jsonButton.setVisible(True)
            else:
                # Utilizzo un dizionario generato casualmente
                pass

    def combobox_index_changed(self, index):
        selected_option = self.option_combo.currentText()
        if selected_option == "Decode":
            self.file_textfield.setVisible(False)
            self.decodedtext.setVisible(True)
            self.dizionario_label.setGeometry(QtCore.QRect(60, 93, 150, 30))
            self.hbox.setGeometry(QtCore.QRect(45, 105, 220, 30))
            self.radio2.setText("Importa da file")
            self.radio1.setChecked(True)
            self.result.setVisible(True)
        elif selected_option == "Encode":
            self.jsonField.setVisible(False)
            self.jsonButton.setVisible(False)
            self.decodedtext.setVisible(False)
            self.file_textfield.setVisible(True)
            self.dizionario_label.setVisible(False)
            self.hbox.setGeometry(QtCore.QRect(60, 148, 220, 30))
            self.dizionario_label.setVisible(True)
            self.dizionario_label.setGeometry(QtCore.QRect(60, 135, 150, 30))
            self.radio2.setText("Generato casualmente")
        else:
            raise ValueError("Operazione non permessa")

    def select_file(self):
        global file_path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Seleziona file")
        if file_path:
            self.image_label.setPixmap(QPixmap(file_path))
            self.text_label.setText(file_path)

    def select_dictionary(self):
        global keys_path
        keys_path, _ = QFileDialog.getOpenFileName(self, "Seleziona file", "", "File JSON (*.json)")
        if keys_path:
            self.jsonField.setText(keys_path)

    def process_action(self):
        global file_path
        selected_option = self.option_combo.currentText()
        if selected_option == "Encode":
            # Logica per l'encoding dell'immagine
            if self.radio1.isChecked():
                st.encode(file_path, self.file_textfield.text(), 1)
            else:
                st.encode(file_path, self.file_textfield.text(), 2)
        elif selected_option == "Decode":

            if self.radio1.isChecked():
                try:
                    self.result.setText("Testo decodificato: "+st.decode(file_path))
                except ValueError as e:
                    self.result.setText("Errore: "+e.args[0])
            else:
                self.result.setText("Testo decodificato: "+st.decode(file_path, keys_path))

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
