import bisect
from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from uis.ui_note_item import UiNoteItem


class UiDateSection(QtWidgets.QWidget):
	"""An widget for displaying all note items of one day together with a dividing line and date title"""
	def __init__(self, date):
		super().__init__()
		self.date = date
		self.note_items = []

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)

		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd d. MMMM"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.vertical_layout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		# creates the dividing line
		self.line = QtWidgets.QFrame(self)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.vertical_layout.addWidget(self.line)

		self.note_area = QtWidgets.QWidget(self)
		self.vertical_layout.addWidget(self.note_area)

		self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.note_area)
		self.vertical_layout_2.setContentsMargins(10, 10, 10, 10)
		self.vertical_layout_2.setSpacing(10)

	def get_note_count(self):
		return len(self.note_items)

	def any_notes_are_visible(self):
		for note in self.note_items:
			if note.isVisible():
				return True
		return False

	def display_note(self, new_note):
		new_item = UiNoteItem(new_note, self)
		index = bisect.bisect_right(self.note_items, new_item)

		self.note_area.layout().insertWidget(index, new_item)
		self.note_items.insert(index, new_item)
		return new_item

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

	def __lt__(self, other):
		if not isinstance(other, UiDateSection):
			return False
		return self.date < other.date
