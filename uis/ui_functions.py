from PySide2 import QtCore
from PySide2.QtCore import (QPropertyAnimation)
# from main import MainWindow
import main


class UIFunctions(main.MainWindow):

	def toggle_menu(self, min_extended, max_extend, set_expanded):
		if set_expanded:
			width = self.ui.frame_left_menu.width()

			if width == min_extended:
				widthExtended = max_extend
			else:
				widthExtended = min_extended

			self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
			self.animation.setDuration(400)
			self.animation.setStartValue(width)
			self.animation.setEndValue(widthExtended)
			self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
			self.animation.start()
