import os
from os import path
import pickle
import uuid

from model.note import Note
from uis.ui_note_editor import UINoteEditor
from uis.ui_timeline import UITimeline


class NoteHandler:
	def __init__(self, main_ui):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self._saves_file = self._saves_dir + path.sep + "data.json"
		self._load_notes()

		self._main_ui = main_ui
		self._timeline = UITimeline(self._main_ui.window.timeline_area)

		self._note_editor = UINoteEditor()
		self._note_editor.dialog.create_btn.clicked.connect(self.finish_editing_note)
		self._note_editor.dialog.create_btn.setText("Save")
		self._edited_note = None

		for note in self._notes:
			self._create_entry(note)

	def create_note(self, note_form):
		title = note_form.dialog.title_edit.text().strip()
		dialog = note_form.dialog
		description = dialog.description_edit.toPlainText().strip()
		date = dialog.date_picker.date()

		time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None
		new_note = Note(uuid.uuid4(), title, date, description, time)
		self.add_note(new_note)

	def add_note(self, note):
		self._notes.append(note)
		self.save_notes()
		self._create_entry(note)

	def _create_entry(self, new_note):
		self._main_ui.window.empty_timeline_label.hide()
		self._main_ui.window.timeline_area.show()

		entry = self._timeline.display_note(new_note)
		entry.content.toggle_done_btn.clicked.connect(lambda: self.toggle_complete_note(new_note))
		entry.content.delete_btn.clicked.connect(lambda: self.delete_note(new_note, True))
		entry.content.edit_btn.clicked.connect(lambda: self.start_editing_note(new_note))

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

	def delete_note(self, note, save_change=False):
		self._timeline.remove_note(note)
		self._notes.remove(note)
		if save_change:
			self.save_notes()

		if len(self._notes) == 0:
			self._main_ui.window.timeline_area.hide()
			self._main_ui.window.empty_timeline_label.show()

	def start_editing_note(self, note):
		self._note_editor.clear()
		self._note_editor.dialog.title_edit.setText(note.title)
		self._note_editor.dialog.description_edit.setPlainText(note.description)
		self._note_editor.dialog.date_picker.setDate(note.date)

		if note.time:
			self._note_editor.dialog.time_picker.setTime(note.time)
			self._note_editor.dialog.enable_time_check.setChecked(True)

		self._edited_note = note
		self._note_editor.dialog.show()

	def finish_editing_note(self):
		dialog = self._note_editor.dialog
		self._edited_note.title = dialog.title_edit.text().strip()
		self._edited_note.description = dialog.description_edit.toPlainText().strip()
		self._edited_note.date = dialog.date_picker.date()
		self._edited_note.time = dialog.time_picker.time() if dialog.enable_time_check.isChecked() else None

		self._edited_note.update_listeners()
		for entry in self._edited_note._listeners:
			entry._section.update_entry(entry)

		self._edited_note = None

		self._note_editor.dialog.hide()
		self._note_editor.clear()
		self.save_notes()

	def toggle_complete_note(self, note):
		note.toggle_is_done()
		note.update_listeners()
		self.save_notes()
