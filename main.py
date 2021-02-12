import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFont

from control.note_handler import NoteHandler
from uis.ui_main import UIMainWindow
from uis.ui_note_editor import UINoteEditor


class MainHandler:
	def __init__(self):
		self.main_ui = UIMainWindow()
		self.note_editor = UINoteEditor()

		self.main_ui.window.create_note_btn.clicked.connect(self.note_editor.show_updated)
		self.note_editor.dialog.create_btn.clicked.connect(self.forward_note)
		self.main_ui.window.show()

		self.note_handler = NoteHandler(self.main_ui.window.note_timeline_frame)
		self.note_handler.display_notes()

	def forward_note(self):
		self.note_handler.create_note(self.note_editor)
		self.note_handler.display_notes(self.main_ui.window.note_timeline_frame)
		self.note_editor.dialog.hide()


if __name__ == "__main__":

	from PySide2.QtCore import QDate
	arr = [QDate(2000, 5, 1), QDate(2000, 2, 1), QDate(2000, 7, 1), QDate(2000, 3, 1)]
	print(arr)
	arr.sort()
	print(arr)
	app = QApplication(sys.argv)
	app.setFont(QFont("Segoe UI light", 12))

	whatever = MainHandler()
	sys.exit(app.exec_())


