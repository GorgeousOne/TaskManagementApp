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

	def update_item(self, item):
		self.project_items.remove(item)
		new_index = bisect.bisect_right(self.project_items, item) + 1
		self.layout().insertWidget(new_index, item)
		self.project_items.insert(new_index, item)

	def delete_project(self, project):
		for i in range(len(self.project_items)):
			item = self.project_items[i]
			if item.project == project:
				item.hide()
				item.deleteLater()

				self.project_items.remove(item)
				return
