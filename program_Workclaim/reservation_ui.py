import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox,
                             QDateEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QFrame, QMessageBox)
from PyQt5.QtCore import QDate, Qt

class ReservationScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WorkClaim - Reservation Page')
        self.resize(550, 450)
        self.setStyleSheet("background-color: #f8f9fa;") 

        # Ana Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        #Başlık
        title_label = QLabel("Reservation Page")
        title_label.setStyleSheet("font-size: 22px; color: #2c3e50; font-family: 'Segoe UI', Arial;")
        main_layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        # Facility Type 
        self.combo_facility = QComboBox()
        self.combo_facility.addItem("<select a facility type>")
        self.combo_facility.addItems(["Classroom", "Meeting Room", "Conference Room", "Library Desk"])
        
        # Filter
        self.combo_filters = QComboBox()
        self.combo_filters.addItem("<select filters>")
        self.combo_filters.addItems(["Projector", "Whiteboard", "Sound System"])

        # Date Picker
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True) 
        self.date_edit.setDate(QDate.currentDate()) 

        # Start Time
        self.combo_start_time = QComboBox()
        self.combo_start_time.addItems([f"{i:02d}:00" for i in range(8, 20)]) 

        # End Time
        self.combo_end_time = QComboBox()
        self.combo_end_time.addItems([f"{i:02d}:00" for i in range(9, 21)])

        input_style = """
            QComboBox, QDateEdit { 
                padding: 6px; 
                border: 1px solid #ced4da; 
                border-radius: 4px; 
                background-color: white;
                font-size: 14px;
            }
            QComboBox::drop-down { border: 0px; }
        """
        self.combo_facility.setStyleSheet(input_style)
        self.combo_filters.setStyleSheet(input_style)
        self.date_edit.setStyleSheet(input_style)
        self.combo_start_time.setStyleSheet(input_style)
        self.combo_end_time.setStyleSheet(input_style)

        label_style = "font-size: 14px; color: #495057;"
        
        lbl_facility = QLabel("Select Facility Type:")
        lbl_facility.setStyleSheet(label_style)
        form_layout.addRow(lbl_facility, self.combo_facility)

        lbl_filters = QLabel("Select Filters:")
        lbl_filters.setStyleSheet(label_style)
        form_layout.addRow(lbl_filters, self.combo_filters)

        lbl_date = QLabel("Select Date:")
        lbl_date.setStyleSheet(label_style)
        form_layout.addRow(lbl_date, self.date_edit)

        lbl_start = QLabel("Start Time:")
        lbl_start.setStyleSheet(label_style)
        form_layout.addRow(lbl_start, self.combo_start_time)

        lbl_end = QLabel("End Time:")
        lbl_end.setStyleSheet(label_style)
        form_layout.addRow(lbl_end, self.combo_end_time)

        main_layout.addLayout(form_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #e9ecef;")
        main_layout.addWidget(line)

        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Reserve Butonu
        self.btn_reserve = QPushButton("Reserve Facility")
        self.btn_reserve.setStyleSheet("""
            QPushButton {
                background-color: #2b6cb0; 
                color: white; 
                padding: 10px 20px; 
                font-size: 14px; 
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2c5282; }
        """)

        # Back Butonu
        self.btn_back = QPushButton("Back to Main Menu")
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0; 
                color: #4a5568; 
                padding: 10px 20px; 
                font-size: 14px; 
                border: 1px solid #cbd5e0;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #cbd5e0; }
        """)

        button_layout.addWidget(self.btn_reserve)
        button_layout.addWidget(self.btn_back)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # EVENTS
        self.btn_reserve.clicked.connect(self.handle_reservation)
        self.btn_back.clicked.connect(self.go_back)

    #BUSINESS LOGIC FONKSİYONLARI

    def handle_reservation(self):
        """Kullanıcı Reserve Facility butonuna bastığında tetiklenir."""
        # Kullanıcının girdiği veriler
        facility_type = self.combo_facility.currentText()
        selected_date = self.date_edit.date().toString(Qt.ISODate)
        start_time = self.combo_start_time.currentText()
        end_time = self.combo_end_time.currentText()

        # Hata Kontrolleri
        if facility_type == "<select a facility type>":
            QMessageBox.warning(self, "Warning", "Please select a valid facility type to proceed.")
            return

        if start_time >= end_time:
            QMessageBox.warning(self, "Time Error", "End time must be after the start time.")
            return

        # Database Bağlanacak Kısım!!!!!
        # from database_functions import Database
        # db = Database()
        # db.reserve(current_user_id, facility_id) 
        
        # Şimdilik başarılı simülasyon
        success_msg = f"Request Sent!\n\nFacility: {facility_type}\nDate: {selected_date}\nTime: {start_time} - {end_time}"
        QMessageBox.information(self, "Success", success_msg)
        
        
        self.combo_facility.setCurrentIndex(0)
        self.combo_filters.setCurrentIndex(0)

    def go_back(self):
        """Back to Main Menu butonuna basıldığında tetiklenir."""
        QMessageBox.information(self, "Navigation", "Going back to Main Menu...")
        # self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReservationScreen()
    window.show()
    sys.exit(app.exec_())