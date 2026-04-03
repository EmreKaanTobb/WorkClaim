import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QDateEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QFrame, QMessageBox, QListWidget,
    QSpinBox
)

from PyQt5.QtCore import QDate, Qt

# Veritabanı işlemlerini yapan sınıfı burada backend olarak kullanıyoruz.
from database_functions import Database


class ReservationScreen(QWidget):
    def __init__(self, current_user_id):
        super().__init__()

        # Sisteme giriş yapmış kullanıcının id'si
        self.current_user_id = current_user_id

        # Veritabanı nesnesi, burada kullanmak üzere kullanıyoruz.
        self.db = Database()

        # Filtreleme sonrası bulunan facility'leri burada tutuyoruz.
        # Böylece listeden seçilen facility'nin gerçek kaydına ulaşabiliyoruz.
        self.filtered_facilities = []

        # Arayüz oluşturuluyor.
        self.init_ui()

    def init_ui(self):
        
        
        #Pencere özellikleri belirleniyor.
        self.setWindowTitle('WorkClaim - Reservation Page')
        self.resize(700, 650)
        self.setStyleSheet("background-color: #f8f9fa;")
        
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)


        # Sayfa başlığı
        title_label = QLabel("Reservation Page")
        title_label.setStyleSheet(
            "font-size: 22px; color: #2c3e50; font-family: 'Segoe UI', Arial;"
        )
        main_layout.addWidget(title_label)

        # Form elemanlarını düzenlemek için
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Facility type seçimi
        self.combo_facility = QComboBox()
        self.combo_facility.addItem("<select a facility type>")
        self.combo_facility.addItems([
            "Classroom",
            "Meeting Room",
            "Conference Room",
            "Library Desk"
        ])

        # Minimum capacity seçimi
        self.spin_capacity = QSpinBox()
        self.spin_capacity.setMinimum(0)
        self.spin_capacity.setMaximum(1000)
        self.spin_capacity.setValue(0)
        self.spin_capacity.setSpecialValueText("No minimum")

        # Özellik filtreleri: Any / Yes / No
        self.combo_screen = QComboBox()
        self.combo_screen.addItems(["Any", "Yes", "No"])

        self.combo_sound = QComboBox()
        self.combo_sound.addItems(["Any", "Yes", "No"])

        self.combo_whiteboard = QComboBox()
        self.combo_whiteboard.addItems(["Any", "Yes", "No"])

        self.combo_air = QComboBox()
        self.combo_air.addItems(["Any", "Yes", "No"])

        self.combo_projector = QComboBox()
        self.combo_projector.addItems(["Any", "Yes", "No"])

        # Tarih seçimi
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd.MM.yyyy")

        # Başlangıç saati seçimi
        # 08:00 - 19:00 arası
        self.combo_start_time = QComboBox()
        self.combo_start_time.addItems([f"{i:02d}:00" for i in range(8, 20)])

        # Bitiş saati seçimi
        # 09:00 - 20:00 arası
        self.combo_end_time = QComboBox()
        self.combo_end_time.addItems([f"{i:02d}:00" for i in range(9, 21)])

        # Filtreye uyan facility'lerin gösterileceği liste
        self.facility_list = QListWidget()
        self.facility_list.setMinimumHeight(140)

        # Input elemanlarının ortak görünümü
        input_style = """
            QComboBox, QDateEdit, QSpinBox, QListWidget {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox::drop-down { border: 0px; }
        """

        # Stil verilecek widget'lar
        widgets_to_style = [
            self.combo_facility, self.spin_capacity, self.combo_screen,
            self.combo_sound, self.combo_whiteboard, self.combo_air,
            self.combo_projector, self.date_edit,
            self.combo_start_time, self.combo_end_time, self.facility_list
        ]

        # Hepsine aynı stili uygulanıyor.
        for widget in widgets_to_style:
            widget.setStyleSheet(input_style)

        label_style = "font-size: 14px; color: #495057;"

        # label oluşturma yardımcı fonksiyonu.
        def make_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            return lbl

        # Form satırları bu kısımda ekleniyor.
        form_layout.addRow(make_label("Select Facility Type:"), self.combo_facility)
        form_layout.addRow(make_label("Minimum Capacity:"), self.spin_capacity)
        form_layout.addRow(make_label("Screen:"), self.combo_screen)
        form_layout.addRow(make_label("Sound System:"), self.combo_sound)
        form_layout.addRow(make_label("Whiteboard:"), self.combo_whiteboard)
        form_layout.addRow(make_label("Air Conditioning:"), self.combo_air)
        form_layout.addRow(make_label("Projector:"), self.combo_projector)
        form_layout.addRow(make_label("Select Date:"), self.date_edit)
        form_layout.addRow(make_label("Start Time:"), self.combo_start_time)
        form_layout.addRow(make_label("End Time:"), self.combo_end_time)
        form_layout.addRow(make_label("Matching Facilities:"), self.facility_list)

        # Form ana yerleşime ekleniyor.
        main_layout.addLayout(form_layout)

  
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #e9ecef;")
        main_layout.addWidget(line)

        # Butonların yerleşimi
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Facility filtreleme butonu
        self.btn_filter = QPushButton("Filter Facilities")
        self.btn_filter.setStyleSheet("""
            QPushButton {
                background-color: #3182ce;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2b6cb0; }
        """)

        # Rezervasyon yapma butonu
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

        # Ana menüye dönüş butonu
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

        # Butonlar yatay düzene burada ekleniyor.
        button_layout.addWidget(self.btn_filter)
        button_layout.addWidget(self.btn_reserve)
        button_layout.addWidget(self.btn_back)

        # Buton düzeni ana düzene ekleniyor.
        main_layout.addLayout(button_layout)

        # Ana düzen pencereye bağlanıyor.
        self.setLayout(main_layout)

        # Butonlara tıklanınca çalışacak backend fonksiyonları.
        self.btn_filter.clicked.connect(self.handle_filter)
        self.btn_reserve.clicked.connect(self.handle_reservation)
        self.btn_back.clicked.connect(self.go_back)


    def combo_to_bool(self, combo_text):
        # ComboBox'taki metni Python bool / None değerine çevirir
        if combo_text == "Yes":
            return True
        if combo_text == "No":
            return False
        return None


    def handle_filter(self):
        # Kullanıcının seçtiği facility type alınıyor.
        facility_type = self.combo_facility.currentText()

        # Eğer kullanıcı gerçek bir seçim yapmadıysa None yapıyoruz.
        # Böylece veritabanında bu alan filtrelenmiyor.
        if facility_type == "<select a facility type>":
            facility_type = None

        # Minimum capacity değeri alınıyor.
        capacity = self.spin_capacity.value()

        # 0 ise kullanıcı minimum kapasite istemiyor demektir.
        if capacity == 0:
            capacity = None

        # Özellikler Any / Yes / No -> None / True / False şeklinde çevriliyor.
        has_screen = self.combo_to_bool(self.combo_screen.currentText())
        has_sound_system = self.combo_to_bool(self.combo_sound.currentText())
        has_whiteboard = self.combo_to_bool(self.combo_whiteboard.currentText())
        has_air_conditioning = self.combo_to_bool(self.combo_air.currentText())
        has_projector = self.combo_to_bool(self.combo_projector.currentText())

        # Veritabanından bu filtrelere uygun facility'leri çekiyoruz, backend filter_facilities kullanılıyor.
        facilities = self.db.filter_facilities(
            facility_type=facility_type,
            capacity=capacity,
            has_screen=has_screen,
            has_sound_system=has_sound_system,
            has_whiteboard=has_whiteboard,
            has_air_conditioning=has_air_conditioning,
            has_projector=has_projector
        )

        # Sonuçları saklıyoruz.
        self.filtered_facilities = facilities

        # Eski listeyi temizliyoruz.
        self.facility_list.clear()

        # Hiç sonuç gelmediyse kullanıcıya mesaj gösteriyoruz.
        if not facilities:
            QMessageBox.information(
                self,
                "No Result",
                "No facility matched the selected filters."
            )
            return


        # Bulunan facility'leri ekranda alt kısımda listeliyoruz.
        for facility in facilities:
            # facility tuplesi parçalanıyor.
            facility_id, f_type, cap, screen, sound, whiteboard, air, projector = facility

            # Kullanıcıya gösterilecek metin bu kısımda oluşturuluyor.
            item_text = (
                f"ID: {facility_id} | Type: {f_type} | Capacity: {cap} | "
                f"Screen: {screen} | Sound: {sound} | Whiteboard: {whiteboard} | "
                f"Air: {air} | Projector: {projector}"
            )

            # Listeye ekleniyor.
            self.facility_list.addItem(item_text)


    def handle_reservation(self):
        # Kullanıcının listede seçtiği satır numarasını alıyoruz.
        selected_item = self.facility_list.currentRow()

        # Seçilen tarihi ISO formatına çevir(Veritabanında problem yaşanmaması için.)
        # Örn: 2026-03-27
        selected_date = self.date_edit.date().toString(Qt.ISODate)

        # Saatler combobox'tan string olarak geliyor.
        # Örn: "09:00"
        start_time = self.combo_start_time.currentText()
        end_time = self.combo_end_time.currentText()

        # Kullanıcı listeden facility seçmediyse uyarı veriyoruz.
        if selected_item < 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a facility from the filtered list."
            )
            return

        # Bitiş saati başlangıçtan sonra olmalı. Mantıksal hata kontrolü yapıyoruz.
        if start_time >= end_time:
            QMessageBox.warning(
                self,
                "Time Error",
                "End time must be after the start time."
            )
            return

        # Kullanıcı rezervasyon limitine ulaştıysa arayüz tarafında da uyarı veriyoruz.
        if self.db.has_reached_reservation_limit(self.current_user_id):
            reservation_limit = self.db.get_user_reservation_limit(self.current_user_id)

            QMessageBox.warning(
                self,
                "Reservation Limit Reached",
                f"You have reached your reservation limit. You can have at most {reservation_limit} active reservations."
            )
            return


        # Listeden seçilen facility'nin gerçek veritabanı kaydını alıyoruz.
        selected_facility = self.filtered_facilities[selected_item]
        facility_id = selected_facility[0]

        # Debug amaçlı konsola yazdırılıyor.
        print("facility_id =", facility_id)
        print("selected_date =", selected_date)
        print("start_time =", start_time)
        print("end_time =", end_time)


        # Seçilen facility , tarih ve  saat aralığı için uygun reservation slot'unu arıyoruz.
        reservation_id = self.db.find_reservation_slot(
            facility_id=facility_id,
            date=selected_date,
            start_time=start_time,
            end_time=end_time
        )

        # Debug amaçlı reservation id'yi yazdırıyoruz.
        print("reservation_id =", reservation_id)

        # Uygun slot bulunamadıysa kullanıcıya bildiriyoruz.
        if reservation_id is None:
            QMessageBox.warning(
                self,
                "No Slot Found",
                "No reservation slot exists for the selected facility, date, and time."
            )
            return

        # Rezervasyon işlemini veritabanında gerçekleştiriyoruz.
        result_message = self.db.reserve(self.current_user_id, reservation_id)

        # Sonuç mesajını kullanıcıya gösteriyoruz.
        # Başarı varsa information, yoksa warning veriyoruz.
        if "başarıyla" in result_message.lower() or "override" in result_message.lower():
            QMessageBox.information(self, "Result", result_message)
        else:
            QMessageBox.warning(self, "Result", result_message)

    def go_back(self):

        # Geri ana sayfaya dönme .
        
        QMessageBox.information(self, "Navigation", "Going back to Main Menu...")
        


# Program doğrudan çalıştırılırsa burası devreye girer
if __name__ == '__main__':


    app = QApplication(sys.argv)

    # Test amacıyla sabit kullanıcı id'si verildi
    # Normalde bu değer login ekranından gelmeli
    current_user_id = 44412345678

    # Reservation ekranını oluşturuyoruz.
    window = ReservationScreen(current_user_id)

    window.show()

    sys.exit(app.exec_())