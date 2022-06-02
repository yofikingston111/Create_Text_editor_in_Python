import sys

from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QTextEdit, QLabel, QShortcut, QFileDialog, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5 import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None

        """config sortcut"""
        #open new file shortcut
        self.open_new_file_shortcut = QShortcut(QKeySequence('Ctrl+O'), self)
        self.open_new_file_shortcut.activated.connect(self.open_new_file)

        #save current file shortcut
        self.save_current_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.save_current_file_shortcut.activated.connect(self. save_current_file)

        """Configure Window for App"""
        vbox = QVBoxLayout()
        window_title_text = 'Untitled File'
        self.title = QLabel(window_title_text)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.Qt.AlignCenter)
        vbox.addWidget(self.title)
        self.setLayout(vbox)

        #text editor area
        self.scrollable_text_area = QTextEdit()
        vbox.addWidget(self.scrollable_text_area)

    #function to open new file
    def open_new_file(self):
        self.file_path, filter_type = QFileDialog.getOpenFileName(self, "Open New File", "All Files(*)")
        if self.file_path:
            with open(self.file_path, 'r') as f:
                file_content = f.read()
                self.title.setText(self.file_path)
                self.scrollable_text_area.setText(file_content)
        else:
            self.invalid_path_alert_message()

    #function to save current file
    def save_current_file(self):
        if not self.file_path:
            new_file_path, filter_type = QFileDialog.getOpenFileNames(self, "Save this file as..", "All Files(*)")
            if new_file_path:
                self.file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False
            file_contents = self.scrollable_text_area.toPlainText()
            with open(self.file_path, 'w') as f:
                f.write(file_contents)
            self.title.setText(self.file_path)

    #function to handle clossed application warning
    def closeEvent(self, event):
        messageBox = QMessageBox
        title = "Exit Application"
        message = """ "WARNING !!\n\nif you quit without saving, any changes made to the file
                will be lost.\n\nsave file before quitting?"""
        reply = messageBox.question(self, title, message, messageBox.Yes | messageBox.No | messageBox.Cancel, messageBox.Cancel)
        if reply == messageBox.Yes:
            return_value = self.save_current_file()
            if return_value == False:
                event.ignore()
        elif reply == messageBox.No:
            event.accept()
        else:
            event.ignore()

    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid File,Please select a valid file")
        messageBox.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())