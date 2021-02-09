import sys

from PySide2.QtGui import (QFont)
from PySide2.QtWidgets import QMainWindow, QApplication, QDialog

from control.note_handler import NoteHandler

import uis.ui_functions
from uis.ui_main import UIMainWindow
from uis.ui_note_editor import UINoteEditor


class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = UIMainWindow()
		self.ui.setup_ui(self)

		create_note_dialog = QDialog()
		self.ui_create_note = UINoteEditor()
		self.ui_create_note.setup_ui(create_note_dialog)
		self.ui_create_note.btn_create.clicked.connect(self.forward_note)

		self.ui.btn_toggle_menu.clicked.connect(lambda: uis.ui_functions.UIFunctions.toggle_menu(self, 50, 250, True))
		self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
		self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
		self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

		self.ui.btn_add_note.clicked.connect(self.ui_create_note.show_updated)
		self.show()

	def forward_note(self):
		note_handler.create_note(self.ui_create_note)
		note_handler.display_notes(window.ui.page_1, window.ui.verticalLayout_7)
		self.ui_create_note.dialog.hide()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	segoe_font = QFont("Segoe UI Light", 12)
	app.setFont(segoe_font)

	window = MainWindow()

	note_handler = NoteHandler()
	note_handler.display_notes(window.ui.page_1, window.ui.verticalLayout_7)

	sys.exit(app.exec_())

