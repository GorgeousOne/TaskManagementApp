import textwrap

from PySide2 import QtCore

from command import ParentCommand, ArgCommand
from model.note import Note
from model.note_handler import NoteHandler
from model.project import Project


class CommandHandler:
	def __init__(self, sys_args):
		self.note_handler = NoteHandler()
		main_cmd = ParentCommand("main")

		notes_cmd = ParentCommand("task", "Parent command for all task related commands")
		main_cmd.add_child(notes_cmd)

		list_notes_cmd = ArgCommand("list", self.list_notes, "Lists all tasks with an index, optionally filters tasks of a project or uncompleted tasks")
		notes_cmd.add_child(list_notes_cmd)
		parser = list_notes_cmd.get_parser()
		parser.add_argument("--uncompleted", "-u", action="store_true", help="hides completed tasks")
		parser.add_argument("--project", "-p", help="name of project to filter tasks by")

		create_note_cmd = ArgCommand("create", self.create_note, "Creates a new task")
		notes_cmd.add_child(create_note_cmd)
		parser = create_note_cmd.get_parser()
		parser.add_argument("title", help="title text of the task")
		parser.add_argument("date", help="date for task to be displayed at (format: dd.mm.yyyy)")
		parser.add_argument("--description", "-d", help="description text of task")
		parser.add_argument("--time", "-t", help="time of day for task to be displayed at (24h format: hh:mm)")
		parser.add_argument("--project", "-p", help="name of project for task")

		edit_note_cmd = ArgCommand("edit", self.edit_note, "Edits the passed properties of a task")
		notes_cmd.add_child(edit_note_cmd)
		parser = edit_note_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")
		parser.add_argument("--title", "-T", help="new title text for task")
		parser.add_argument("--description", "-d", help="new description for task")
		parser.add_argument("--date", "-D", help="new date of task to be displayed at (format: dd.mm.yyyy)")
		parser.add_argument("--time", "-t", help="new day time of task (24h format: hh:mm), enter empty quotes to mark as all-day")
		parser.add_argument("--project", "-p", help="name of new project for task")

		complete_note_cmd = ArgCommand("complete", self.complete_note, "Sets the completion state of a task")
		notes_cmd.add_child(complete_note_cmd)
		parser = complete_note_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")
		parser.add_argument("state", help="true/false")

		delete_note_cmd = ArgCommand("delete", self.delete_note, "Deletes a task")
		notes_cmd.add_child(delete_note_cmd)
		parser = delete_note_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in task list")

		projects_cmd = ParentCommand("project", "Parent command for all project related commands")
		main_cmd.add_child(projects_cmd)

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

		delete_project_cmd = ArgCommand("delete", self.delete_note, "Deletes a project")
		projects_cmd.add_child(delete_project_cmd)
		parser = delete_project_cmd.get_parser()
		parser.add_argument("project", help="name of the project to delete")

		main_cmd.execute(sys_args[1:])

	def list_notes(self, args):
		try:
			project = self.deserialize_project(args.project) if args.project else None
		except Exception as e:
			print(e)
			return True
		note_list = self.note_handler.get_notes(args.uncompleted, project)
		if len(note_list) == 0:
			print("No tasks listed.")
		else:
			self.print_notes(note_list)
		return True

	def create_note(self, args):
		try:
			title = self.format_title(args.title)
			description = args.description if args.description else ""
			date = self.deserialize_date(args.date)
			time = self.deserialize_time(args.time) if args.time else None
			project = self.deserialize_project(args.project) if args.project else None

			note = Note(title, description, date, time, project)
			self.note_handler.add_note(note)
			print("Added task '{}' for {}".format(note.get_title(), note.get_date().toString("dddd, d. MMMM yy.")))
		except Exception as e:
			print(e)
		return True

	def edit_note(self, args):
		try:
			note = self.note_handler.get_notes()[args.index - 1]
			if args.title is not None:
				note.set_title(self.format_title(args.title))
			if args.description is not None:
				note.set_description(args.description)
			if args.date is not None:
				note.set_date(self.deserialize_date(args.date))
			if args.time is not None:
				note.set_time(self.deserialize_time(args.time))
			if args.project is not None:
				note.set_project(self.deserialize_project(args.project))
			self.note_handler.save_notes()
			print("Edited task '{}'.".format(note.get_title()))
		except IndexError:
			print(args.index, "not in range of tasks ({})".format(str(len(self.note_handler.get_notes()))))
		except Exception as e:
			print(e)
		return True

	def complete_note(self, args):
		try:
			note = self.note_handler.get_notes()[args.index - 1]
		except IndexError:
			print(args.index, "not in range of tasks ({})".format(str(len(self.note_handler.get_notes()))))
			return True

		if args.state.lower() == "true":
			should_be_done = True
		elif args.state.lower() == "false":
			should_be_done = False
		else:
			return False

		if should_be_done:
			if note.get_is_done():
				print("Task '{}' is already completed.".format(note.get_title()))
			else:
				note.toggle_is_done()
				self.note_handler.save_notes()
				print("Completed task '{}'.".format(note.get_title()))
		else:
			if not note.get_is_done():
				print("Task '{}' was not completed yet.".format(note.get_title()))
			else:
				note.toggle_is_done()
				self.note_handler.save_notes()
				print("Reset task '{}' to uncompleted.".format(note.get_title()))
		return True

	def delete_note(self, args):
		if len(self.note_handler.get_notes()) == 0:
			print("No tasks left to delete.")
			return True
		try:
			deleted_note = self.note_handler.pop_note(args.index - 1)
			print("Deleted task '{}'.".format(deleted_note.get_title()))
		except IndexError:
			print(args.index, "not in range of tasks (" + str(len(self.note_handler.get_notes())) + ")")
		return True

	def print_notes(self, note_list):
		index_pad = len(str(len(self.note_handler.get_notes()))) + 2
		current_date = None

		for note in note_list:
			index = self.note_handler.get_notes().index(note) + 1
			if current_date != note.get_date():
				current_date = note.get_date()
				print("-" * 20, current_date.toString("dddd, d. MMMM"), "-" * 20)
			self.print_note(note, index, index_pad)

	def print_note(self, note, index, index_pad):
		header = str(index).ljust(index_pad)
		if note.get_time():
			header += note.get_time().toString("HH:mm")
			print(header)
			header = " " * index_pad

		if note.is_done:
			header += "✓ "
		header += note.get_title()
		if note.get_project():
			header += " " * 3 + "({})".format(note.get_project().get_name())
		print(header)
		if len(note.get_description()) > 0:
			print(self.wrap_text(note.get_description(), index_pad + 3, 80))

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
			raise Exception("Invalid date:'{}'. Please enter the date in the format dd.mm. or dd.mm.yyyy".format(str_date))
		return date

	def deserialize_time(self, str_time):
		if str_time == "":
			return None
		time = QtCore.QTime.fromString(str_time, "h:mm")
		if time.hour() == -1:
			raise Exception("Invalid time: '{}'. Please enter the time in the format hh:mm (24h format)".format(str_time))
		return time

	def deserialize_project(self, project_name):
		if project_name == "":
			return None
		return self.note_handler.get_project_bye_name(project_name)

	def list_projects(self, args):
		projects = self.note_handler.get_projects()
		print("-" * 20, "Projects", "-" * 20)
		for i in range(len(projects)):
			print(projects[i].get_name())
		return True

	def create_project(self, args):
		try:
			project = Project(args.name.strip()[:64])
			self.note_handler.add_project(project)
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
			self.note_handler.rename_project(project, args.new_name.strip())
			print("Renamed project to '{}'".format(new_name))
		except Exception as e:
			print(e)
		return True

	def delete_project(self, args):
		try:
			project = self.deserialize_project(args.name)
			self.note_handler.delete_project(project)
			print("Deleted project to'{}'".format(project.get_name()))
		except Exception as e:
			print(e)
		return True
