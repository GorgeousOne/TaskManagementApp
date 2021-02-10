from PySide2 import QtCore
from PySide2.QtCore import (QPropertyAnimation)


def toggle_menu(main_ui, min_extend, max_extend):
	width = main_ui.frame_left_menu.width()
	width_extend = max_extend if width == min_extend else min_extend

	main_ui.animation = QPropertyAnimation(main_ui.frame_left_menu, b"minimumWidth")
	main_ui.animation.setDuration(400)
	main_ui.animation.setStartValue(width)
	main_ui.animation.setEndValue(width_extend)
	main_ui.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
	main_ui.animation.start()
