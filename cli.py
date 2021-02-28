import argparse

from command import ParentCommand, ArgCommand
from model.note_handler import NoteHandler


class CommandHandler:
	def __init__(self, sys_args):
		main_cmd = ParentCommand("main")

		notes_cmd = ParentCommand("note")
		main_cmd.add_child(notes_cmd)

		create_note_cmd = ArgCommand("create", self.create_note)
		notes_cmd.add_child(create_note_cmd)

		parser = create_note_cmd.get_parser()
		parser.add_argument("-title")
		parser.add_argument("-date")
		parser.add_argument("--description")
		parser.add_argument("--time")
		parser.add_argument("--project")

		list_notes_cmd = ArgCommand("list", self.list_notes)
		notes_cmd.add_child(list_notes_cmd)

		parser = list_notes_cmd.get_parser()
		parser.add_argument("--uncompleted", action="store_true")
		parser.add_argument("--project")

		main_cmd.execute(sys_args[1:])

	def list_notes(self, args):
		note_handler = NoteHandler()
		project = None

		if args.project:
			project = note_handler.match_project(args.project)
			if not project:
				print("No project found with name:", args.project)
				return

		self.print_notes(note_handler.get_notes(args.uncompleted, project))

	def create_note(self, args):


		print("Created note")

	def edit_note(self, args):
		pass

	def delete_note(self, sys_args):
		pass

	def projects(self, sys_args):
		parser = argparse.ArgumentParser(usage="")
		parser.add_argument("command", help="Subcommand to run")
		args = parser.parse_args(sys_args[:1])
		cmd_name = args.command + "_project"

		if not hasattr(self, cmd_name):
			print("Unrecognized command")
			parser.print_help()
			exit(1)

		getattr(self, cmd_name)(sys_args[1:])

	def print_notes(self, note_list):
		project_pad = max(len(note.title) for note in note_list)
		current_date = None

		for note in note_list:
			if current_date != note.date:
				current_date = note.date
				print("-"*20, current_date.toString("dddd d. MMMM"), "-"*20)
			print(note.text(project_pad))
		pass
