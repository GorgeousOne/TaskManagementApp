
from PySide2 import QtUiTools, QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt


class UiNoteEditor:
	"""A form for creating or editing notes"""
	def __init__(self, projects):
		self.projects = projects

		# makes the dialog always stay on top, frameless and translucent on the rounded edges
		self.dialog = QtUiTools.QUiLoader().load("./uis/res/ui_note_editor.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		# adds a drop shadow around the dialog
		shadow = QtWidgets.QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(30)
		shadow.setOffset(0)
		shadow.setColor(QtGui.QColor(0, 0, 0, 100))
		self.dialog.frame.setGraphicsEffect(shadow)
		self.dialog.description_edit.setPlaceholderText("Add description")

		self.dialog.date_picker.calendarPopup = True
		self.dialog.time_picker.hide()
		self.dialog.enable_time_check.stateChanged.connect(self.toggle_time_visibility)
		self.dialog.title_edit.textChanged.connect(self.toggle_btn_create)
		self.dialog.cancel_btn.clicked.connect(self.dialog.hide)

	def get_title(self):
		return self.dialog.title_edit.text().strip()

	def get_description(self):
		return self.dialog.description_edit.toPlainText().strip()

	def get_date(self):
		return self.dialog.date_picker.date()

	def get_time(self):
		return self.dialog.time_picker.time() if self.dialog.enable_time_check.isChecked() else None

	def get_project(self):
		project_index = self.dialog.projects_combo.currentIndex()
		if project_index == 0:
			return None
		else:
			return self.projects[project_index - 1]

	def toggle_time_visibility(self):
		"""Toggles visibility of the time picker when check or unchecked"""
		self.dialog.time_picker.setVisible(self.dialog.enable_time_check.isChecked())

	def toggle_btn_create(self, text):
		"""Enables or disables the create button depending if the title is set"""
		enable = len(text.strip()) > 0
		self.dialog.create_btn.setEnabled(enable)

	def show_reset(self):
		self.reset()
		self.dialog.show()
		self.dialog.title_edit.setFocus()

	def reset(self):
		"""Resets all input fields and update date and time picker to current time"""
		self.dialog.title_edit.setText("")
		self.dialog.description_edit.setPlainText("")
		self.dialog.enable_time_check.setChecked(False)
		self.dialog.create_btn.setEnabled(False)

		now = QtCore.QTime.currentTime()
		next_quarter = (now.minute() + 18) // 15 * 15
		time = QtCore.QTime(now.hour() + next_quarter // 60, next_quarter % 60)

		self.dialog.time_picker.setTime(time)
		self.dialog.date_picker.setDate(QtCore.QDate.currentDate())

		projects_combo = self.dialog.projects_combo
		projects_combo.clear()
		projects_combo.addItem("No project")

		for project in self.projects:
			projects_combo.addItem(project.get_name())

	def fill_in(self, note):
		"""Fills in the data of a note into the inputs for it to get edited"""
		self.dialog.title_edit.setText(note.title)
		self.dialog.description_edit.setPlainText(note.description)
		self.dialog.date_picker.setDate(note.date)
		self.set_project(note.project)

		if note.time:
			self.dialog.time_picker.setTime(note.time)
			self.dialog.enable_time_check.setChecked(True)

	def set_project(self, project):
		if not project:
			return
		index = self.projects.index(project) + 1
		self.dialog.projects_combo.setCurrentIndex(index)
