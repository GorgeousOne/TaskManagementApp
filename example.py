import sys
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QPushButton, QDialog

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(.8)
        self.setStyleSheet("QMainWindow {background: 'black'}")

        self.dialog = QDialog()
        self.dialog.setModal(True)

        self.b = QPushButton(self.dialog)
        self.b.setText("exit")
        self.b.clicked.connect(self.nowclose)

        self.dialog.show()

    def nowclose(self):
        self.dialog.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyWindow()
    myapp.setGeometry(app.desktop().screenGeometry())
    myapp.show()
    sys.exit(app.exec_())
