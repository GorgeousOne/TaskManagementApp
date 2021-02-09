from PySide2.QtCore import QCoreApplication, QMetaObject, Qt, QSize
from PySide2.QtWidgets import QDialog, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, \
	QGraphicsDropShadowEffect
from PySide2.QtGui import QFont, QIcon

from utils import icons_folder


class UINotePopup(QDialog):

	def __init__(self):
		super().__init__()
		self.setObjectName("Dialog")
		self.setWindowModality(Qt.ApplicationModal)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setFixedWidth(420)
		self.setFont(QFont("Segoe UI light", 12))

		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(20, 20, 20, 20)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.frame = QFrame(self)
		self.frame.setStyleSheet(
			".QFrame {\n"
			"    border:0px solid;\n"
			"    background-color: white;\n"
			"    border-radius:10px;\n"
			"}")
		self.frame.setFrameShape(QFrame.StyledPanel)
		self.frame.setFrameShadow(QFrame.Raised)
		self.frame.setObjectName("frame")

		shadow = QGraphicsDropShadowEffect(self)
		shadow.setBlurRadius(20)
		shadow.setOffset(0)
		shadow.setColor(Qt.black)
		self.frame.setGraphicsEffect(shadow)

		self.vertical_layout_2 = QVBoxLayout(self.frame)
		self.vertical_layout_2.setObjectName("verticalLayout_2")

		self.widget_top_bar = QWidget(self.frame)
		self.widget_top_bar.setStyleSheet(
			".QPushButton {\n"
			"    border: 0px solid;\n"
			"    border-radius: 20px;\n"
			"}\n"
			".QPushButton:hover:!pressed {\n"
			"    background-color: rgb(230, 230, 230);\n"
			"}")
		self.widget_top_bar.setObjectName("horizontalWidget")
		self.vertical_layout_2.addWidget(self.widget_top_bar)

		self.top_bar = QHBoxLayout(self.widget_top_bar)
		self.top_bar.setContentsMargins(10, 0, 10, 0)
		self.top_bar.setSpacing(0)
		self.top_bar.setObjectName("action_bar")
		self.top_bar.addStretch(1)

		self.btn_edit = QPushButton(self.widget_top_bar)
		self.btn_edit.setObjectName("btn_edit")
		self.btn_edit.setFixedSize(40, 40)
		self.btn_edit.setIcon(QIcon(icons_folder + "pencil.png"))
		self.btn_edit.setIconSize(QSize(50, 50))
		self.top_bar.addWidget(self.btn_edit)

		self.btn_delete = QPushButton(self.widget_top_bar)
		self.btn_delete.setObjectName("btn_delete")
		self.btn_delete.setFixedSize(40, 40)
		self.btn_delete.setIcon(QIcon(icons_folder + "trashcan.png"))
		self.btn_delete.setIconSize(QSize(50, 50))
		self.top_bar.addWidget(self.btn_delete)

		self.btn_close = QPushButton(self.widget_top_bar)
		self.btn_close.setObjectName("btn_close")
		self.btn_close.setFixedSize(40, 40)
		self.btn_close.setIcon(QIcon(icons_folder + "cross2.png"))
		self.btn_close.setIconSize(QSize(50, 50))
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
		self.title_label.setFont(QFont("Segoe UI semibold", 12))

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

		self.retranslate_ui()
		QMetaObject.connectSlotsByName(self)

		self.btn_close.clicked.connect(self.hide)

	def retranslate_ui(self):
		_translate = QCoreApplication.translate
		# self.btn_edit.setText(_translate("Dialog", "edit"))
		# self.btn_delete.setText(_translate("Dialog", "delete"))
		# self.btn_close.setText(_translate("Dialog", "close"))
		self.date_label.setText(_translate("Dialog", "Insert Date and Time"))
		self.title_label.setText(_translate("Dialog", "Insert Title"))
		self.description_label.setText(_translate("Dialog", "Insert Description"))
		self.btn_done.setText(_translate("Dialog", "Mark as done"))

	def display_note(self, note):
		date_info = note.date.toString("d. MMMM yy")
		if note.time:
			date_info += "   " + note.time.toString("HH:mm")

		self.date_label.setText(date_info)
		self.title_label.setText(note.title)
		self.description_label.setText(note.description)


if __name__ == '__main__':
	import sys
	from PySide2.QtWidgets import QApplication

	app = QApplication(sys.argv)
	ui = UINotePopup()
	ui.dialog.show()
	sys.exit(app.exec_())
