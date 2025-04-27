from PyQt5 import QtCore, QtGui, QtWidgets


class records(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1484, 849)
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
        self.Timein = QtWidgets.QPushButton(self.centralwidget)
        self.Timein.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.Timein.setFont(font)
        self.Timein.setStyleSheet("background-color: white;")
        self.Timein.setObjectName("Timein")
        self.Timein.clicked.connect(self.time_in_employee)
        self.gridLayout.addWidget(self.Timein, 0, 2, 1, 1)
        self.Back = QtWidgets.QPushButton(self.centralwidget)
        self.Back.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Back.setFont(font)
        self.Back.setStyleSheet("background-color: white;")
        self.Back.setObjectName("Back")
        self.Back.clicked.connect(self.go_back)
        self.gridLayout.addWidget(self.Back, 0, 8, 1, 1)
        self.TimeSet = QtWidgets.QPushButton(self.centralwidget)
        self.TimeSet.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.TimeSet.setFont(font)
        self.TimeSet.setStyleSheet("background-color: white;")
        self.TimeSet.setObjectName("TimeSet")
        self.TimeSet.clicked.connect(self.open_time_set)
        self.gridLayout.addWidget(self.TimeSet, 0, 5, 1, 1)
        self.Refresh = QtWidgets.QPushButton(self.centralwidget)
        self.Refresh.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Refresh.setFont(font)
        self.Refresh.setStyleSheet("background-color: white;")
        self.Refresh.setObjectName("Refresh")
        self.Refresh.clicked.connect(self.refresh_attendance_data)  
        self.gridLayout.addWidget(self.Refresh, 0, 1, 1, 1)
        self.Records = QtWidgets.QPushButton(self.centralwidget)
        self.Records.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Records.setFont(font)
        self.Records.setStyleSheet("background-color: white;")
        self.Records.setObjectName("Records")
        self.Records.clicked.connect(self.date_records)
        self.gridLayout.addWidget(self.Records, 0, 7, 1, 1)
        self.Timeout = QtWidgets.QPushButton(self.centralwidget)
        self.Timeout.setMinimumSize(QtCore.QSize(70, 0))
        self.Timeout.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.Timeout.setFont(font)
        self.Timeout.setStyleSheet("background-color: white;")
        self.Timeout.setObjectName("Timeout")
        self.Timeout.clicked.connect(self.time_out_employee)
        self.gridLayout.addWidget(self.Timeout, 0, 4, 1, 1)
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.clicked.connect(self.save_attendance_data)  # Add this line
        self.Save.setMaximumSize(QtCore.QSize(100, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.Save.setFont(font)
        self.Save.setStyleSheet("background-color: white;")
        self.Save.setObjectName("Save")
        self.gridLayout.addWidget(self.Save, 0, 6, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.EmployeeTable = QtWidgets.QTableWidget(self.centralwidget)
        self.EmployeeTable.setMinimumSize(QtCore.QSize(1350, 0))
        self.EmployeeTable.setMaximumSize(QtCore.QSize(980, 700))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.EmployeeTable.setFont(font)
        self.EmployeeTable.setStyleSheet("background-color: white;")
        self.EmployeeTable.setWordWrap(True)
        self.EmployeeTable.setRowCount(1)
        self.EmployeeTable.setObjectName("EmployeeTable")
        self.EmployeeTable.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.EmployeeTable.setHorizontalHeaderItem(5, item)
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
        self.EmployeeTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.horizontalLayout.addWidget(self.EmployeeTable)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1484, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Timein.setText(_translate("MainWindow", "Time In"))
        self.Back.setText(_translate("MainWindow", "Back"))
        self.TimeSet.setText(_translate("MainWindow", "Time Set"))
        self.Refresh.setText(_translate("MainWindow", "Refresh"))
        self.Records.setText(_translate("MainWindow", "Records"))
        self.Timeout.setText(_translate("MainWindow", "Time Out"))
        self.Save.setText(_translate("MainWindow", "Save"))
        item = self.EmployeeTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.EmployeeTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Employee"))
        item = self.EmployeeTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Time in"))
        item = self.EmployeeTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        item = self.EmployeeTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Time out"))
        item = self.EmployeeTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))

    def go_back(self):
        """Function to return to the Admin Panel."""
        from src.frontend.admin_panel import admin_panel
        self.window = QtWidgets.QMainWindow()
        self.ui = admin_panel()
        self.ui.setupUi(self.window)
        self.window.show()
        QtWidgets.QApplication.instance().activeWindow().close()  

    def open_time_set(self):
        """Function to open time set ui"""
        from src.frontend.time_set import SetWorkTimePanel
        self.ui = SetWorkTimePanel() 
        self.ui.show() #show window

    def time_in_employee(self):
        """Handle the Time In button click"""
        from src.frontend.Time_in_ui import EmployeeTimeInPanel
        self.time_in_window = EmployeeTimeInPanel()
        self.time_in_window.show()

    def time_out_employee(self):
        """Handle the Time out button click"""
        from src.frontend.Time_out_ui import EmployeeTimeOutPanel
        self.time_out_window = EmployeeTimeOutPanel()
        self.time_out_window.show()

    def date_records(self):
        """Open date of records"""
        from src.frontend.date_records import DateRecordsUI
        # Pass the table widget directly
        self.date_records_ui = DateRecordsUI(self.EmployeeTable)
        self.date_records_ui.show()


    def refresh_attendance_data(self):
        """Refresh the attendance table data"""
        from src.backend.time_in import TimeInSystem
        time_in_system = TimeInSystem(self)
        time_in_system.update_attendance_table()

    def get_employee_table(self):
        """Method to expose the table widget"""
        return self.EmployeeTable
    
    def save_attendance_data(self):
        from src.backend.save_function import SaveSystem
        """Save current attendance data to Excel"""
        save_system = SaveSystem(self)
        
        # Get the currently displayed date from the table if available
        current_date = None
        if self.EmployeeTable.rowCount() > 0:
            date_item = self.EmployeeTable.item(0, 5)  # Date is in column 5
            if date_item:
                current_date = date_item.text()
        
        save_system.save_to_excel(current_date)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = records()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
