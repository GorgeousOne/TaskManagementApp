from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore

import utils


class UiNoteItem(QtWidgets.QFrame):
	"""A timeline item for displaying the data of a note"""
	def __init__(self, note, date_section):
		super().__init__()
		self.note = note
		self.note.add_listener(self)
		self.project = None

		self.date_section = date_section
		self.setStyleSheet(
			"""
			border: 0px solid;
			border-radius: 5px;
			"""
		)

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)
		self.setMaximumWidth(1300)

		self.content = QtUiTools.QUiLoader().load("./uis/scripts/ui_note_item.ui")
		self.vertical_layout.addWidget(self.content)

		self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect(self.date_section)
		self.shadow_effect.setBlurRadius(10)
		self.shadow_effect.setOffset(0)
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 40))
		self.setGraphicsEffect(self.shadow_effect)

		self.content.details_widget.hide()
		self.content.button_bar.hide()
		self.content.project_btn.hide()

		self.on_note_change(self.note)
		self.on_project_change(self.note.get_project())

	def enterEvent(self, event: QtCore.QEvent):
		"""Amplifies the drop shadow of the item when hovered over it"""
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 80))
		self.content.button_bar.show()

	def leaveEvent(self, event: QtCore.QEvent):
		self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 40))
		self.content.button_bar.hide()

	def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
		"""Shows and hides the description of the note when clicked"""
		collapse = self.content.details_widget.isVisible()
		if collapse:
			self.collapse_details()
		else:
			self.fold_out_details()

	def fold_out_details(self):
		self.content.details_widget.setVisible(True)
		self.content.title_label.setStyleSheet("""font: semibold "Segoe UI";""")

	def collapse_details(self):
		self.content.details_widget.setVisible(False)
		self.content.title_label.setStyleSheet("")

	def on_note_change(self, note):
		"""Updates the displayed information about the note when it calls an update event"""
		self.content.title_label.setText(note.get_title())

		description = note.get_description()
		if description == "":
			self.content.description_label.hide()
		else:
			self.content.description_label.show()
			self.content.description_label.setText(utils.highlight_urls(description))

		if note.get_time():
			self.content.time_label.show()
			self.content.time_label.setText(note.get_time().toString("HH:mm"))
		else:
			self.content.time_label.hide()

		self.on_project_change(note.get_project())

		# updates the col
		if note.get_is_done():
			self.content.toggle_done_btn.setText("Undo")
			self.shadow_effect.setEnabled(False)
			styles = utils.replace_property(self.styleSheet(), "background", "rgb(240, 245, 255)")
			styles = utils.replace_property(styles, "color", "rgb(200, 200, 200)")
			self.setStyleSheet(styles)
		else:
			self.content.toggle_done_btn.setText("Complete")
			self.shadow_effect.setEnabled(True)
			styles = utils.replace_property(self.styleSheet(), "background", "rgb(255, 255, 255)")
			styles = utils.replace_property(styles, "color", "rgb(0, 0, 0)")
			self.setStyleSheet(styles)

	def on_project_change(self, project):
		"""Updates the project icon"""
		# removes the old project in case there is no new one
		if self.project:
			self.project.remove_listener(self)
			self.content.project_btn.hide()
			self.project = None

		# adds the new project if not None
		if project:
			self.project = project
			self.project.add_listener(self)

			# updates the icon's color (gray if the note is completed)
			new_color = QtGui.QColor(235, 235, 235) if self.note.get_is_done() else project.get_color()
			project_style = self.content.project_btn.styleSheet()
			project_style = utils.replace_property(project_style, "background", new_color.name())
			self.content.project_btn.setStyleSheet(project_style)
			# sets the capital letter in the icon
			self.content.project_btn.setText(project.get_name()[0].upper())
			self.content.project_btn.show()

	def __lt__(self, other):
		if not isinstance(other, UiNoteItem):
			return False
		return self.note < other.note
