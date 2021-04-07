''' 
Module: Clipboard History
Technology: Python PyQT5
Developer: Daniyal Tariq
'''

import sys

from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QAction, QApplication, QHeaderView, \
    QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
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
        self.app = app

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
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Adding cells in table
        self.tableWidget.move(0, 0)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.event_on_click)
        self.tableWidget.cellChanged.connect(self.event_cell_changed)

        # This property holds how the widget shows a context menu
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # This signal is emitted when the widget's contextMenuPolicy is Qt::CustomContextMenu,
        # and the user has requested a context menu on the widget.
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.viewport().installEventFilter(self)
        self.prepareMenu()

    def prepareMenu(self):
        ''' Function will prepare right click menu along with actions '''

        # Create menu
        self.menu = QMenu(self)
        # Create Action
        copyAction = QAction('Copy', self)
        removeAction = QAction('Remove', self)
        # Add Action
        self.menu.addAction(copyAction)
        self.menu.addAction(removeAction)

        # Integrate the triggers
        copyAction.triggered.connect(
            lambda: self.app.clipboard().setText(self.item.text()))
        removeAction.triggered.connect(lambda: print(
            self.tableWidget.removeRow(self.item.row())))

    def eventFilter(self, source, event):
        ''' Builtin function to validate right click and copy cell '''
        if(event.type() == QtCore.QEvent.MouseButtonPress and
           event.buttons() == QtCore.Qt.RightButton and
           source is self.tableWidget.viewport()):
            # Copy item in context
            item = self.tableWidget.itemAt(event.pos())
            print('Global Pos:', event.globalPos())
            if item is not None:
                self.item = item
        return super(App, self).eventFilter(source, event)

    def generateMenu(self, pos):
        ''' Function to Generate & Execute the menu '''
        try:
            self.menu.exec_(self.tableWidget.mapToGlobal(pos))
        except:
            pass

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
