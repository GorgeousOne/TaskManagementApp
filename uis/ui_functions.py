from PySide2 import QtCore
from PySide2.QtCore import (QPropertyAnimation)
import main


class UIFunctions(main.MainWindow):

	def toggle_menu(self, min_extend, max_extend, set_expanded):
		if set_expanded:
			width = self.ui.frame_left_menu.width()
			width_extend = max_extend if width == min_extend else min_extend

			self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
			self.animation.setDuration(400)
			self.animation.setStartValue(width)
			self.animation.setEndValue(width_extend)
			self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
			self.animation.start()
