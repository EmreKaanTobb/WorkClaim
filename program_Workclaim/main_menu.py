import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QListWidget, 
                             QListWidgetItem, QMessageBox, QDialog, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# Proje dosyaların
from database_functions import Database
from reservation_ui import ReservationScreen

class Main(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.db_manager = Database()
        self.active_windows = []
        
        # Kullanıcı bilgilerini en başta bir kez çekelim
        self.user_data = self.db_manager.get_user(self.user_id)
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("WorkClaim - Dashboard")
        self.resize(1000, 750)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f7f9fc; }
            #lbl_main { font-size: 26px; font-weight: bold; color: #2c3e50; }
            .MenuButon { border: 1px solid #d1d9e6; background: white; color: #555; 
                         font-size: 14px; padding: 8px 15px; border-radius: 8px; margin-left: 10px; }
            .MenuButon:hover { background-color: #f1f1f1; color: #000; }
            
            #btn_new { background-color: #5cb85c; color: white; border-radius: 12px; font-size: 18px; font-weight: 600; min-height: 90px; border: none; }
            #btn_cancel { background-color: #d9534f; color: white; border-radius: 12px; font-size: 18px; font-weight: 600; min-height: 90px; border: none; }
            #res_frame { background-color: white; border: 1px solid #e1e8ed; border-radius: 15px; }
            QListWidget { border: none; background: transparent; font-size: 15px; }
            QListWidget::item { height: 60px; border-bottom: 1px solid #f1f1f1; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 30, 40, 40)

        # 1. ÜST BAR (Kullanıcı Adı Butonun Yanında)
        top_bar = QHBoxLayout()
        lbl_title = QLabel("Dashboard")
        lbl_title.setObjectName("lbl_main")
        top_bar.addWidget(lbl_title)
        top_bar.addStretch()
        
        # AYARLAR BUTONU (İsim Burada Gözüküyor)
        username = self.user_data[1] if self.user_data else "User"
        self.btn_settings = QPushButton(f"Settings")
        self.btn_settings.setProperty("class", "MenuButon")
        self.btn_settings.clicked.connect(self.open_settings)
        
        self.btn_logout = QPushButton("🚪 Logout")
        self.btn_logout.setProperty("class", "MenuButon")
        self.btn_logout.clicked.connect(self.handle_logout)
        
        top_bar.addWidget(self.btn_settings)
        top_bar.addWidget(self.btn_logout)
        main_layout.addLayout(top_bar)

        # 2. KULLANICI BİLGİ PANELİ
        self.welcome_lbl = QLabel()
        main_layout.addWidget(self.welcome_lbl)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e1e8ed; margin: 10px 0;")
        main_layout.addWidget(line)

        # 3. ANA İÇERİK
        content_layout = QHBoxLayout()
        content_layout.setSpacing(35)

        action_layout = QVBoxLayout()
        action_layout.setSpacing(20)
        self.btn_new = QPushButton("📅  New Reservation")
        self.btn_new.setObjectName("btn_new")
        self.btn_new.clicked.connect(self.open_reservation)
        self.btn_cancel = QPushButton("🗑️  Cancel Reservation")
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.cancel_selected)
        action_layout.addWidget(self.btn_new)
        action_layout.addWidget(self.btn_cancel)
        action_layout.addStretch()
        content_layout.addLayout(action_layout, 2)

        res_frame = QFrame()
        res_frame.setObjectName("res_frame")
        res_v_layout = QVBoxLayout(res_frame)
        res_v_layout.addWidget(QLabel("<b>Your Active & Recent Reservations</b>"))
        self.res_list_widget = QListWidget()
        res_v_layout.addWidget(self.res_list_widget)
        content_layout.addWidget(res_frame, 3)

        main_layout.addLayout(content_layout)
        self.load_reservations()

    # --- AYARLAR VE ŞİFRE DEĞİŞTİRME ---

    def open_settings(self):
        """Kullanıcı adı ve şifre değiştirme alanı olan ayarlar penceresi."""
        dialog = QDialog(self)
        dialog.setWindowTitle("User Settings")
        dialog.setFixedSize(350, 420)
        dialog.setStyleSheet("background-color: white; font-family: 'Segoe UI';")
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 20, 25, 25)

        # Başlık Bölümü
        username = self.user_data[1] if self.user_data else "Unknown"
        header = QLabel(f"👤 {username}")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #2d3748;")
        layout.addWidget(header)
        
        info_label = QLabel(f"User ID: {self.user_id}")
        info_label.setStyleSheet("color: #718096; font-size: 13px;")
        layout.addWidget(info_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #edf2f7; background-color: #edf2f7; min-height: 1px; margin: 10px 0;")
        layout.addWidget(line)

        # ŞİFRE DEĞİŞTİRME ALANI
        layout.addWidget(QLabel("<b>Change Password</b>"))
        
        self.new_pass_input = QLineEdit()
        self.new_pass_input.setPlaceholderText("Enter new password")
        self.new_pass_input.setEchoMode(QLineEdit.Password)
        self.new_pass_input.setStyleSheet("padding: 8px; border: 1px solid #cbd5e0; border-radius: 5px;")
        layout.addWidget(self.new_pass_input)

        btn_update_pass = QPushButton("Update Password")
        btn_update_pass.setStyleSheet("background-color: #3182ce; color: white; font-weight: bold; padding: 8px; border-radius: 5px;")
        
        def update_pass():
            new_p = self.new_pass_input.text()
            if len(new_p) < 4:
                QMessageBox.warning(dialog, "Short Password", "Password must be at least 4 characters.")
                return
            
            # Database fonksiyonunu çağırıyoruz
            res = self.db_manager.update_password(self.user_id, new_p)
            QMessageBox.information(dialog, "Success", res)
            self.new_pass_input.clear()

        btn_update_pass.clicked.connect(update_pass)
        layout.addWidget(btn_update_pass)

        layout.addStretch()

        # HESABI SİL BUTONU
        btn_del = QPushButton("🗑 Delete My Account")
        btn_del.setStyleSheet("background-color: #fff5f5; color: #c53030; font-weight: bold; padding: 10px; border: 1px solid #feb2b2;")
        
        def delete_db():
            if QMessageBox.critical(dialog, "Delete Account", "This cannot be undone! Delete?", 
                                   QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                res = self.db_manager.delete_user(self.user_id)
                QMessageBox.information(None, "Deleted", res)
                dialog.accept()
                self.force_logout()

        btn_del.clicked.connect(delete_db)
        layout.addWidget(btn_del)
        
        dialog.exec_()

    # --- DİĞER FONKSİYONLAR ---

    def update_user_info_label(self):
        user_data = self.db_manager.get_user(self.user_id)
        if user_data:
            role_map = {1: ("Student", "#3182ce"), 2: ("Teacher", "#d9534f"), 3: ("Admin", "#5cb85c")}
            role_text, role_color = role_map.get(user_data[2], ("User", "#555"))
            max_limit = self.db_manager.get_user_reservation_limit(self.user_id)
            active_count = self.db_manager.get_active_reservation_count(self.user_id)
            remaining = max_limit - active_count if max_limit is not None else 0
            
            self.welcome_lbl.setText(
                f"<span style='font-size: 22px; font-weight: bold; color: #1a202c;'>Welcome, {user_data[1]}</span><br>"
                f"<span style='color: {role_color}; font-weight: 600;'>{role_text}</span> | "
                f"Remaining Rights: <b>{remaining} / {max_limit}</b>"
            )

    def load_reservations(self):
        self.res_list_widget.clear()
        data = self.db_manager.get_reservations(self.user_id)
        if data:
            for row in data:
                item_text = f"ID: {row[0]} | Room {row[1]} | {row[2]} | {row[3]}-{row[4]}"
                if row[5] == "cancelled": item_text += " (CANCELLED)"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, row[0])
                if row[5] == "cancelled":
                    item.setForeground(QColor("#a0aec0"))
                self.res_list_widget.addItem(item)
        self.update_user_info_label()

    def open_reservation(self):
        try:
            self.res_win = ReservationScreen(self.user_id)
            self.active_windows.append(self.res_win)
            self.res_win.show()
            self.res_win.setAttribute(Qt.WA_DeleteOnClose)
            self.res_win.destroyed.connect(self.load_reservations)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def cancel_selected(self):
        item = self.res_list_widget.currentItem()
        if item and "(CANCELLED)" not in item.text():
            if QMessageBox.question(self, "Confirm", "Cancel this?") == QMessageBox.Yes:
                res = self.db_manager.cancel_reservation(item.data(Qt.UserRole))
                QMessageBox.information(self, "Result", res)
                self.load_reservations()

    def handle_logout(self):
        if QMessageBox.question(self, "Logout", "Logout?") == QMessageBox.Yes: self.force_logout()

    def force_logout(self):
        main_win = self.window()
        if hasattr(main_win, 'setCurrentIndex'):
            main_win.setCurrentIndex(0)
            main_win.resize(550, 350)
        else: self.close()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Main(user_id=22212345678) 
    window.show()
    sys.exit(app.exec_())