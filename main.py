import sys
import uuid

from PySide2 import QtWidgets, QtCore

from model.note_handler import NoteHandler
from model.note import Note
from model.project import Project
from uis.ui_main import UiMainWindow
from uis.ui_note_editor import UiNoteEditor
from uis.ui_project_editor import UiProjectEditor


class MainHandler:
	def __init__(self):
		self.note_handler = NoteHandler()

		self.main_ui = UiMainWindow(self)
		self.project_editor = UiProjectEditor()
		self.note_editor = UiNoteEditor(self.note_handler.get_projects())

		self.setup_ui()
		self.setup_ui_functions()
		self.main_ui.window.show()

		self.edited_note = None
		self.edited_project = None

	def setup_ui(self):
		for project in self.note_handler.get_projects():
			self.create_project_item(project)
		for note in self.note_handler.get_notes():
			self.create_note_item(note)

	def setup_ui_functions(self):
		self.main_ui.window.create_note_btn.clicked.connect(self.note_editor.show_reset)
		self.main_ui.window.hide_done_notes_check.stateChanged.connect(
			lambda: self.main_ui.timeline.set_done_notes_visible(
				not self.main_ui.window.hide_done_notes_check.isChecked()))

		self.main_ui.window.create_project_btn.clicked.connect(self.project_editor.show_reset)
		self.project_editor.dialog.create_btn.clicked.connect(self.finish_editing_project)
		self.note_editor.dialog.create_btn.clicked.connect(self.finish_editing_note)
		self.main_ui.window.all_projects_btn.clicked.connect(lambda: self.main_ui.timeline.filter_project(None))

	def create_note(self, note_form):
		title = note_form.get_title()
		description = note_form.get_description()
		date = note_form.get_date()
		time = note_form.get_time()
		project = note_form.get_project()

		new_note = Note(uuid.uuid4(), title, description, date, time, project)
		self.create_note_item(new_note)
		self.note_handler.add_note(new_note)

	def create_note_item(self, new_note):
		self.main_ui.window.empty_timeline_label.hide()
		self.main_ui.window.timeline_area.show()
		self.main_ui.timeline.display_note(new_note)

	def create_project(self, project_form):
		name = project_form.get_project_name()
		color = project_form.get_selected_color()
		new_project = Project(uuid.uuid4(), name, color)

		self.note_handler.add_project(new_project)
		self.create_project_item(new_project)

	def create_project_item(self, project):
		project_item = self.main_ui.projects_bar.add_project(project)
		project_item.content.delete_btn.clicked.connect(lambda: self.delete_project(project))
		project_item.content.edit_btn.clicked.connect(lambda: self.start_editing_project(project))
		project_item.connect_click(lambda: self.main_ui.timeline.filter_project(project))

	def toggle_note_completion(self, note):
		note.toggle_is_done()
		note.update_listeners()
		self.note_handler.save_notes()

	def start_editing_note(self, note):
		self.note_editor.reset()
		self.note_editor.fill_in(note)
		self.note_editor.dialog.show()
		self.edited_note = note

	def finish_editing_note(self):
		self.note_editor.dialog.hide()

		if not self.edited_note:
			self.create_note(self.note_editor)
			return

		self.edited_note.title = self.note_editor.get_title()
		self.edited_note.description = self.note_editor.get_description()
		self.edited_note.date = self.note_editor.get_date()
		self.edited_note.time = self.note_editor.get_time()
		self.edited_note.project = self.note_editor.get_project()

		self.edited_note.update_listeners()

		self.note_handler.save_notes()
		self.edited_note = None

	def delete_note(self, note):
		self.main_ui.timeline.remove_note(note)
		self.note_handler.delete_note(note)

		if len(self.note_handler.get_notes()) == 0:
			self.main_ui.window.timeline_area.hide()
			self.main_ui.window.empty_timeline_label.show()

	def start_editing_project(self, project):
		self.project_editor.fill_in(project)
		self.project_editor.dialog.show()
		self.edited_project = project

	def finish_editing_project(self):
		self.project_editor.dialog.hide()

		if not self.edited_project:
			self.create_project(self.project_editor)
			return

		self.edited_project.set_name(self.project_editor.get_project_name())
		self.edited_project.set_color(self.project_editor.get_selected_color())
		self.edited_project.update_listeners()

		self.note_handler.save_projects()
		self.edited_project = None

	def delete_project(self, project):
		self.main_ui.projects_bar.delete_project(project)
		self.note_handler.delete_project(project)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
	MainHandler()
	sys.exit(app.exec_())
