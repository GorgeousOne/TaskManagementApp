import os
from functools import partial
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
			self._create_entry(note)
			# entry.content.edit_btn.clicked.connect(lambda n=note: self.edit_note(n))

	def create_note(self, note_form):
		title = note_form.dialog.title_edit.text()
		if "hello there" in title.lower():
			title = "General Kenobi!"

		dialog = note_form.dialog
		description = dialog.description_edit.toPlainText()
		date = dialog.date_picker.date()

		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		new_note = Note(uuid.uuid4(), title, date, description, time)

		self._notes.append(new_note)
		self.save_notes()
		self._create_entry(new_note)

	def _create_entry(self, new_note):
		entry = self._timeline.display_note(new_note)
		entry.content.delete_btn.clicked.connect(lambda: self.delete_note(new_note))

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
		self._timeline.remove_note(note)
		# self._notes.remove(note)
		# self.save_notes()

	def edit_note(self, note):
		pass

	def complete_note(self, note):
		pass
