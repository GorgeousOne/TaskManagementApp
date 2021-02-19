import bisect

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Qt

from uis.ui_note_entry import UINoteEntry


class UIDateSection(QtWidgets.QWidget):
	def __init__(self, date):
		super().__init__()
		self.date = date

		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.date_label = QtWidgets.QLabel(self)
		self.date_label.setMaximumHeight(20)
		self.date_label.setText(self.date.toString("dddd d. MMMM"))
		self.date_label.setStyleSheet("font: 8pt \"Segoe UI\";")
		self.date_label.setObjectName("date_label")
		self.verticalLayout.addWidget(self.date_label, 0, Qt.AlignHCenter)

		self.line = QtWidgets.QFrame(self)
		self.line.setFrameShape(QtWidgets.QFrame.HLine)
		self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line.setObjectName("line")
		self.verticalLayout.addWidget(self.line)

		self.note_area = QtWidgets.QWidget(self)
		self.note_area.setObjectName("note_area")

		self.verticalLayout.addWidget(self.note_area)

		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.note_area)
		self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
		self.verticalLayout_2.setSpacing(10)
		self.verticalLayout_2.setObjectName("verticalLayout_2")

		self._times = []
		self._entries = []

	def is_empty(self):
		return len(self._entries) == 0

	def display_note(self, new_note):
		new_time = new_note.time if new_note.time else QtCore.QTime(0, 0)
		index = bisect.bisect_right(self._times, new_time)
		new_entry = UINoteEntry(new_note, self)

		self._times.insert(index, new_time)
		self.note_area.layout().insertWidget(index, new_entry)
		self._entries.insert(index, new_entry)
		return new_entry

	def update_entry(self, entry):
		index = self._entries.index(entry)

		self._times.pop(index)
		self._entries.remove(entry)

		note = entry._note
		time = note.time if note.time else QtCore.QTime(0, 0)

		new_index = bisect.bisect_right(self._times, note.time)
		self.note_area.layout().insertWidget(new_index, entry)
		self._entries.insert(new_index, entry)
		self._times.insert(new_index, time)

	def remove_note(self, note):
		for i in range(len(self._times)):
			entry = self._entries[i]
			if entry._note == note:
				entry.hide()
				entry.deleteLater()

				self._entries.remove(entry)
				self._times.pop(i)
				return
