import sys

from PySide2.QtWidgets import QApplication

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

		self.note_handler = NoteHandler(self.main_ui.window.timeline_area)

	def forward_note(self):
		self.note_handler.create_note(self.note_editor)
		self.note_editor.dialog.hide()


if __name__ == "__main__":

	app = QApplication(sys.argv)
	whatever = MainHandler()
	sys.exit(app.exec_())
