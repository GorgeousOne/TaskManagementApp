import os
from os import path
import pickle
import bisect


class NoteHandler:
	def __init__(self):
		self.notes = []
		self.projects = []
		self.saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"

		self.note_saves = self.saves_dir + path.sep + "notes.json"
		self.project_saves = self.saves_dir + path.sep + "projects.json"

		self.load_projects()
		self.load_notes()

	def get_notes(self, hide_completed=False, project=None):
		filtered_notes = []
		for note in self.notes:
			if hide_completed and note.is_done:
				continue
			if project and note.project != project:
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
		note = self.notes.pop(index)
		self.save_notes()
		return note

	def add_project(self, project):
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
			if note.project == project:
				note.project = None
				note.update_listeners()
		self.save_projects()
		self.save_notes()

	def load_notes(self):
		if path.exists(self.note_saves) and os.stat(self.note_saves).st_size > 0:
			with open(self.note_saves, 'rb') as infile:
				self.notes = pickle.load(infile)
			self.notes.sort()
			# replaces doppelganger projects pickle created when loading the notes
			for note in self.notes:
				if note.project:
					note.project = self.projects[self.projects.index(note.project)]

	def load_projects(self):
		if path.exists(self.project_saves) and os.stat(self.project_saves).st_size > 0:
			with open(self.project_saves, 'rb') as infile:
				self.projects = pickle.load(infile)
			self.projects.sort()
			self.save_projects()

	def save_notes(self):
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

	def match_project(self, name):
		for project in self.projects:
			if project.get_name() == name:
				return project
		raise Exception("No project found with name: " + name)
