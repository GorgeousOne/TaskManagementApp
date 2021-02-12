
from PySide2.QtWidgets import QFrame, QSizePolicy


class QLine(QFrame):

	def __init__(self):
		super().__init__()
		self.setFrameShape(QFrame.HLine)
		self.setFrameShadow(QFrame.Sunken)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)