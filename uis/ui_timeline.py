import bisect
from uis.ui_date_section import UiDateSection


class UiTimeline:
	"""Takes the given widget and adds notes to it in form of note entries which are sorted by date sections"""
	def __init__(self, container):
		self.container = container
		self.layout = container.layout()

		self.dates = []
		self.sections = []

		self.are_done_notes_visible = True
		self.filtered_project = None

		self.out_filtered_items = []

	def display_note(self, note):
		date = note.date
		section = None

		if date not in self.dates:
			section = self._insert_date(date)
		else:
			index = self.dates.index(date)
			section = self.sections[index]

		return section.display_note(note)

	def set_done_notes_visible(self, state):
		self.are_done_notes_visible = state

		for section in self.sections:
			for item in section.note_items:
				if item.note.is_done and item not in self.out_filtered_items:
					item.setVisible(state)

	def filter_project(self, project):
		"""Hides all elements in the timeline that do not belong to the project (shows all which were hidden before)"""
		for item in self.out_filtered_items:
			item.setVisible(not item.note.is_done or self.are_done_notes_visible)

		self.out_filtered_items.clear()
		self.filtered_project = project

		if not project:
			return
		for section in self.sections:
			for item in section.note_items:
				if item.note.project != project:
					item.setVisible(False)
					self.out_filtered_items.append(item)

	def remove_note(self, note):
		date = note.date
		if date not in self.dates:
			return

		section = self.sections[self.dates.index(date)]
		section.remove_note(note)
		if section.is_empty():
			self._remove_section(section)

	def _insert_date(self, new_date):
		new_section = UiDateSection(new_date)
		index = bisect.bisect(self.dates, new_date)

		self.dates.insert(index, new_date)
		self.sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section

	def _remove_section(self, section):
		index = self.sections.index(section)
		section.hide()
		section.deleteLater()
		self.sections.remove(section)
		self.dates.pop(index)
