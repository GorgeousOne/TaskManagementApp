import sys
import uuid

from PySide2.QtWidgets import QApplication

from control.note_handler import NoteHandler
from model.note import Note
from uis.ui_main import UIMainWindow
from uis.ui_note_editor import UINoteEditor
from uis.ui_project_editor import UIProjectEditor


class MainHandler:
	def __init__(self):
		self.main_ui = UIMainWindow()
		self.note_creator = UINoteEditor()
		self.note_editor = UINoteEditor()
		self.project_editor = UIProjectEditor()

		self.note_handler = NoteHandler()

		self.setup_ui()
		self.setup_ui_functions()
		self.main_ui.window.show()

		self.edited_note = None

	def setup_ui(self):
		for note in self.note_handler.get_notes():
			self.create_entry(note)
		self.note_editor.dialog.create_btn.setText("Save")

	def setup_ui_functions(self):
		self.main_ui.window.create_note_btn.clicked.connect(self.note_creator.show_updated)
		self.main_ui.window.finished_notes_check.stateChanged.connect(
			lambda: self.main_ui.timeline.set_done_notes_visible(
				not self.main_ui.window.finished_notes_check.isChecked()))

		self.note_creator.dialog.create_btn.clicked.connect(lambda: self.create_note(self.note_creator))
		self.note_editor.dialog.create_btn.clicked.connect(self.finish_editing_note)

	def create_note(self, note_form):
		title = note_form.dialog.title_edit.text().strip()
		dialog = note_form.dialog
		description = dialog.description_edit.toPlainText().strip()
		date = dialog.date_picker.date()

		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		new_note = Note(uuid.uuid4(), title, date, description, time)

		self.note_handler.add_note(new_note)
		self.create_entry(new_note)
		self.note_creator.dialog.hide()

	def create_entry(self, new_note):
		self.main_ui.window.empty_timeline_label.hide()
		self.main_ui.window.timeline_area.show()

		entry = self.main_ui.timeline.display_note(new_note)
		entry.content.toggle_done_btn.clicked.connect(lambda: self.toggle_note_completion(new_note))
		entry.content.delete_btn.clicked.connect(lambda: self.delete_note(new_note))
		entry.content.edit_btn.clicked.connect(lambda: self.start_editing_note(new_note))

	def toggle_note_completion(self, note):
		note.toggle_is_done()
		note.update_listeners()
		self.note_handler.save_notes()

	def start_editing_note(self, note):
		self.note_editor.clear()
		self.note_editor.dialog.title_edit.setText(note.title)
		self.note_editor.dialog.description_edit.setPlainText(note.description)
		self.note_editor.dialog.date_picker.setDate(note.date)

		if note.time:
			self.note_editor.dialog.time_picker.setTime(note.time)
			self.note_editor.dialog.enable_time_check.setChecked(True)

		self.edited_note = note
		self.note_editor.dialog.show()

	def finish_editing_note(self):
		form = self.note_editor.dialog
		self.edited_note.title = form.title_edit.text().strip()
		self.edited_note.description = form.description_edit.toPlainText().strip()
		self.edited_note.date = form.date_picker.date()
		self.edited_note.time = form.time_picker.time() if form.enable_time_check.isChecked() else None

		self.edited_note.update_listeners()
		for entry in self.edited_note._listeners:
			entry._section.update_entry(entry)

		self.note_editor.dialog.hide()
		self.note_editor.clear()
		self.note_handler.save_notes()
		self.edited_note = None

	def delete_note(self, note):
		self.main_ui.timeline.remove_note(note)
		self.note_handler.delete_note(note)
		self.note_handler.save_notes()

		if len(self.note_handler.get_notes()) == 0:
			self.main_ui.window.timeline_area.hide()
			self.main_ui.window.empty_timeline_label.show()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	MainHandler()
	sys.exit(app.exec_())

