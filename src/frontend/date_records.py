from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMainWindow, QCalendarWidget,
    QMessageBox, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from src.backend.records_function import RecordsBackend

class DateRecordsUI(QMainWindow):
    def __init__(self, employee_table):
        super().__init__()
        self.employee_table = employee_table  # Store the table reference
        self.backend = RecordsBackend()
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle('Date of Records')
        self.setFixedSize(500, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        main_layout = QVBoxLayout(self.central_widget)
        
        title = QLabel('Date of Records')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.calendar = QCalendarWidget()
        self.calendar.setFont(QFont('Times New Roman', 12))
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(1900, 1, 1))
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.setSelectedDate(QDate.currentDate())
        
        self.selected_date_label = QLabel()
        self.selected_date_label.setFont(QFont('Times New Roman', 14))
        self.selected_date_label.setAlignment(Qt.AlignCenter)
        self.update_selected_date_label()
        
        self.calendar.selectionChanged.connect(self.update_selected_date_label)

        search_btn = QPushButton('Search Records')
        search_btn.setFont(QFont('Arial', 12, QFont.Bold))
        search_btn.setFixedSize(200, 40)
        search_btn.clicked.connect(self.handle_search)

        main_layout.addSpacing(20)
        main_layout.addWidget(self.calendar)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.selected_date_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(search_btn, alignment=Qt.AlignCenter)
        main_layout.addStretch()

    def update_selected_date_label(self):
        selected_date = self.calendar.selectedDate()
        self.selected_date_label.setText(f"Selected Date: {selected_date.toString('yyyy-MM-dd')}")

    def handle_search(self):
            selected_date = self.calendar.selectedDate()
            date_str = selected_date.toString("yyyy-MM-dd")
            
            try:
                # Get records from backend
                records = self.backend.get_records_by_date(date_str)
                
                if not self.employee_table:
                    raise Exception("Table reference not available")
                    
                # Clear and populate the table
                self.employee_table.setRowCount(0)
                
                if not records:
                    self.show_message(f"No records found for {date_str}")
                    return

                for row_number, row_data in enumerate(records):
                    self.employee_table.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.employee_table.setItem(row_number, column_number, item)
                
                self.close()
                self.show_message(f"Showing {len(records)} records for {date_str}")

            except Exception as e:
                self.show_message(str(e))

    def show_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(text)
        msg.exec_()