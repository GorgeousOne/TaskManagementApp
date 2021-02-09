import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFont

import uis.ui_functions
from control.note_handler import NoteHandler
from uis.ui_main import UIMainWindow
from uis.ui_note_editor import UINoteEditor


class MainHandler:
	def __init__(self):
		self.main_ui = UIMainWindow()
		self.note_editor = UINoteEditor()

		self.main_ui.btn_toggle_menu.clicked.connect(lambda: uis.ui_functions.toggle_menu(self.main_ui, 50, 250))
		self.main_ui.btn_page_1.clicked.connect(lambda: self.main_ui.pages_widget.setCurrentWidget(self.main_ui.page_1))
		self.main_ui.btn_page_2.clicked.connect(lambda: self.main_ui.pages_widget.setCurrentWidget(self.main_ui.page_2))
		self.main_ui.btn_page_3.clicked.connect(lambda: self.main_ui.pages_widget.setCurrentWidget(self.main_ui.page_3))
		self.main_ui.btn_add_note.clicked.connect(self.note_editor.show_updated)

		self.note_editor.btn_create.clicked.connect(self.forward_note)
		self.main_ui.show()

		self.note_handler = NoteHandler()
		self.note_handler.display_notes(self.main_ui.page_1, self.main_ui.verticalLayout_7)

	def forward_note(self):
		self.note_handler.create_note(self.note_editor)
		self.note_handler.display_notes(self.main_ui.page_1, self.main_ui.verticalLayout_7)
		self.note_editor.dialog.hide()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	app.setFont(QFont("Segoe UI light", 12))

	whatever = MainHandler()
	sys.exit(app.exec_())

