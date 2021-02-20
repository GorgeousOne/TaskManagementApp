import bisect
from uis.ui_date_section import UiDateSection


class UiTimeline:
	"""Takes the given widget and adds notes to it in form of note entries which are sorted by date sections"""
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

		return section.display_note(note)

	def set_done_notes_visible(self, state):
		for section in self.sections:
			for item in section.note_items:
				if item._note.is_done:
					item.setVisible(state)

	def remove_note(self, note):
		date = note.date
		if date not in self.dates:
			return

		section = self.sections[self.dates.index(date)]
		section.remove_note(note)
		if section.is_empty():
			self.remove_section(section)

	def insert_date(self, new_date):
		new_section = UiDateSection(new_date)
		index = bisect.bisect(self.dates, new_date)

		self.dates.insert(index, new_date)
		self.sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section

	def remove_section(self, section):
		index = self.sections.index(section)
		section.hide()
		section.deleteLater()
		self.sections.remove(section)
		self.dates.pop(index)
