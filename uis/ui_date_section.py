import bisect
from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from uis.ui_note_item import UiNoteItem


class UiDateSection(QtWidgets.QWidget):
	def __init__(self, date):
		super().__init__()
		self.date = date
		self.note_items = []

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)

		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd d. MMMM"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.verticalLayout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		self.line = QtWidgets.QFrame(self)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.verticalLayout.addWidget(self.line)

		self.note_area = QtWidgets.QWidget(self)
		self.verticalLayout.addWidget(self.note_area)

		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.note_area)
		self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
		self.verticalLayout_2.setSpacing(10)

	def is_empty(self):
		return len(self.note_items) == 0

	def display_note(self, new_note):
		new_item = UiNoteItem(new_note, self)
		index = bisect.bisect_right(self.note_items, new_item)

		self.note_area.layout().insertWidget(index, new_item)
		self.note_items.insert(index, new_item)

		new_note.add_listener(self)
		return new_item

	def on_note_change(self, note):
		self.update_item(note)

	def update_item(self, note):
		item = self.get_item(note)
		self.note_items.remove(item)
		new_index = bisect.bisect_right(self.note_items, item)
		self.note_area.layout().insertWidget(new_index, item)
		self.note_items.insert(new_index, item)

	def remove_note(self, note):
		item = self.get_item(note)
		item.hide()
		item.deleteLater()
		self.note_items.remove(item)
		return

	def get_item(self, note):
		for item in self.note_items:
			if item.note == note:
				return item
		raise Exception(str(note), "not listed in" + self.date.toString("dddd d. MMMM"))
