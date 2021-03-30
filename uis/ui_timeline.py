import bisect
from uis.ui_date_section import UiDateSection


class UiTimeline:
	"""Handles displaying of tasks in a linear timeline, split into sections for each day"""
	def __init__(self, container, main_handler):
		"""container: QWidget that will be used to display the tasks"""
		self.main_handler = main_handler
		self.container = container
		self.layout = container.layout()

		self.date_sections = []
		self.displayed_tasks = dict()

		self.are_done_tasks_visible = True
		self.filtered_project = None
		self.out_filtered_items = []

	def display_task(self, task):
		"""Displays a task in the timeline. Creates a new section if there was no section with the task's date before"""
		date = task.get_date()
		section = None

		for existing_section in self.date_sections:
			if existing_section.date == task.get_date():
				section = existing_section
				break

		if not section:
			section = self.insert_section(date)

		self.displayed_tasks[task] = section
		task.add_listener(self)

		item = section.display_task(task)
		item.content.toggle_done_btn.clicked.connect(lambda: self.main_handler.toggle_task_completion(task))
		item.content.edit_btn.clicked.connect(lambda: self.main_handler.start_editing_task(task, False))
		item.content.copy_btn.clicked.connect(lambda: self.main_handler.start_editing_task(task, True))
		item.content.delete_btn.clicked.connect(lambda: self.main_handler.delete_task(task))

	def on_task_change(self, task):
		"""Reorders a task after it's date/time was potentially being changed"""
		section = self.displayed_tasks[task]
		if section.date == task.get_date():
			section.update_item(task)
		else:
			self.remove_task(task)
			self.display_task(task)

	def set_done_tasks_visible(self, state):
		"""Hides or displays all tasks that are completed"""
		self.are_done_tasks_visible = state

		for section in self.date_sections:
			for item in section.task_items:
				if item.task.is_done and item not in self.out_filtered_items:
					section.set_item_visible(item, state)

	def filter_project(self, project):
		"""Hides all elements in the timeline that do not belong to the given project"""
		for item in self.out_filtered_items:
			if self.are_done_tasks_visible or not item.task.get_is_done():
				self.displayed_tasks[item.task].set_item_visible(item, True)

		self.out_filtered_items.clear()

		# reset the filtered project if a project item was clicked twice
		if project == self.filtered_project:
			self.filtered_project = None
		else:
			self.filtered_project = project
		if not self.filtered_project:
			return

		for section in self.date_sections:
			for item in section.task_items:
				if item.task.get_project() != project:
					section.set_item_visible(item, False)
					self.out_filtered_items.append(item)

	def remove_task(self, task):
		task.remove_listener(self)
		section = self.displayed_tasks[task]
		section.remove_task(task)

		if section.task_count() == 0:
			self.remove_section(section)
		del self.displayed_tasks[task]

	def insert_section(self, new_date):
		"""Inserts a section for a new date"""
		new_section = UiDateSection(new_date)
		index = bisect.bisect(self.date_sections, new_section)

		self.date_sections.insert(index, new_section)
		self.layout.insertWidget(index, new_section)
		return new_section

	def remove_section(self, section):
		section.hide()
		section.deleteLater()
		self.date_sections.remove(section)
