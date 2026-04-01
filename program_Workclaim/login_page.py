import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QStackedWidget,
    QFormLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt

# Veritabanı fonksiyonları için veritabanı sınıfı içe aktarılıyor
from database_functions import Database
db = Database()


# Çeşitli yerlerde kullanılan stil ve renklerin tanımları
BG_COLOR = "#f8f9fa"
TITLE_STYLE = "font-size: 22px; color: #2c3e50; font-family: 'Segoe UI', Arial; background-color: transparent;"
LABEL_STYLE = "font-size: 14px; color: #495057; background-color: transparent"
INPUT_STYLE = """
    QLineEdit {
        padding: 6px;
        border: 1px solid #ced4da;
        border-radius: 4px;
        background-color: white;
        font-size: 14px;
    }
"""
PRIMARY_BTN = """
    QPushButton {
        background-color: #2b6cb0;
        color: white;
        padding: 10px 20px;
        font-size: 14px;
        border: none;
        border-radius: 4px;
    }
    QPushButton:hover { background-color: #2c5282; }
"""
SECONDARY_BTN = """
    QPushButton {
        background-color: #e2e8f0;
        color: #4a5568;
        padding: 10px 20px;
        font-size: 14px;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
    }
    QPushButton:hover { background-color: #cbd5e0; }
"""


# Giriş sayfası
class LoginPage(QWidget):
    def __init__(self, switch_to_signup, login_success):
        super().__init__()
        self.switch_to_signup = switch_to_signup
        self.login_success = login_success
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {BG_COLOR};")

        # Ana düzen
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Başlık
        title = QLabel("WORKCLAIM - LOGIN")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Form düzeni
        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        # ID ve şifre giriş alanları
        self.user_id = QLineEdit()
        self.user_id.setPlaceholderText("User ID")
        self.user_id.setStyleSheet(INPUT_STYLE)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(INPUT_STYLE)

        # ID ve şifre alanlarının başlıkları
        user_label = QLabel("User ID:")
        user_label.setStyleSheet(LABEL_STYLE)

        pass_label = QLabel("Password:")
        pass_label.setStyleSheet(LABEL_STYLE)

        # Alanlar form düzenine burada ekleniyor
        form_layout.addRow(user_label, self.user_id)
        form_layout.addRow(pass_label, self.password)

        main_layout.addLayout(form_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e9ecef;")
        main_layout.addWidget(line)

        # Giriş ve kayıt sayfası butonları
        button_layout = QHBoxLayout()

        self.login_btn = QPushButton("Enter")
        self.login_btn.setStyleSheet(PRIMARY_BTN)

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setStyleSheet(SECONDARY_BTN)

        self.login_btn.clicked.connect(self.handle_login)
        self.signup_btn.clicked.connect(self.switch_to_signup)

        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.signup_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Veritabanına giriş kontrolü yapan fonksiyon
    def handle_login(self):
        uid = self.user_id.text()
        pw = self.password.text()

        if db.login_user(uid, pw):
            self.login_success(uid)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")


# Kaydol sayfası
class SignupPage(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {BG_COLOR};")

        # Ana düzen
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Başlık
        title = QLabel("WORKCLAIM - SIGN UP")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Form düzeni
        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        # ID, ad ve şifre giriş alanları
        self.user_id = QLineEdit()
        self.user_id.setPlaceholderText("User ID")
        self.user_id.setStyleSheet(INPUT_STYLE)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet(INPUT_STYLE)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(INPUT_STYLE)

        # ID, ad ve şifre alanlarının başlıkları
        user_label = QLabel("User ID:")
        user_label.setStyleSheet(LABEL_STYLE)

        username_label = QLabel("Username:")
        username_label.setStyleSheet(LABEL_STYLE)

        password_label = QLabel("Password:")
        password_label.setStyleSheet(LABEL_STYLE)

        # Alanlar form düzenine burada ekleniyor
        form_layout.addRow(user_label, self.user_id)
        form_layout.addRow(username_label, self.username)
        form_layout.addRow(password_label, self.password)

        main_layout.addLayout(form_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e9ecef;")
        main_layout.addWidget(line)

        # Kayıt ve giriş sayfası butonları
        button_layout = QHBoxLayout()

        self.signup_btn = QPushButton("Register")
        self.signup_btn.setStyleSheet(PRIMARY_BTN)

        self.login_btn = QPushButton("Back to Login")
        self.login_btn.setStyleSheet(SECONDARY_BTN)

        self.signup_btn.clicked.connect(self.handle_signup)
        self.login_btn.clicked.connect(self.switch_to_login)

        button_layout.addWidget(self.signup_btn)
        button_layout.addWidget(self.login_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    # Veritabanına kayıt işlem fonksiyonu
    def handle_signup(self):
        uid = self.user_id.text()
        uname = self.username.text()
        pw = self.password.text()

        result = db.register_user(uid, uname, pw)
        QMessageBox.information(self, "Info", result)


# Kabul sayfası (Yer tutucu, asıl kullanım sayfasına yönlendirilmesi lazım)
class HomePage(QWidget):
    def __init__(self, logout_func):
        super().__init__()
        self.logout_func = logout_func
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"background-color: {BG_COLOR};")

        # Ana düzen
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(20)

        # Başlık ve Rol
        self.label = QLabel("Logged in")
        self.label.setStyleSheet(TITLE_STYLE)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.role_label = QLabel("")
        self.role_label.setStyleSheet(LABEL_STYLE)
        self.role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e9ecef;")

        # Çıkış butonu
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet(PRIMARY_BTN)
        self.logout_btn.clicked.connect(self.logout_func)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.role_label)
        self.main_layout.addWidget(line)
        self.main_layout.addWidget(self.logout_btn)

        self.setLayout(self.main_layout)

    # Kullanıcı bilgilerini başlık ve role yükleyen fonksiyon
    def load_user(self, user_id):
        user = db.get_user(user_id)

        if user:
            uid, uname, role = user

            role_map = {
                1: "Student",
                2: "Teacher",
                3: "Administrator"
            }

            role_text = role_map.get(role, "Unknown")

            self.label.setText(f"Welcome {uname}")
            self.role_label.setText(f"Role: {role_text}")


# Asıl (Main) pencere, sayfalar arası geçişi yönetiyor
class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_page = LoginPage(self.show_signup, self.login_success)
        self.signup_page = SignupPage(self.show_login)
        self.home_page = HomePage(self.logout)

        self.addWidget(self.login_page)
        self.addWidget(self.signup_page)
        self.addWidget(self.home_page)

        self.setCurrentWidget(self.login_page)

    def show_signup(self):
        self.setCurrentWidget(self.signup_page)

    def show_login(self):
        self.setCurrentWidget(self.login_page)

    def login_success(self, user_id):
        self.home_page.load_user(user_id)
        self.setCurrentWidget(self.home_page)

    def logout(self):
        self.setCurrentWidget(self.login_page)


app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("WorkClaim")
window.resize(550, 350)
window.show()
sys.exit(app.exec_())