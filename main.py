import sys
from datetime import datetime

from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import QMainWindow, QApplication, QErrorMessage

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
		self.note_dialog.btn_create.clicked.connect(self.forward_note)
		self.note_dialog.hide()

		self.ui.btn_toggle_menu.clicked.connect(lambda: uis.ui_functions.UIFunctions.toggle_menu(self, 50, 250, True))
		self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
		self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
		self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

		self.ui.btn_add_note.clicked.connect(self.note_dialog.show_updated)
		self.show()

	def forward_note(self):
		note_handler.create_note(self.note_dialog)
		note_handler.display_notes(window.ui.page_1, window.ui.verticalLayout_7)
		self.note_dialog.hide()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	segoe_font = QFont("Segoe UI Light", 12)
	app.setFont(segoe_font)

	window = MainWindow()

	note_handler = NoteHandler()
	# note_handler.create_note(Note("I am pickle rick!", datetime.now()))
	note_handler.display_notes(window.ui.page_1, window.ui.verticalLayout_7)

	sys.exit(app.exec_())

