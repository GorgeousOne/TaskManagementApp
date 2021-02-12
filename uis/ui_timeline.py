import bisect

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel
from PySide2.QtGui import QFont

from uis.QLine import QLine


class UITimeline:

	def __init__(self, container):
		self.container = container
		self.layout = container.layout()

		self.listed_dates = []
		self.date_widgets = {}

	def display_note(self, note):
		date = note.date

		if date not in self.listed_dates:
			self.insert_date(date)

	def insert_date(self, date):
		index = bisect.bisect(self.listed_dates, date)
		self.listed_dates.insert(index, date)

		date_label = QLabel(date.toString("dddd d. MMMM"))
		date_label.setAlignment(Qt.AlignHCenter)
		date_label.setStyleSheet('font: 8pt "Segoe UI";')

		separator = QLine
		self.date_widgets[date] = [date_label, separator]

		if index < len(self.listed_dates) - 1:
			next_date = self.listed_dates[index + 1]
			next_layout_index = self.index(self.date_widgets[next_date][0])

			self.layout.insertWidget(next_layout_index, date_label)
			self.layout.insertWidget(next_layout_index, QLine())
		else:
			self.layout.addWidget(date_label)
			self.layout.addWidget(QLine())

	def index(self, widget):
		for i in range(self.layout.count()):
			if self.layout.itemAt(i) == widget:
				return i
		return -1
