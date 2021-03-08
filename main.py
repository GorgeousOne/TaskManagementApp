import sys

from PySide2 import QtWidgets, QtGui

from cli import CommandHandler
from model.note_handler import NoteHandler
from model.note import Note
from model.project import Project
from uis.ui_main import UiMainWindow
from uis.ui_note_editor import UiNoteEditor
from uis.ui_project_editor import UiProjectEditor


class MainHandler:
	"""Sets up the whole GUI and it's functionality"""
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
		"""Displays all projects / tasks in the project bar / task timeline"""
		for project in self.note_handler.get_projects():
			self.create_project_item(project)
		for note in self.note_handler.get_notes():
			self.create_note_item(note)

	def setup_ui_functions(self):
		"""Connects main ui buttons and editor buttons to their tasks"""
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

		new_note = Note(title, description, date, time, project)
		self.create_note_item(new_note)
		self.note_handler.add_note(new_note)

	def create_note_item(self, new_note):
		"""creates a ui item in the timeline for a task"""
		self.main_ui.window.empty_timeline_label.hide()
		self.main_ui.window.timeline_area.show()
		self.main_ui.timeline.display_note(new_note)

	def create_project(self, project_form):
		name = project_form.get_project_name()
		color = project_form.get_selected_color()
		new_project = Project(name, color)

		self.note_handler.add_project(new_project)
		self.create_project_item(new_project)

	def create_project_item(self, project):
		"""Creates project item in the project bar and gives connects it's buttons functionality"""
		project_item = self.main_ui.projects_bar.add_project(project)
		project_item.content.delete_btn.clicked.connect(lambda: self.delete_project(project))
		project_item.content.edit_btn.clicked.connect(lambda: self.start_editing_project(project))
		project_item.connect_click(lambda: self.main_ui.timeline.filter_project(project))

	def toggle_note_completion(self, note):
		"""Toggles if a note id completed and saves"""
		note.toggle_is_done()
		note.update_listeners()
		self.note_handler.save_notes()

	def start_editing_note(self, note):
		"""Opens note editor and fills in details of note to edit"""
		self.note_editor.reset()
		self.note_editor.fill_in(note)
		self.note_editor.dialog.show()
		self.edited_note = note

	def finish_editing_note(self):
		"""Called when "Create" button in note editor is clicked.
		If a note was being edited the changes will be saved, otherwise a new note will be created+displayed"""
		self.note_editor.dialog.hide()

		if not self.edited_note:
			self.create_note(self.note_editor)
			return

		self.edited_note.set_title(self.note_editor.get_title())
		self.edited_note.set_description(self.note_editor.get_description())
		self.edited_note.set_date(self.note_editor.get_date())
		self.edited_note.set_time(self.note_editor.get_time())
		self.edited_note.set_project(self.note_editor.get_project())
		self.edited_note.update_listeners()

		self.note_handler.save_notes()
		self.edited_note = None

	def delete_note(self, note):
		"""Deletes a note and hides the time ine if no other notes are left"""
		self.main_ui.timeline.remove_note(note)
		self.note_handler.delete_note(note)

		if len(self.note_handler.get_notes()) == 0:
			self.main_ui.window.timeline_area.hide()
			self.main_ui.window.empty_timeline_label.show()

	def start_editing_project(self, project):
		"""Opens the project editor and fills in the details of this project"""
		self.project_editor.fill_in(project)
		self.project_editor.dialog.show()
		self.edited_project = project

	def finish_editing_project(self):
		"""Called when the "Create" button in the project editor is hit.
		Either a new project will be created or the one that was being edited is being updated"""
		try:
			if not self.edited_project:
				self.create_project(self.project_editor)
				self.project_editor.dialog.hide()
				return
			self.note_handler.rename_project(self.edited_project, self.project_editor.get_project_name())
		except Exception as e:
			msg = QtWidgets.QMessageBox()
			msg.setIcon(QtWidgets.QMessageBox.Critical)
			msg.setText(str(e))
			msg.setWindowTitle("Duplicate project name")
			msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
			msg.exec_()
			return

		self.edited_project.set_color(self.project_editor.get_selected_color())
		self.edited_project.update_listeners()

		self.note_handler.save_projects()
		self.edited_project = None
		self.project_editor.dialog.hide()

	def delete_project(self, project):
		self.main_ui.projects_bar.delete_project(project)
		self.note_handler.delete_project(project)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		CommandHandler(sys.argv)
		exit(-1)

	app = QtWidgets.QApplication(sys.argv)

	# adds taskbar icon app in windows
	if sys.platform == "win32":
		import ctypes
		my_app_id = "taskmanagementapp.1-0"
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
	# loads Segoe fonts in operating systems other than windows
	else:
		QtGui.QFontDatabase.addApplicationFont("./res/fonts/segoeuil.ttf")
		QtGui.QFontDatabase.addApplicationFont("./res/fonts/seguisb.ttf")

	MainHandler()
	sys.exit(app.exec_())
