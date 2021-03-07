import bisect

from uis.ui_project_item import UiProjectItem


class UiProjectsBar:
	"""Handles adding and removing of project items for projects in the sidebar"""
	def __init__(self, container):
		self.layout = container.layout
		self.project_items = []

	def add_project(self, new_project):
		"""Adds project item for project, sorting the items alphabetically"""
		new_item = UiProjectItem(new_project)
		index = bisect.bisect_right(self.project_items, new_item)

		self.project_items.insert(index, new_item)
		self.layout().insertWidget(index, new_item)

		new_project.add_listener(self)
		return new_item

	def on_project_change(self, project):
		self.update_item(project)

	def update_item(self, project):
		"""Updates the index of the project item when it's name is changed"""
		item = self.get_item(project)
		self.project_items.remove(item)
		new_index = bisect.bisect_right(self.project_items, item)
		self.layout().insertWidget(new_index, item)
		self.project_items.insert(new_index, item)

	def delete_project(self, project):
		item = self.get_item(project)
		if item.project == project:
			item.hide()
			item.deleteLater()

			self.project_items.remove(item)
			return

	def get_item(self, project):
		"""Finds the item connected to a project"""
		for item in self.project_items:
			if item.project == project:
				return item
