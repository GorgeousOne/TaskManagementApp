import json
from model.note import NoteDecoder, NoteEncoder
import os
from os import path


class NoteHandler:
	def __init__(self, saves_path):
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagerApp"
		self.saves_file = self.saves_dir + path.sep + "data.json"
		self.notes = self.load_notes()
		print(self.notes)


	def add_note(self, note):
		self.notes.append(note)
		self.save_notes()


	def load_notes(self):
		
		if path.exists(self.saves_file) and os.stat(self.saves_file).st_size > 0:
			with open(self.saves_file, 'r') as infile:
				try:
					return json.load(infile, cls=NoteDecoder)
				except json.decoder.JSONDecodeError as e:
					print("Failed to load save file:", str(e))
		return []


	def save_notes(self):

		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)

		with open(self.saves_file, 'w') as outfile:
			return json.dump(self.notes, outfile, cls=NoteEncoder, ensure_ascii=False, indent=4)


