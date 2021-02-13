import os
from os import path
import pickle
import uuid

from model.note import Note
from uis.ui_timeline import UITimeline


class NoteHandler:
	def __init__(self, timeline_container):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self._saves_file = self._saves_dir + path.sep + "data.json"
		self._load_notes()
		self._timeline = UITimeline(timeline_container)

		for note in self._notes:
			self._timeline.display_note(note)

	def create_note(self, note_form):
		title = note_form.dialog.title_edit.text()
		if "hello there" in title.lower():
			title = "General Kenobi!"

		dialog = note_form.dialog
		description = dialog.description_edit.toPlainText()
		date = dialog.date_picker.date()

		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		note = Note(uuid.uuid4(), title, date, description, time)

		self._notes.append(note)
		self.save_notes()
		self._timeline.display_note(note)

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
