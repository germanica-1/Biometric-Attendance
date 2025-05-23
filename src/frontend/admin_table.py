from PyQt5 import QtCore, QtGui, QtWidgets
from src.backend.admin_table_service import load_data 
from src.frontend.adding_admin_gui import AddAdminPanel
from PyQt5.QtWidgets import QApplication
from src.backend.admin_table_service import remove_admin


class add_admin(object):
    
    def setupUi(self, AdminTable):
        AdminTable.setObjectName("Admin Table")
        AdminTable.resize(909, 565)
        AdminTable.setStyleSheet("background-color:rgb(8, 39, 79)")
        self.centralwidget = QtWidgets.QWidget(AdminTable)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.Search = QtWidgets.QPushButton(self.centralwidget)
        self.Search.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.Search.setFont(font)
        self.Search.setStyleSheet("background-color: white;")
        self.Search.setText("Refresh")
        self.Search.setObjectName("Refresh")
        self.Search.clicked.connect(self.load_data)

        self.gridLayout.addWidget(self.Search, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: white;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: white;")
        self.pushButton.setObjectName("AddAdmin")
        self.gridLayout.addWidget(self.pushButton, 0, 3, 1, 1)
        self.pushButton.clicked.connect(self.adding_admin)  

        self.RemoveADD = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveADD.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.RemoveADD.setFont(font)
        self.RemoveADD.setStyleSheet("background-color: white;")
        self.RemoveADD.setObjectName("RemoveADD")
        self.gridLayout.addWidget(self.RemoveADD, 0, 2, 1, 1)
        self.RemoveADD.clicked.connect(self.handle_remove_admin)

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

        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(980, 700))
        self.tableWidget.setStyleSheet("background-color: white;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)  # Changed to 3 columns (user, username, admin_pin)
        self.tableWidget.resizeRowsToContents()
        font = QtGui.QFont()
        font.setPointSize(20)
        self.tableWidget.setFont(font)

        # Set up header items for 3 columns
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)  # user

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)  # username

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)  # admin_pin

        self.tableWidget.horizontalHeader().setDefaultSectionSize(220)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(220)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setSortIndicatorShown(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        AdminTable.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdminTable)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 21))
        self.menubar.setObjectName("menubar")
        AdminTable.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdminTable)
        self.statusbar.setObjectName("statusbar")
        AdminTable.setStatusBar(self.statusbar)

        self.retranslateUi(AdminTable)
        QtCore.QMetaObject.connectSlotsByName(AdminTable)

    def retranslateUi(self, AdminTable):
        _translate = QtCore.QCoreApplication.translate
        AdminTable.setWindowTitle(_translate("AdminTable", "AdminTable"))
        self.Search.setText(_translate("MainWindow", "Refresh"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Username"))
        self.pushButton.setText(_translate("MainWindow", "Add New Admin"))
        self.RemoveADD.setText(_translate("MainWindow", "Remove Admin"))
        self.Back.setText(_translate("MainWindow", "Back"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "user"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "username"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "admin_pin"))

    def load_data(self):
        """Fetch and display admin data without password column."""
        admins = load_data(self.tableWidget)
        if admins is None:  # Handle case when load_data returns None
            return
            
        self.tableWidget.setRowCount(len(admins))
        row_height = 70
        for row_idx, row in enumerate(admins):
            self.tableWidget.setRowHeight(row_idx, row_height)
            col_idx = 0
            # SQLite Row object can be accessed by index or column name
            for i in range(len(row)):  # Loop through columns by index
                col_name = self.tableWidget.horizontalHeaderItem(i).text().lower()
                if col_name != 'password':  # Skip password column
                    data = row[i]  # Access by index
                    item = QtWidgets.QTableWidgetItem(str(data) if data is not None else "")
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableWidget.setItem(row_idx, col_idx, item)
                    col_idx += 1
        self.tableWidget.resizeRowsToContents()

    def handle_remove_admin(self):
        """Function to call remove_admin with input from lineEdit."""
        username = self.lineEdit.text()
        remove_admin(username, self.load_data)  

    def adding_admin(self):
        """Function to open the Adding Admin window."""
        self.admin_window = AddAdminPanel() 
        self.admin_window.show()  
    
    def go_back(self):
        """Function to return to the Admin Panel."""
        from src.frontend.admin_panel import admin_panel
        self.window = QtWidgets.QMainWindow()
        self.ui = admin_panel()
        self.ui.setupUi(self.window)
        self.window.show()
        QtWidgets.QApplication.instance().activeWindow().close()  


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = add_admin()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())