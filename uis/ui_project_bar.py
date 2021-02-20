import bisect

from uis.ui_project_item import UiProjectItem


class UiProjectsBar:
	def __init__(self, container):
		self.container = container
		self.layout = container.layout
		self.project_items = []

	def add_project(self, new_project):
		new_item = UiProjectItem(new_project, self)
		index = bisect.bisect_right(self.project_items, new_project) + 1  # plus one for the already existent "All Projects" button

		self.layout().insertWidget(index, new_item)
		self.project_items.insert(index, new_item)
		return new_item
