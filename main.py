import sys

from PySide2.QtWidgets import QApplication

from control.note_handler import NoteHandler
from uis.ui_main import UIMainWindow
from uis.ui_note_editor import UINoteEditor


class MainHandler:
	def __init__(self):
		self.main_ui = UIMainWindow()
		self.note_creator = UINoteEditor()
		self.note_handler = NoteHandler(self.main_ui)

		self.main_ui.window.create_note_btn.clicked.connect(self.note_creator.show_updated)
		self.note_creator.dialog.create_btn.clicked.connect(self.forward_note)
		self.main_ui.window.finished_notes_check.stateChanged.connect(lambda: self.note_handler._timeline.set_done_notes_visible(not self.main_ui.window.finished_notes_check.isChecked()))
		self.main_ui.window.show()

	def forward_note(self):
		self.note_handler.create_note(self.note_creator)
		self.note_creator.dialog.hide()

if __name__ == "__main__":

	app = QApplication(sys.argv)
	whatever = MainHandler()
	sys.exit(app.exec_())
