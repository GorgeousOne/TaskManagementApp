import bisect
from uis.ui_date_section import UiDateSection


class UiTimeline:
	"""Takes the given widget and adds notes to it in form of note entries which are sorted by date sections"""
	def __init__(self, container, main_handler):
		self.main_handler = main_handler
		self.container = container
		self.layout = container.layout()

		self.date_sections = []
		self.displayed_notes = dict()

		self.are_done_notes_visible = True
		self.filtered_project = None
		self.out_filtered_items = []

	def display_note(self, note):
		date = note.date
		section = None

		for existing_section in self.date_sections:
			if existing_section.date == note.date:
				section = existing_section
				break

		if not section:
			section = self.insert_date(date)

		self.displayed_notes[note] = section
		note.add_listener(self)

		item = section.display_note(note)
		item.content.toggle_done_btn.clicked.connect(lambda: self.main_handler.toggle_note_completion(note))
		item.content.delete_btn.clicked.connect(lambda: self.main_handler.delete_note(note))
		item.content.edit_btn.clicked.connect(lambda: self.main_handler.start_editing_note(note))

	def on_note_change(self, note):
		section = self.displayed_notes[note]
		if section.date == note.date:
			section.update_item(note)
		else:
			self.remove_note(note)
			self.display_note(note)

	def set_done_notes_visible(self, state):
		self.are_done_notes_visible = state

		for section in self.date_sections:
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
		for section in self.date_sections:
			for item in section.note_items:
				if item.note.project != project:
					item.setVisible(False)
					self.out_filtered_items.append(item)

	def remove_note(self, note):
		note.remove_listener(self)
		section = self.displayed_notes[note]
		section.remove_note(note)

		if section.get_note_count() == 0:
			self.remove_section(section)
		del self.displayed_notes[note]

	def insert_date(self, new_date):
		new_section = UiDateSection(new_date)
		index = bisect.bisect(self.date_sections, new_section)

		self.date_sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section

	def remove_section(self, section):
		section.hide()
		section.deleteLater()
		self.date_sections.remove(section)
