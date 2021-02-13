from PySide2.QtWidgets import QFrame, QVBoxLayout, QGraphicsDropShadowEffect, QGraphicsColorizeEffect
from PySide2.QtGui import QColor
from PySide2.QtUiTools import QUiLoader


class UINoteEntry(QFrame):
	def __init__(self, note, container):
		super().__init__()
		self._note = note

		self.setStyleSheet(
			"""
			QFrame {
				border: 0px solid;
				border-radius: 3px;
				background-color: rgb(255, 255, 255);
			}
			"""
		)

		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.setMaximumWidth(1400)
		self.verticalLayout.setObjectName("verticalLayout")

		self.content = QUiLoader().load("./uis/res/ui_note_entry.ui")
		self.verticalLayout.addWidget(self.content)

		self.shadow_effect = QGraphicsDropShadowEffect(container)
		self.shadow_effect.setBlurRadius(10)
		self.shadow_effect.setOffset(0)
		self.shadow_effect.setColor(QColor(0, 0, 0, 30))
		self.setGraphicsEffect(self.shadow_effect)

		self.content.details_widget.hide()

		self.gray_out_effect = QGraphicsColorizeEffect(self)
		self.gray_out_effect.setColor(QColor(255, 255, 255))
		self.gray_out_effect.setStrength(0.95)
		self.content.button_bar.setGraphicsEffect(self.gray_out_effect)

		self.update_content()

	def enterEvent(self, event):
		self.shadow_effect.setColor(QColor(0, 0, 0, 60))
		self.gray_out_effect.setEnabled(False)

	def leaveEvent(self, event):
		self.shadow_effect.setColor(QColor(0, 0, 0, 30))
		self.gray_out_effect.setEnabled(True)

	def mouseReleaseEvent(self, event):
		collapse = self.content.details_widget.isVisible()
		if collapse:
			self.collapse_details()
		else:
			self.fold_out_details()

	def fold_out_details(self):
		self.content.details_widget.setVisible(True)
		self.content.title_label.setStyleSheet("""font: 63 12pt "Segoe UI Semibold";""")

	def collapse_details(self):
		self.content.details_widget.setVisible(False)
		self.content.title_label.setStyleSheet("")


	def update_content(self):
		"""Updates the displayed information about the note."""
		self.content.title_label.setText(self._note.title)
		self.content.description_label.setText(self._note.description)

		if self._note.time:
			self.content.time_label.setText(self._note.time.toString("HH:mm"))
		else:
			self.content.time_label.hide()
