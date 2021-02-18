import os
from os import path
import pickle


class NoteHandler:
	def __init__(self):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self._saves_file = self._saves_dir + path.sep + "data.json"
		self._load_notes()

	def add_note(self, note):
		self._notes.append(note)
		self.save_notes()

	def _load_notes(self):
		if path.exists(self._saves_file) and os.stat(self._saves_file).st_size > 0:
			with open(self._saves_file, 'rb') as infile:
				self._notes = pickle.load(infile)
				self._notes.sort(reverse=True)
				return
		self._notes = []

	def save_notes(self):
		if not path.exists(self._saves_dir):
			os.makedirs(self._saves_dir)
		with open(self._saves_file, 'wb') as outfile:
			pickle.dump(self._notes, outfile)

	def delete_note(self, note):
		self._notes.remove(note)
		self.save_notes()

	def get_notes(self):
		return self._notes
