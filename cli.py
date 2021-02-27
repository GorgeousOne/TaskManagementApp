import argparse

from model.note_handler import NoteHandler


class CommandHandler:
	def __init__(self, sys_args):
		parser = argparse.ArgumentParser(usage="")
		parser.add_argument("command", help="Subcommand to run")

		args = parser.parse_args(sys_args[1:2])

		if not hasattr(self, args.command):
			print("Unrecognized command")
			parser.print_help()
			exit(1)

		getattr(self, args.command)(sys_args[2:])

	def timeline(self, sys_args):
		parser = argparse.ArgumentParser(description="Lists the tasks in the timeline")
		parser.add_argument("--hide", action="store_true")
		args = parser.parse_args(sys_args)

		print("Running timeline command")
		note_handler = NoteHandler()
		self.print_notes(note_handler.get_notes(args.hide))

	def print_notes(self, note_list):

		project_pad = max(len(note.title) for note in note_list)

		current_date = None
		for note in note_list:
			if current_date != note.date:
				current_date = note.date
				print("-"*20, current_date.toString("dddd d. MMMM"), "-"*20)
			print(note.text(project_pad))
		pass
