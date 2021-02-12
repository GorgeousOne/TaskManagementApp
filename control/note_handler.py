import os
from os import path
import pickle
import uuid

from PySide2.QtCore import Qt

from model.note import Note
from uis.ui_note_entry import UINoteEntry
from uis.ui_note_popup import UINotePopup
from uis.ui_timeline import UITimeline


class NoteHandler:
	def __init__(self, timeline_frame):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self._saves_file = self._saves_dir + path.sep + "data.json"
		self._load_notes()
		self._entries = {}
		self._details_popup = UINotePopup()
		self._timeline = UITimeline(timeline_frame)

		for note in self._notes:
			self._create_entry(note)

	def create_note(self, note_form):
		title = note_form.dialog.title_edit.text()
		if "hello there" in title.lower():
			title = "General Kenobi!"

		dialog = note_form.dialog
		description = dialog.description_edit.toPlainText()
		date = dialog.date_picker.date()
		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		note = Note(uuid.uuid4(), date, description, time)

		self._notes.append(note)
		self.save_notes()
		self._create_entry(note)

	def _create_entry(self, note):
		entry = UINoteEntry(note)
		self._entries[note] = entry

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

	def display_notes(self):
		# layout = container.layout()
		# for i in reversed(range(layout.count())):
		# 	layout.itemAt(i).widget().setParent(None)
		for note in self._notes:
			# layout.addWidget(self.create_note_box(note, container))
			self._timeline.display_note(note)

	def create_note_box(self, note, container):
		box = self._entries[note].create_button(container)
		box.clicked.connect(lambda: self.create_popup(note))
		return box

	def create_popup(self, note):

		self._details_popup.display_note(note)

		if not self._details_popup.dialog.isVisible():
			self._details_popup.dialog.show()
			self._details_popup.dialog.setFocus(Qt.PopupFocusReason)
