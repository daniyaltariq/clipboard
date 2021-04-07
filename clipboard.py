# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow
# import sys


# def window():
# 	app = QApplication(sys.argv)
# 	win = QMainWindow()
# 	win.setGeometry(200, 200, 300, 300)
# 	win.setWindowTitle("Clipboard History")

# 	label = QtWidgets.QLabel(win)
# 	label.setText("Management System")
# 	label.move(50, 50)

# 	app.clipboard().dataChanged.connect(lambda: changed(app.clipboard()))


# 	win.show()
# 	sys.exit(app.exec_())

# def changed(clipboard):
# 	print(clipboard.text())

# window()

import sys
from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QMessageBox, QHeaderView, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

	def __init__(self, app):
		super().__init__()
		self.title = 'Clipboard History'
		self.left = 0
		self.top = 0
		self.width = 300
		self.height = 200
		self.row = 0
		self.column = 0

		app.clipboard().dataChanged.connect(
			lambda: self.event_data_changed(app.clipboard()))
		self.initUI()

	def initUI(self):
		self.setWindowIcon(QIcon('icon.png'))
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.createTable()

		# Add box layout, add table to box layout and add box layout to widget
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.tableWidget)
		self.setLayout(self.layout)

		# Show widget
		self.show()

	def createTable(self):
	   # Create table
		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(5)
		self.tableWidget.setColumnCount(1)
		self.tableWidget.setHorizontalHeaderLabels(["History"])
		self.tableWidget.horizontalHeader().setStretchLastSection(True);
		self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# Adding cells in table
		self.tableWidget.move(0, 0)
		# table selection change
		self.tableWidget.doubleClicked.connect(self.event_on_click)
		self.tableWidget.cellChanged.connect(self.event_cell_changed)

	def setTableCell(self, value):
		item = QTableWidgetItem(value)
		item.setTextAlignment(Qt.Qt.AlignCenter)
		self.tableWidget.setItem(self.row, self.column, item)
		self.column += 1
		self.tableWidget.setRowCount(5 + self.column)

	def event_cell_changed(self, row, column):
		item = self.tableWidget.currentItem()
		if item:
			item.setTextAlignment(Qt.Qt.AlignCenter)

	def event_data_changed(self, clipboard):
		if not self.search(clipboard.text()):
			self.setTableCell(clipboard.text())

	@pyqtSlot()
	def event_on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
				  currentQTableWidgetItem.text())

	def search(self, target):
		items = self.tableWidget.findItems(target, QtCore.Qt.MatchExactly)
		if not items:
			results = 'Found Nothing'
			# QMessageBox.information(self, 'Search Results', results)
			return False
		return True

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App(app)
	sys.exit(app.exec_())  
