import os
from os import path
import pickle

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QPushButton

from model.note import Note


class NoteHandler:
	def __init__(self):
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self.saves_file = self.saves_dir + path.sep + "data.json"
		self.saves_file2 = self.saves_dir + path.sep + "data2.json"

		self.notes = self.load_notes()
		print(self.notes)

	def create_note(self, note_form):
		title = note_form.title.text()
		if "hello there" in title.lower():
			title = "General Kenobi!"

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
		box.setFixedSize(QSize(300, 40))
		box.setText(note.title)
		font = box.font()
		font.setStrikeOut(True)
		box.setFont(font)
		box.setLayoutDirection(Qt.RightToLeft)

		box.setStyleSheet(
			"	text-align: left;\n"
			"   padding: 10px;\n"
			"   border: 1px solid;\n"
			"   border-radius: 5px;\n"
			"   border-color: rgb(133, 227, 70);\n"
			"   background-color: rgb(133, 227, 70);\n"
		)

		box_width = box.width() - 2 * 10
		text_width = box.fontMetrics().boundingRect(box.text()).width()

		# create a gradient for makes long texts to fade out
		if text_width > box_width:
			rel_start = str((box_width - 30) / text_width)
			rel_end = str(box_width / text_width)
			box.setStyleSheet(box.styleSheet() + (
				"	color: qlineargradient("
				"spread:pad, x1:" + rel_start + ", y1:0, x2: " + rel_end + ", y2:0,"
				"stop:0 rgb(0, 0, 0), stop:1 rgba(0, 0, 0, 0));\n"
			))

		box.setStyleSheet(box.styleSheet() + (
			"}\n"
			"QPushButton:hover:!pressed {\n"
			"   background-color: rgb(153, 247, 90);\n"
			"}"
		))
		return box
