import os
from os import path
import pickle
import bisect


class TaskHandler:
	"""Takes care of loading, storing and saving all tasks and projects"""
	def __init__(self):
		self.tasks = []
		self.projects = []
		# creates the path for a save directory in the user root directory
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self.task_saves = self.saves_dir + path.sep + "tasks.pickle"
		self.project_saves = self.saves_dir + path.sep + "projects.pickle"

		self.load_projects()
		self.load_tasks()

	def get_tasks(self, hide_completed=False, project=None):
		"""Returns a list of all tasks with the option to filter out tasks by project and state of completion"""
		filtered_tasks = []
		for task in self.tasks:
			if hide_completed and task.is_done:
				continue
			if project and task.get_project() != project:
				continue
			filtered_tasks.append(task)
		return filtered_tasks

	def get_projects(self):
		return self.projects

	def add_task(self, task):
		"""Registers a new task and saves afterwards"""
		bisect.insort(self.tasks, task)
		self.save_tasks()

	def delete_task(self, task):
		"""Removes the task and saves"""
		self.tasks.remove(task)
		self.save_tasks()

	def pop_task(self, index):
		"""Removes the task at the given index"""
		task = self.tasks.pop(index)
		self.save_tasks()
		return task

	def add_project(self, project):
		"""Adds project after ensuring that there is no other project with the same name"""
		for other in self.projects:
			if other.get_name() == project.get_name():
				raise Exception("There already exists a project named '{}'.".format(project.get_name()))
		bisect.insort(self.projects, project)
		self.save_projects()

	def rename_project(self, project, new_name):
		if new_name == project.get_name():
			return
		for other in self.projects:
			if other.get_name() == new_name:
				raise Exception("There already exists a project named '{}'.".format(new_name))
		project.set_name(new_name)
		self.save_projects()

	def delete_project(self, project):
		self.projects.remove(project)
		for task in self.tasks:
			if task.get_project() == project:
				task.set_project(None)
				task.update_listeners()
		self.save_projects()
		self.save_tasks()

	def load_tasks(self):
		"""Loads the tasks from the saves file"""
		if path.exists(self.task_saves) and os.stat(self.task_saves).st_size > 0:
			with open(self.task_saves, 'rb') as infile:
				self.tasks = pickle.load(infile)
			self.tasks.sort()
			# replaces the projects pickle created incorrectly when loading the tasks
			for task in self.tasks:
				if task.get_project():
					task.set_project(self.get_project_by_name(task.get_project().get_name()))

	def load_projects(self):
		if path.exists(self.project_saves) and os.stat(self.project_saves).st_size > 0:
			with open(self.project_saves, 'rb') as infile:
				self.projects = pickle.load(infile)
			self.projects.sort()
			self.save_projects()

	def save_tasks(self):
		"""Dumps the tasks to a file in saves directory"""
		self.tasks.sort()
		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)
		with open(self.task_saves, 'wb') as outfile:
			pickle.dump(self.tasks, outfile)

	def save_projects(self):
		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)
		with open(self.project_saves, 'wb') as outfile:
			pickle.dump(self.projects, outfile)

	def get_project_by_name(self, name):
		"""Returns the project with the matching name or raises an exception"""
		for project in self.projects:
			if project.get_name() == name:
				return project
		raise Exception("No project found with name: " + name)

	def get_project_by_id(self, project_id):
		"""Returns the project with the matching UUID or returns None"""
		for project in self.projects:
			if project.get_id() == project_id:
				return project
		return None
