import os
from os import path
import pickle

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QPushButton

from model.note import Note


class NoteHandler:
	def __init__(self):
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagerApp"
		self.saves_file = self.saves_dir + path.sep + "data.json"
		self.saves_file2 = self.saves_dir + path.sep + "data2.json"

		self.notes = self.load_notes()
		print(self.notes)

	def create_note(self, note_form):
		title = note_form.title.text()
		description = note_form.description.toPlainText()
		date = note_form.date_picker.date()
		time = note_form.time_picker.time() if note_form.enable_time.isChecked() else None
		note = Note(title, date, description, time)

		self.notes.append(note)
		self.save_notes()

	def load_notes(self):
		if path.exists(self.saves_file) and os.stat(self.saves_file).st_size > 0:
			with open(self.saves_file, 'rb') as infile:
				return pickle.load(infile)
		return []

	def save_notes(self):
		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)
		with open(self.saves_file, 'wb') as outfile:
			pickle.dump(self.notes, outfile)

	def display_notes(self, container, layout):
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for note in self.notes:
			layout.addWidget(self.create_note_box(note, container))

	def create_note_box(self, note, container):
		box = QPushButton(container)
		box.setObjectName(u"insert something here")
		box.setMinimumSize(QSize(0, 40))
		box.setMaximumSize(QSize(120, 80))
		box.setText(note.title)
		box.setStyleSheet(
			u"QPushButton {\n"
			"   border: none;\n"
			"   border-radius: 3px;\n"
			"   background-color: rgb(133, 227, 70);\n"
			"}\n"
			"QPushButton:hover {\n"
			"   border: 1px solid;\n"
			"   background-color: rgb(133, 227, 70);\n"
			"}"
			)
		return box
