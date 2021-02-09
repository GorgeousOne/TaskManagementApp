from PySide2.QtCore import QCoreApplication, QMetaObject, Qt, QSize, QFile
from PySide2.QtWidgets import QApplication, QDialog, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, \
	QGraphicsDropShadowEffect
from PySide2.QtGui import QIcon


class UINotePopup(object):
	def setup_ui(self, dialog):
		dialog.setWindowFlags(Qt.FramelessWindowHint)
		dialog.setObjectName("Dialog")
		dialog.resize(350, 420)
		dialog.setStyleSheet("font: 25 12pt \"Segoe UI\";")
		dialog.setAttribute(Qt.WA_TranslucentBackground, True)

		self.verticalLayout = QVBoxLayout(dialog)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.frame = QFrame(dialog)
		self.frame.setStyleSheet(
			".QFrame {\n"
			"    border:0px solid;\n"
			"    background-color: rgb(125, 240, 31);\n"
			"    border-radius:10px;\n"
			"}")
		self.frame.setFrameShape(QFrame.StyledPanel)
		self.frame.setFrameShadow(QFrame.Raised)
		self.frame.setObjectName("frame")

		# self.shadow = QGraphicsDropShadowEffect(dialog)
		# self.shadow.setBlurRadius(10)
		# self.frame.setGraphicsEffect(self.shadow)

		self.vertical_layout_2 = QVBoxLayout(self.frame)
		self.vertical_layout_2.setObjectName("verticalLayout_2")

		self.widget_top_bar = QWidget(self.frame)
		# self.widget_top_bar.setStyleSheet(
		# 	".QPushButton {\n"
		# 	"    border: 0px solid;\n"
		# 	"    border-radius: 20px;\n"
		# 	"    background-color: rgb(125, 240, 31);\n"
		# 	"}\n"
		# 	".QPushButton:hover:!pressed {\n"
		# 	"    background-color: rgb(158, 240, 63);\n"
		# 	"}")
		self.widget_top_bar.setObjectName("horizontalWidget")
		self.vertical_layout_2.addWidget(self.widget_top_bar)

		self.top_bar = QHBoxLayout(self.widget_top_bar)
		self.top_bar.setContentsMargins(10, 10, 10, 0)
		self.top_bar.setSpacing(10)
		self.top_bar.setObjectName("action_bar")
		self.top_bar.addStretch(1)

		self.btn_edit = QPushButton(self.widget_top_bar)
		self.btn_edit.setObjectName("btn_edit")
		# self.btn_edit.setFixedSize(40, 40)

		import os
		from os.path import sep
		my_path = os.path.dirname(os.path.abspath("requirements.txt"))
		print(my_path)
		print(QFile.exists(my_path))

		# self.btn_edit.setIcon(QIcon(icons_folder + "pencil.png"))
		# self.btn_edit.setIconSize(QSize(50, 50))
		self.top_bar.addWidget(self.btn_edit)

		self.btn_delete = QPushButton(self.widget_top_bar)
		self.btn_delete.setObjectName("btn_delete")
		self.top_bar.addWidget(self.btn_delete)

		self.btn_close = QPushButton(self.widget_top_bar)
		self.btn_close.setObjectName("btn_close")
		self.top_bar.addWidget(self.btn_close)

		self.vertical_layout_2.addLayout(self.top_bar)

		self.widget = QWidget(self.frame)
		self.widget.setObjectName("widget")

		self.info_layout = QVBoxLayout(self.widget)
		self.info_layout.setContentsMargins(30, 0, 30, 0)
		self.info_layout.setSpacing(10)
		self.info_layout.setObjectName("verticalLayout_3")

		self.date_label = QLabel(self.widget)
		self.date_label.setObjectName("date_label")
		self.info_layout.addWidget(self.date_label)

		self.title_label = QLabel(self.widget)
		self.title_label.setObjectName("title_label")
		self.info_layout.addWidget(self.title_label)

		self.description_label = QLabel(self.widget)
		self.description_label.setObjectName("description_label")
		self.info_layout.addWidget(self.description_label)
		self.vertical_layout_2.addWidget(self.widget)

		self.action_bar_2 = QHBoxLayout()
		self.action_bar_2.setContentsMargins(10, 10, 10, 10)
		self.action_bar_2.setSpacing(10)
		self.action_bar_2.setObjectName("action_bar_2")
		self.action_bar_2.addStretch(1)

		self.btn_done = QPushButton(self.frame)
		self.btn_done.setObjectName("btn_done")
		self.action_bar_2.addWidget(self.btn_done)

		self.vertical_layout_2.addLayout(self.action_bar_2)
		self.verticalLayout.addWidget(self.frame, 0, Qt.AlignTop)

		self.retranslateUi(dialog)
		QMetaObject.connectSlotsByName(dialog)


	def retranslateUi(self, dialog):
		_translate = QCoreApplication.translate
		self.btn_edit.setText(_translate("Dialog", "edit"))
		self.btn_delete.setText(_translate("Dialog", "delete"))
		self.btn_close.setText(_translate("Dialog", "close"))
		self.date_label.setText(_translate("Dialog", "Insert Date and Time"))
		self.title_label.setText(_translate("Dialog", "Insert Title"))
		self.description_label.setText(_translate("Dialog", "Insert Description"))
		self.btn_done.setText(_translate("Dialog", "Mark as done"))


if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	main_dialog = QDialog()
	ui = UINotePopup()
	ui.setup_ui(main_dialog)
	main_dialog.show()
	sys.exit(app.exec_())
