import argparse
import textwrap

from PySide2 import QtCore

from command import ParentCommand, ArgCommand
from model.note import Note
from model.note_handler import NoteHandler


class CommandHandler:
	def __init__(self, sys_args):
		self.note_handler = NoteHandler()

		main_cmd = ParentCommand("main")

		notes_cmd = ParentCommand("task")
		main_cmd.add_child(notes_cmd)

		list_notes_cmd = ArgCommand("list", self.list_notes)
		notes_cmd.add_child(list_notes_cmd)
		parser = list_notes_cmd.get_parser()
		parser.add_argument("--uncompleted", "-u", action="store_true", help="hide completed tasks")
		parser.add_argument("--project", "-p", help="filter tasks by project name")

		create_note_cmd = ArgCommand("create", self.create_note)
		notes_cmd.add_child(create_note_cmd)
		parser = create_note_cmd.get_parser()
		parser.add_argument("title", help="set title for task")
		parser.add_argument("date", help="set deadline for task (dd.mm.yyyy)")
		parser.add_argument("--description", "-d", help="add description to task")
		parser.add_argument("--time", "-t", help="add day time to task (hh:mm 24h format)")
		parser.add_argument("--project", "-p", help="assign task to project")

		edit_note_cmd = ArgCommand("edit", self.edit_note)
		notes_cmd.add_child(edit_note_cmd)
		parser = edit_note_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in list")
		parser.add_argument("--title", "-T", help="edit title of task")
		parser.add_argument("--description", "-d", help="edit description of task")
		parser.add_argument("--date", "-D", help="edit deadline of task (dd.mm.yyyy)")
		parser.add_argument("--time", "-t", help="edit day time of task (hh:mm 24h format)")
		parser.add_argument("--project", "-p", help="edit project of task")

		close_note_cmd = ArgCommand("delete", self.delete_note)
		notes_cmd.add_child(close_note_cmd)
		parser = close_note_cmd.get_parser()
		parser.add_argument("index", type=int, help="index of task in list")

		main_cmd.execute(sys_args[1:])

	def list_notes(self, args):
		try:
			project = self.get_project(args)
		except Exception as e:
			print(str(e))
			return
		note_list = self.note_handler.get_notes(args.uncompleted, project)
		if len(note_list) == 0:
			print("No tasks listed.")
			return
		self.print_notes(note_list)

	def create_note(self, args):
		try:
			title = args.title[:64]
			description = args.description if args.description else ""
			date = self.get_date(args.date)
			time = self.get_time(args)
			project = self.get_project(args)

			note = Note(title, description, date, time, project)
			self.note_handler.add_note(note)
			print("Added task '" + note.title + "' for", note.date.toString("dddd, d. MMMM yy."))
		except Exception as e:
			print(str(e))

	def edit_note(self, args):
		pass

	def delete_note(self, args):
		if len(self.note_handler.get_notes()) == 0:
			print("No tasks left to delete.")
			return
		try:
			deleted_note = self.note_handler.pop_note(args.index-1)
			print("Deleted task '" + deleted_note.title + "'.")
		except IndexError as e:
			print(args.index, "not in list range (" + str(len(self.note_handler.get_notes())) + ")")


	def print_notes(self, note_list):
		index_pad = len(str(len(self.note_handler.get_notes()))) + 2
		current_date = None

		for note in note_list:
			index = self.note_handler.get_notes().index(note) + 1
			if current_date != note.date:
				current_date = note.date
				print("-"*20, current_date.toString("dddd, d. MMMM"), "-"*20)
			self.print_note(note, index, index_pad)

	def print_note(self, note, index, index_pad):
		header = str(index).ljust(index_pad)
		if note.time:
			header += note.time.toString("HH:mm")
			print(header)
			header = " "*index_pad

		if note.is_done:
			header += "✓ "
		header += note.title
		if note.project:
			header += " "*3 + "(" + note.project.get_name() + ")"
		print(header)
		if len(note.description) > 0:
			print(self.wrap_text(note.description, index_pad + 3, 80))

	def wrap_text(self, text, indent, margin):
		lines = textwrap.fill(text, margin-indent)
		return " "*indent + lines.replace("\n", "\n" + " "*indent)

	def get_project(self, args):
		if args.project:
			return self.note_handler.match_project(args.project)
		return None

	def get_date(self, str_date):
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
			raise Exception("Invalid date:'" + str_date + "'. Please enter the date in the format dd.mm. or dd.mm.yyyy")
		return date

	def get_time(self, args):
		if not args.time:
			return None
		time = QtCore.QTime.fromString(args.time, "h:mm")

		if time.hour() == -1:
			raise Exception("Invalid time: '" + args.time + "'. Please enter the time in the format hh:mm (24h format)")
		return time


