import bisect

from uis.ui_date_section import UIDateSection


class UITimeline:

	def __init__(self, container):
		self.container = container
		self.layout = container.layout()

		self.dates = []
		self.sections = []

	def display_note(self, note):
		date = note.date
		section = None

		if date not in self.dates:
			section = self.insert_date(date)
		else:
			index = self.dates.index(date)
			section = self.sections[index]

		section.display_note(note, self.container)

	def insert_date(self, new_date):
		new_section = UIDateSection(new_date)
		index = bisect.bisect(self.dates, new_date)

		self.dates.insert(index, new_date)
		self.sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section
