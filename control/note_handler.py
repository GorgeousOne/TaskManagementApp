import os
from os import path
import pickle

from PySide2.QtCore import Qt

from model.note import Note
from uis.ui_note_entry import UINoteEntry
from uis.ui_note_popup import UINotePopup


class NoteHandler:
	def __init__(self):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self._saves_file = self._saves_dir + path.sep + "data.json"
		self._notes = self.load_notes()
		self._entries = {}
		self._details_popup = UINotePopup()

		for note in self._notes:
			self._create_entry(note)

		print(self._notes)

	def create_note(self, note_form):
		title = note_form.title.text()
		if "hello there" in title.lower():
			title = "General Kenobi!"

		description = note_form.description.toPlainText()
		date = note_form.date_picker.date()
		time = note_form.time_picker.time() if note_form.enable_time.isChecked() else None
		note = Note(title, date, description, time)

		self._notes.append(note)
		self.save_notes()
		self._create_entry(note)

	def _create_entry(self, note):
		entry = UINoteEntry(note)
		self._entries[note] = entry

	def load_notes(self):
		if path.exists(self._saves_file) and os.stat(self._saves_file).st_size > 0:
			with open(self._saves_file, 'rb') as infile:
				return pickle.load(infile)
		return []

	def save_notes(self):
		if not path.exists(self._saves_dir):
			os.makedirs(self._saves_dir)
		with open(self._saves_file, 'wb') as outfile:
			pickle.dump(self._notes, outfile)

	def display_notes(self, container, layout):
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for note in self._notes:
			layout.addWidget(self.create_note_box(note, container))

	def create_note_box(self, note, container):
		box = self._entries[note].create_button(container)
		box.clicked.connect(lambda: self.create_popup(note))
		return box

	def create_popup(self, note):

		self._details_popup.display_note(note)

		if not self._details_popup.isVisible():
			self._details_popup.show()
			self._details_popup.setFocus(Qt.PopupFocusReason)
			print(self._details_popup.font())
