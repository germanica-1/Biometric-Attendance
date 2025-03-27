from PyQt5 import QtCore, QtGui, QtWidgets
from src.frontend.adding_employee_gui import EmployeeWindow
from src.backend.employee_table_service import load_data

class addEmployee(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(984, 817)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color:rgb(8, 39, 79)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.Refresh = QtWidgets.QPushButton(self.centralwidget)
        self.Refresh.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.Refresh.setFont(font)
        self.Refresh.setStyleSheet("background-color: white;")
        self.Refresh.setObjectName("Refresh")
        self.gridLayout.addWidget(self.Refresh, 0, 0, 1, 1)
        self.Refresh.clicked.connect(self.load_data)

        self.Remove = QtWidgets.QPushButton(self.centralwidget)
        self.Remove.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.Remove.setFont(font)
        self.Remove.setStyleSheet("background-color: white;")
        self.Remove.setObjectName("Remove")
        self.gridLayout.addWidget(self.Remove, 0, 2, 1, 1)

        self.Add = QtWidgets.QPushButton(self.centralwidget)
        self.Add.setMinimumSize(QtCore.QSize(180, 0))
        self.Add.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.Add.setFont(font)
        self.Add.setStyleSheet("background-color: white;")
        self.Add.setObjectName("Add")
        self.gridLayout.addWidget(self.Add, 0, 3, 1, 1)
        self.Add.clicked.connect(self.add_employee)  


        self.Back = QtWidgets.QPushButton(self.centralwidget)
        self.Back.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Back.setFont(font)
        self.Back.setStyleSheet("background-color: white;")
        self.Back.setObjectName("Back")
        self.gridLayout.addWidget(self.Back, 0, 4, 1, 1)
        self.Back.clicked.connect(self.go_back)

        self.Search = QtWidgets.QLineEdit(self.centralwidget)
        self.Search.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.Search.setFont(font)
        self.Search.setStyleSheet("background-color: white;")
        self.Search.setText("")
        self.Search.setObjectName("Search")
        self.gridLayout.addWidget(self.Search, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.EmployeeTable = QtWidgets.QTableWidget(self.centralwidget)
        self.EmployeeTable.setMaximumSize(QtCore.QSize(980, 700))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.EmployeeTable.setFont(font)
        self.EmployeeTable.setStyleSheet("background-color: white;")
        self.EmployeeTable.setWordWrap(True)
        self.EmployeeTable.setRowCount(1)
        self.EmployeeTable.setObjectName("EmployeeTable")
        self.EmployeeTable.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.EmployeeTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(1, item)
        self.EmployeeTable.horizontalHeader().setCascadingSectionResizes(False)
        self.EmployeeTable.horizontalHeader().setDefaultSectionSize(220)
        self.EmployeeTable.horizontalHeader().setMinimumSectionSize(220)
        self.EmployeeTable.horizontalHeader().setSortIndicatorShown(False)
        self.EmployeeTable.horizontalHeader().setStretchLastSection(True)
        self.EmployeeTable.verticalHeader().setVisible(True)
        self.EmployeeTable.verticalHeader().setCascadingSectionResizes(False)
        self.EmployeeTable.verticalHeader().setDefaultSectionSize(40)
        self.EmployeeTable.verticalHeader().setMinimumSectionSize(0)
        self.EmployeeTable.verticalHeader().setSortIndicatorShown(True)
        self.EmployeeTable.verticalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.EmployeeTable)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 984, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Add Employee"))
        self.Refresh.setText(_translate("MainWindow", "Refresh"))
        self.Remove.setText(_translate("MainWindow", "Remove Emplyee"))
        self.Add.setText(_translate("MainWindow", "Add New Employee"))
        self.Back.setText(_translate("MainWindow", "Back"))
        self.Search.setPlaceholderText(_translate("MainWindow", "Employee Name"))
        item = self.EmployeeTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.EmployeeTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))

    #back to admin panel
    def go_back(self):
        """Function to return to the Admin Panel."""
        from src.frontend.admin_panel import admin_panel
        self.window = QtWidgets.QMainWindow()
        self.ui = admin_panel()
        self.ui.setupUi(self.window)
        self.window.show()
        QtWidgets.QApplication.instance().activeWindow().close()  

    def add_employee(self):
        """Function to open the Adding Employee Window."""
        self.add_employee_window = EmployeeWindow() 
        self.add_employee_window.show()  

    #refresh button
    def load_data(self):
        """ Fetch and display admin data. """
        Employee = load_data(self.EmployeeTable) 
        self.EmployeeTable.setRowCount(len(Employee))
        row_height = 70
        for row_idx, row in enumerate(Employee):
            self.EmployeeTable.setRowHeight(row_idx, row_height)  
            for col_idx, data in enumerate(row.values()):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.EmployeeTable.setItem(row_idx, col_idx, item)

        self.EmployeeTable.resizeRowsToContents()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = addEmployee()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
