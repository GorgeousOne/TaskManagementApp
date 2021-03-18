import textwrap

from PySide2 import QtCore

from command import ParentCommand, ArgCommand
from model.task import Task
from model.task_handler import TaskHandler
from model.project import Project


class CommandHandler:
	"""A class that takes in the console arguments and processes them"""

	def __init__(self, sys_args):
		self.task_handler = TaskHandler()
		self.setup_commands()
		# executes the main command with the console arguments
		self.main_cmd.execute(sys_args[1:])

	def setup_commands(self):
		"""Sets up all the possible commands and subcommands"""
		self.main_cmd = ParentCommand("main")

		tasks_cmd = ParentCommand("task", "Parent command for all task related commands")
		self.main_cmd.add_child(tasks_cmd)

		list_tasks_cmd = ArgCommand("list", self.list_tasks, "Lists all tasks with an index, optionally filters tasks of a project or uncompleted tasks")
		tasks_cmd.add_child(list_tasks_cmd)
		parser = list_tasks_cmd.get_parser()
		parser.add_argument("--uncompleted", "-u", action="store_true", help="hides completed tasks")
		parser.add_argument("--project", "-p", help="name of project to filter tasks by")

		create_task_cmd = ArgCommand("create", self.create_task, "Creates a new task")
		tasks_cmd.add_child(create_task_cmd)
		parser = create_task_cmd.get_parser()
		parser.add_argument("title", help="title text of the task")
		parser.add_argument("date", help="date for task to be displayed at (format: dd.mm.yyyy)")
		parser.add_argument("--description", "-d", help="description text of task")
		parser.add_argument("--time", "-t", help="time of day for task to be displayed at (24h format: hh:mm)")
		parser.add_argument("--project", "-p", help="name of project for task")

		edit_task_cmd = ArgCommand("edit", self.edit_task, "Changes the passed properties of a task")
		tasks_cmd.add_child(edit_task_cmd)
		parser = edit_task_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")
		parser.add_argument("--title", "-T", help="new title text for task")
		parser.add_argument("--description", "-d", help="new description for task")
		parser.add_argument("--date", "-D", help="new date of task to be displayed at (format: dd.mm.yyyy)")
		parser.add_argument("--time", "-t", help="new day time of task (24h format: hh:mm), enter empty quotes to mark as all-day")
		parser.add_argument("--project", "-p", help="name of new project for task")

		complete_task_cmd = ArgCommand("complete", self.complete_task, "Sets the completion state of a task")
		tasks_cmd.add_child(complete_task_cmd)
		parser = complete_task_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")
		parser.add_argument("state", help="true/false")

		delete_task_cmd = ArgCommand("delete", self.delete_task, "Deletes a task")
		tasks_cmd.add_child(delete_task_cmd)
		parser = delete_task_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")

		projects_cmd = ParentCommand("project", "Parent command for all project related commands")
		self.main_cmd.add_child(projects_cmd)

		list_projects_cmd = ArgCommand("list", self.list_projects, "Lists all projects")
		projects_cmd.add_child(list_projects_cmd)

		create_project_cmd = ArgCommand("create", self.create_project, "Creates a new project")
		projects_cmd.add_child(create_project_cmd)
		parser = create_project_cmd.get_parser()
		parser.add_argument("name", help="name for the project (must be unique)")

		rename_project_cmd = ArgCommand("rename", self.rename_project, "Renames a project")
		projects_cmd.add_child(rename_project_cmd)
		parser = rename_project_cmd.get_parser()
		parser.add_argument("name", help="name of the project to rename")
		parser.add_argument("new_name", help="new name of the project")

		delete_project_cmd = ArgCommand("delete", self.delete_task, "Deletes a project")
		projects_cmd.add_child(delete_project_cmd)
		parser = delete_project_cmd.get_parser()
		parser.add_argument("project", help="name of the project to delete")
		return self.main_cmd

	def list_tasks(self, args):
		try:
			project = self.deserialize_project(args.project) if args.project else None
		except Exception as e:
			print(e)
			return True
		task_list = self.task_handler.get_tasks(args.uncompleted, project)
		if len(task_list) == 0:
			print("No tasks listed.")
		else:
			self.print_tasks(task_list)
		return True

	def create_task(self, args):
		try:
			title = self.format_title(args.title)
			description = args.description if args.description else ""
			date = self.deserialize_date(args.date)
			time = self.deserialize_time(args.time) if args.time else None
			project = self.deserialize_project(args.project) if args.project else None

			task = Task(title, description, date, time, project)
			self.task_handler.add_task(task)
			print("Added task '{}' for {}".format(task.get_title(), task.get_date().toString("dddd, d. MMMM yy.")))
		except Exception as e:
			print(e)
		return True

	def edit_task(self, args):
		try:
			task = self.task_handler.get_tasks()[args.index - 1]
			if args.title is not None:
				task.set_title(self.format_title(args.title))
			if args.description is not None:
				task.set_description(args.description)
			if args.date is not None:
				task.set_date(self.deserialize_date(args.date))
			if args.time is not None:
				task.set_time(self.deserialize_time(args.time))
			if args.project is not None:
				task.set_project(self.deserialize_project(args.project))
			self.task_handler.save_tasks()
			print("Edited task '{}'.".format(task.get_title()))
		except IndexError:
			print(args.index, "not in range of tasks ({})".format(str(len(self.task_handler.get_tasks()))))
		except Exception as e:
			print(e)
		return True

	def complete_task(self, args):
		try:
			task = self.task_handler.get_tasks()[args.index - 1]
		except IndexError:
			print(args.index, "not in range of tasks ({})".format(str(len(self.task_handler.get_tasks()))))
			return True

		if args.state.lower() == "true":
			should_be_done = True
		elif args.state.lower() == "false":
			should_be_done = False
		else:
			return False

		if should_be_done:
			if task.get_is_done():
				print("Task '{}' is already completed.".format(task.get_title()))
			else:
				task.toggle_is_done()
				self.task_handler.save_tasks()
				print("Completed task '{}'.".format(task.get_title()))
		else:
			if not task.get_is_done():
				print("Task '{}' was not completed yet.".format(task.get_title()))
			else:
				task.toggle_is_done()
				self.task_handler.save_tasks()
				print("Reset task '{}' to uncompleted.".format(task.get_title()))
		return True

	def delete_task(self, args):
		if len(self.task_handler.get_tasks()) == 0:
			print("No tasks left to delete.")
			return True
		try:
			deleted_task = self.task_handler.pop_task(args.index - 1)
			print("Deleted task '{}'.".format(deleted_task.get_title()))
		except IndexError:
			print(args.index, "not in range of tasks (" + str(len(self.task_handler.get_tasks())) + ")")
		return True

	def print_tasks(self, task_list):
		index_pad = len(str(len(self.task_handler.get_tasks()))) + 2
		current_date = None

		for task in task_list:
			index = self.task_handler.get_tasks().index(task) + 1
			if current_date != task.get_date():
				current_date = task.get_date()
				print("-" * 20, current_date.toString("dddd, d. MMMM"), "-" * 20)
			self.print_task(task, index, index_pad)

	def print_task(self, task, index, index_pad):
		header = str(index).ljust(index_pad)
		if task.get_time():
			header += task.get_time().toString("HH:mm")
			print(header)
			header = " " * index_pad

		if task.is_done:
			header += "[Done] "
		header += task.get_title()
		if task.get_project():
			header += " " * 3 + "({})".format(task.get_project().get_name())
		print(header)
		if len(task.get_description()) > 0:
			print(self.wrap_text(task.get_description(), index_pad + 3, 80))

	def wrap_text(self, text, indent, margin):
		lines = textwrap.fill(text, margin - indent)
		return " " * indent + lines.replace("\n", "\n" + " " * indent)

	def format_title(self, title):
		title = title.strip()
		if title == "":
			raise Exception("Title cannot be empty or white spaces only.")
		return title[:64]

	def deserialize_date(self, str_date):
		date = None
		if str_date.endswith("."):
			current_date = QtCore.QDate.currentDate()
			date = QtCore.QDate.fromString(str_date, "d.M.")
			date.setDate(current_date.year(), date.month(), date.day())
			if date.daysTo(current_date) < 0:
				date.addYears(1)
		else:
			date = QtCore.QDate.fromString(str_date, "d.M.yyyy")

		if date.year() == 0:
			raise Exception(
				"Invalid date:'{}'. Please enter the date in the format dd.mm. or dd.mm.yyyy".format(str_date))
		return date

	def deserialize_time(self, str_time):
		"""Creates a QTime object from a string"""
		if str_time == "":
			return None
		time = QtCore.QTime.fromString(str_time, "h:mm")
		if time.hour() == -1:
			raise Exception(
				"Invalid time: '{}'. Please enter the time in the format hh:mm (24h format)".format(str_time))
		return time

	def deserialize_project(self, project_name):
		"""Finds a project by name or """
		if project_name == "":
			return None
		return self.task_handler.get_project_by_name(project_name)

	def list_projects(self, args):
		projects = self.task_handler.get_projects()
		print("-" * 20, "Projects", "-" * 20)
		for i in range(len(projects)):
			print(projects[i].get_name())
		return True

	def create_project(self, args):
		try:
			project = Project(args.name.strip()[:64])
			self.task_handler.add_project(project)
			print("Create project '{}'.".format(project.name))
		except Exception as e:
			print(e)
		return True

	def rename_project(self, args):
		try:
			project = self.deserialize_project(args.name)
			new_name = args.new_name.strip()
			if not new_name:
				raise Exception("Project name cannot be empty or white spaces only.")
			self.task_handler.rename_project(project, args.new_name.strip())
			print("Renamed project to '{}'".format(new_name))
		except Exception as e:
			print(e)
		return True

	def delete_project(self, args):
		try:
			project = self.deserialize_project(args.name)
			self.task_handler.delete_project(project)
			print("Deleted project to'{}'".format(project.get_name()))
		except Exception as e:
			print(e)
		return True
