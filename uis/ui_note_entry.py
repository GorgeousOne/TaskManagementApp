
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide2.QtGui import QColor

class UINoteEntry:
	def __init__(self, note):
		self._note = note

	def create_button(self, container, shadow_container):
		button = QPushButton(container)
		# button.setObjectName(u"insert something here")
		button.setFixedSize(QSize(300, 40))

		button.setText((self._note.time.toString("HH:mm    ") if self._note.time else "") + self._note.title)
		# if self._note.isDone:
		# 	font = button.font()
		# 	font.setStrikeOut(True)
		# 	button.setFont(font)

		button.setStyleSheet(
			"	text-align: left;\n"
			"   padding: 10px;\n"
			"   border: 1px solid;\n"
			"   border-radius: 5px;\n"
			"   border-color: rgb(230, 230, 230);\n"
			# "   background-color: rgb(133, 227, 70);\n"
		)

		shadow = QGraphicsDropShadowEffect(shadow_container)
		shadow.setBlurRadius(10)
		shadow.setOffset(0)
		shadow.setColor(QColor(0, 0, 0, 20))
		button.setGraphicsEffect(shadow)

		button_width = button.width() - 2 * 10
		text_width = button.fontMetrics().boundingRect(button.text()).width()

		# create a gradient that makes label overflow fade out
		if text_width > button_width:
			rel_start = 0  # str((button_width - 40) / text_width)
			rel_end = 1  # str(button_width / text_width)
			button.setStyleSheet(button.styleSheet() + (
				"	color: qlineargradient("
				"spread:pad, x1:" + rel_start + ", y1:0, x2: " + rel_end + ", y2:0,"
				"stop:0 rgb(0, 0, 0), stop:1 rgba(0, 0, 0, 0));\n"
			))

		button.setStyleSheet(button.styleSheet() + (
			"}\n"
			"QPushButton:hover:!pressed {\n"
			"   background-color: rgb(153, 247, 90);\n"
			"}"
		))
		return button
