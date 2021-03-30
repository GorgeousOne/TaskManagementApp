import sys

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt

from cli import CommandHandler
from model.task_handler import TaskHandler
from model.task import Task
from model.project import Project
from uis.ui_main import UiMainWindow
from uis.ui_task_editor import UiTaskEditor
from uis.ui_project_editor import UiProjectEditor


class MainHandler:
	"""Sets up the whole GUI and it's functionality"""
	def __init__(self):
		self.task_handler = TaskHandler()

		self.main_ui = UiMainWindow(self)
		self.project_editor = UiProjectEditor()
		self.task_editor = UiTaskEditor(self.task_handler.get_projects())

		self.setup_ui()
		self.setup_ui_functions()
		self.main_ui.window.show()

		self.edited_task = None
		self.edited_project = None

	def setup_ui(self):
		"""Displays all projects and tasks in the project bar and task timeline"""
		for project in self.task_handler.get_projects():
			self.create_project_item(project)
		for task in self.task_handler.get_tasks():
			self.create_task_item(task)

	def setup_ui_functions(self):
		"""Connects main ui buttons and editor buttons to their tasks"""
		self.main_ui.window.create_task_btn.clicked.connect(self.task_editor.show_reset)
		self.main_ui.window.hide_done_tasks_check.stateChanged.connect(
			lambda: self.main_ui.timeline.set_done_tasks_visible(
				not self.main_ui.window.hide_done_tasks_check.isChecked()))

		self.main_ui.window.create_project_btn.clicked.connect(self.project_editor.show_reset)
		self.project_editor.dialog.create_btn.clicked.connect(self.finish_editing_project)
		self.task_editor.dialog.create_btn.clicked.connect(self.finish_editing_task)
		self.main_ui.window.all_projects_btn.clicked.connect(lambda: self.main_ui.timeline.filter_project(None))

	def create_task(self, task_editor):
		"""Creates a task with the information of the editor"""
		title = task_editor.get_title()
		description = task_editor.get_description()
		date = task_editor.get_date()
		time = task_editor.get_time()
		project = task_editor.get_project()

		new_task = Task(title, description, date, time, project)
		self.create_task_item(new_task)
		self.task_handler.add_task(new_task)

	def create_task_item(self, new_task):
		"""creates a ui item in the timeline for a task"""
		self.main_ui.window.empty_timeline_label.hide()
		self.main_ui.window.timeline_area.show()
		self.main_ui.timeline.display_task(new_task)

	def create_project(self, project_editor):
		"""Creates a project with the information of the editor"""
		name = project_editor.get_project_name()
		color = project_editor.get_selected_color()
		new_project = Project(name, color)

		self.task_handler.add_project(new_project)
		self.create_project_item(new_project)

	def create_project_item(self, project):
		"""Creates project item in the project bar and gives connects it's buttons functionality"""
		project_item = self.main_ui.projects_bar.add_project(project)
		project_item.content.delete_btn.clicked.connect(lambda: self.delete_project(project))
		project_item.content.edit_btn.clicked.connect(lambda: self.start_editing_project(project))
		project_item.connect_click(lambda: self.main_ui.timeline.filter_project(project))

	def toggle_task_completion(self, task):
		"""Toggles if a task id completed and saves"""
		task.toggle_is_done()
		task.update_listeners()
		self.task_handler.save_tasks()

	def start_editing_task(self, task, is_copy):
		"""Opens task editor and fills in details of task to edit"""
		self.task_editor.reset()
		self.task_editor.fill_in(task, is_copy)
		self.task_editor.dialog.show()
		# if a copy is being created the original task will not be affected in finish_editing_task
		if not is_copy:
			self.edited_task = task

	def finish_editing_task(self):
		"""Called when "Create" button in task editor is clicked.
		If a task was being edited the changes will be saved, otherwise a new task will be created+displayed"""
		self.task_editor.dialog.hide()

		if not self.edited_task:
			self.create_task(self.task_editor)
			return

		self.edited_task.set_title(self.task_editor.get_title())
		self.edited_task.set_description(self.task_editor.get_description())
		self.edited_task.set_date(self.task_editor.get_date())
		self.edited_task.set_time(self.task_editor.get_time())
		self.edited_task.set_project(self.task_editor.get_project())
		self.edited_task.update_listeners()

		self.task_handler.save_tasks()
		self.edited_task = None

	def delete_task(self, task):
		"""Deletes a task and hides the time ine if no other tasks are left"""
		self.main_ui.timeline.remove_task(task)
		self.task_handler.delete_task(task)

		if len(self.task_handler.get_tasks()) == 0:
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
			self.task_handler.rename_project(self.edited_project, self.project_editor.get_project_name())
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

		self.task_handler.save_projects()
		self.edited_project = None
		self.project_editor.dialog.hide()

	def delete_project(self, project):
		self.main_ui.projects_bar.delete_project(project)
		self.task_handler.delete_project(project)


if __name__ == "__main__":
	# runs the command handler instead of the GUI if arguments were passed
	if len(sys.argv) > 1:
		CommandHandler(sys.argv)
		exit(-1)
	# stops this one warning message from popping up
	QtCore.QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QtWidgets.QApplication(sys.argv)

	# loads Segoe fonts in other OS other than Windows, not 100% sure if that works
	if sys.platform != "win32":
		import os
		app_dir = os.path.dirname(os.path.abspath(__file__))
		QtGui.QFontDatabase.addApplicationFont(app_dir + "/res/fonts/segoeui.ttf")
		QtGui.QFontDatabase.addApplicationFont(app_dir + "/res/fonts/segoeuil.ttf")
		QtGui.QFontDatabase.addApplicationFont(app_dir + "/res/fonts/seguisb.ttf")
		# makes application visible in MacOs
		if sys.platform == "darwin":
			os.environ['QT_MAC_WANTS_LAYER'] = '1'

	MainHandler()
	sys.exit(app.exec_())
