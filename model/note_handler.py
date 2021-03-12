import os
from os import path
import pickle
import bisect


class NoteHandler:
	"""Takes care of loading, storing and saving all tasks and projects"""
	def __init__(self):
		self.notes = []
		self.projects = []

		# creates the path for a save directory in the user root directory
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"
		self.note_saves = self.saves_dir + path.sep + "notes.json"
		self.project_saves = self.saves_dir + path.sep + "projects.json"

		self.load_projects()
		self.load_notes()

	def get_notes(self, hide_completed=False, project=None):
		"""Returns a list of all tasks with the option to filter out tasks by project and state of completion"""
		filtered_notes = []
		for note in self.notes:
			if hide_completed and note.is_done:
				continue
			if project and note.get_project() != project:
				continue
			filtered_notes.append(note)
		return filtered_notes

	def get_projects(self):
		return self.projects

	def add_note(self, note):
		bisect.insort(self.notes, note)
		self.save_notes()

	def delete_note(self, note):
		self.notes.remove(note)
		self.save_notes()

	def pop_note(self, index):
		"""Removes the note at the given index"""
		note = self.notes.pop(index)
		self.save_notes()
		return note

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
		for note in self.notes:
			if note.get_project() == project:
				note.set_project(None)
				note.update_listeners()
		self.save_projects()
		self.save_notes()

	def load_notes(self):
		"""Loades the tasks from the saves file"""
		if path.exists(self.note_saves) and os.stat(self.note_saves).st_size > 0:
			with open(self.note_saves, 'rb') as infile:
				self.notes = pickle.load(infile)
			self.notes.sort()
			# replaces the projects pickle created incorrectly when loading the notes
			for note in self.notes:
				if note.get_project():
					note.set_project(self.get_project_by_id(note.get_project().get_id()))

	def load_projects(self):
		if path.exists(self.project_saves) and os.stat(self.project_saves).st_size > 0:
			with open(self.project_saves, 'rb') as infile:
				self.projects = pickle.load(infile)
			self.projects.sort()
			self.save_projects()

	def save_notes(self):
		"""Dumps the notes to a file in saves directory"""
		self.notes.sort()
		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)
		with open(self.note_saves, 'wb') as outfile:
			pickle.dump(self.notes, outfile)

	def save_projects(self):
		if not path.exists(self.saves_dir):
			os.makedirs(self.saves_dir)
		with open(self.project_saves, 'wb') as outfile:
			pickle.dump(self.projects, outfile)

	def get_project_bye_name(self, name):
		for project in self.projects:
			if project.get_name() == name:
				return project
		raise Exception("No project found with name: " + name)

	def get_project_by_id(self, project_id):
		for project in self.projects:
			if project.get_id() == project_id:
				return project
		return None
