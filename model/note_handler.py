import os
from os import path
import pickle
import bisect


class NoteHandler:
	def __init__(self):
		self._saves_dir = path.expanduser("~") + path.sep + "TaskManagementApp"

		self._note_saves = self._saves_dir + path.sep + "notes.json"
		self._project_saves = self._saves_dir + path.sep + "projects.json"

		self._load_projects()
		self._load_notes()

	def get_notes(self, hide_completed=False, project=None):
		filtered_notes = []
		for note in self._notes:
			if hide_completed and note.is_done:
				continue
			if project and note.project != project:
				continue
			filtered_notes.append(note)
		return filtered_notes

	def get_projects(self):
		return self._projects

	def add_note(self, note):
		self._notes.append(note)
		self.save_notes()

	def delete_note(self, note):
		self._notes.remove(note)
		self.save_notes()

	def add_project(self, project):
		bisect.insort(self._projects, project)
		self.save_projects()

	def delete_project(self, project):
		self._projects.remove(project)
		for note in self._notes:
			if note.project == project:
				note.project = None
				note.update_listeners()
		self.save_projects()
		self.save_notes()

	def _load_notes(self):
		if path.exists(self._note_saves) and os.stat(self._note_saves).st_size > 0:
			with open(self._note_saves, 'rb') as infile:
				self._notes = pickle.load(infile)
			# replaces doppelganger projects pickle created when loading the notes
			for note in self._notes:
				if note.project:
					note.project = self._projects[self._projects.index(note.project)]
			return
		self._notes = []

	def _load_projects(self):
		if path.exists(self._project_saves) and os.stat(self._project_saves).st_size > 0:
			with open(self._project_saves, 'rb') as infile:
				self._projects = pickle.load(infile)
				return
		self._projects = []

	def save_notes(self):
		if not path.exists(self._saves_dir):
			os.makedirs(self._saves_dir)
		with open(self._note_saves, 'wb') as outfile:
			pickle.dump(self._notes, outfile)

	def save_projects(self):
		if not path.exists(self._saves_dir):
			os.makedirs(self._saves_dir)
		with open(self._project_saves, 'wb') as outfile:
			pickle.dump(self._projects, outfile)

	def match_project(self, name):
		for project in self._projects:
			if project.get_name() == name:
				return project
		return None
