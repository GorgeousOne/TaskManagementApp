import sys
import uuid

from PySide2 import QtWidgets

from control.note_handler import NoteHandler
from model.note import Note
from model.project import Project
from uis.ui_main import UiMainWindow
from uis.ui_note_editor import UiNoteEditor
from uis.ui_project_editor import UiProjectEditor


class MainHandler:
	def __init__(self):
		self.main_ui = UiMainWindow()
		self.note_creator = UiNoteEditor()
		self.note_editor = UiNoteEditor()
		self.project_editor = UiProjectEditor()

		self.note_handler = NoteHandler()

		self.setup_ui()
		self.setup_ui_functions()
		self.main_ui.window.show()

		self.edited_note = None

	def setup_ui(self):
		for note in self.note_handler.get_notes():
			self.create_item(note)
		self.note_editor.dialog.create_btn.setText("Save")

	def setup_ui_functions(self):
		self.main_ui.window.create_note_btn.clicked.connect(self.note_creator.show_updated)
		self.main_ui.window.finished_notes_check.stateChanged.connect(
			lambda: self.main_ui.timeline.set_done_notes_visible(
				not self.main_ui.window.finished_notes_check.isChecked()))

		self.main_ui.window.create_project_btn.clicked.connect(self.project_editor.dialog.show)
		self.project_editor.dialog.create_btn.clicked.connect(lambda: self.create_project(self.project_editor))

		self.note_creator.dialog.create_btn.clicked.connect(lambda: self.create_note(self.note_creator))
		self.note_editor.dialog.create_btn.clicked.connect(self.finish_editing_note)

	def create_note(self, note_form):
		dialog = note_form.dialog
		dialog.hide()
		title = dialog.title_edit.text().strip()
		description = dialog.description_edit.toPlainText().strip()
		date = dialog.date_picker.date()

		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		new_note = Note(uuid.uuid4(), title, date, description, time)

		self.note_handler.add_note(new_note)
		self.create_item(new_note)

	def create_item(self, new_note):
		self.main_ui.window.empty_timeline_label.hide()
		self.main_ui.window.timeline_area.show()

		item = self.main_ui.timeline.display_note(new_note)
		item.content.toggle_done_btn.clicked.connect(lambda: self.toggle_note_completion(new_note))
		item.content.delete_btn.clicked.connect(lambda: self.delete_note(new_note))
		item.content.edit_btn.clicked.connect(lambda: self.start_editing_note(new_note))

	def create_project(self, project_form):
		# project_form.dialog.hide()
		name = project_form.dialog.name_edit.text().strip()
		color = project_form.get_selected_color()
		new_project = Project(uuid.uuid4(), name, color)

		self.note_handler.add_project(new_project)
		self.main_ui.projects_bar.add_project(new_project)

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
		for item in self.edited_note._listeners:
			item.date_section.update_item(item)

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
	app = QtWidgets.QApplication(sys.argv)
	MainHandler()
	sys.exit(app.exec_())

