import bisect
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from uis.ui_note_item import UiNoteItem


class UiDateSection(QtWidgets.QWidget):
	def __init__(self, date):
		super().__init__()
		self.date = date

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

		self._times = []
		self.items = []

	def is_empty(self):
		return len(self.items) == 0

	def display_note(self, new_note):
		new_time = new_note.time if new_note.time else QtCore.QTime(0, 0)
		index = bisect.bisect_right(self._times, new_time)
		new_item = UiNoteItem(new_note, self)

		self._times.insert(index, new_time)
		self.note_area.layout().insertWidget(index, new_item)
		self.items.insert(index, new_item)
		return new_item

	def update_item(self, item):
		index = self.items.index(item)

		self._times.pop(index)
		self.items.remove(item)

		note = item._note
		time = note.time if note.time else QtCore.QTime(0, 0)

		new_index = bisect.bisect_right(self._times, note.time)
		self.note_area.layout().insertWidget(new_index, item)
		self.items.insert(new_index, item)
		self._times.insert(new_index, time)

	def remove_note(self, note):
		for i in range(len(self._times)):
			item = self.items[i]
			if item._note == note:
				item.hide()
				item.deleteLater()

				self.items.remove(item)
				self._times.pop(i)
				return
