from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QGraphicsDropShadowEffect

from utils import icons_folder


class UINotePopup:

	def __init__(self):
		super().__init__()

		self.dialog = QUiLoader().load("uis/res/ui_note_popup.ui")
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.setWindowFlags(Qt.FramelessWindowHint)
		self.dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		self.dialog.title_label.setWordWrap(True)
		self.dialog.description_label.setWordWrap(True)
		
		shadow = QGraphicsDropShadowEffect(self.dialog)
		shadow.setBlurRadius(20)
		shadow.setOffset(0)
		shadow.setColor(Qt.black)

		self.dialog.edit_btn.setIcon(QIcon(icons_folder + "pencil.png"))
		self.dialog.delete_btn.setIcon(QIcon(icons_folder + "trashcan.png"))
		self.dialog.close_btn.setIcon(QIcon(icons_folder + "cross.png"))

		self.dialog.frame.setGraphicsEffect(shadow)
		self.dialog.close_btn.clicked.connect(self.dialog.hide)


	def display_note(self, note):
		date_info = note.date.toString("dddd, d. MMMM")
		if note.time:
			date_info += " "*5 + note.time.toString("HH:mm")

		self.dialog.title_label.setText(note.title)
		self.dialog.date_label.setText(date_info)
		self.dialog.description_label.setText(note.description)


if __name__ == '__main__':
	import sys
	from PySide2.QtWidgets import QApplication

	app = QApplication(sys.argv)
	ui = UINotePopup()
	ui.dialog.show()
	sys.exit(app.exec_())
