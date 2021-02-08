import sys
from datetime import datetime

from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import QMainWindow, QApplication

from control.note_handler import NoteHandler
from model.note import Note

import uis.ui_functions
from uis.ui_main import Ui_MainWindow
from uis.ui_note_form import NoteForm

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setup_ui(self)

		self.note_dialog = NoteForm()
		self.note_dialog.hide()

		self.ui.btn_toggle_menu.clicked.connect(lambda: uis.ui_functions.UIFunctions.toggle_menu(self, 50, 250, True))
		self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
		self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
		self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

		self.ui.btn_add_note.clicked.connect(self.open_node_form)
		self.show()

	def open_node_form(self):
		self.note_dialog.show()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	segoe_font = QFont("Segoe UI Light", 12)
	app.setFont(segoe_font)

	window = MainWindow()

	note_handler = NoteHandler()
	#note_handler.add_note(Note("Remember!", datetime.now()))
	note_handler.display_notes(window.ui.page_1, window.ui.verticalLayout_7)

	sys.exit(app.exec_())

