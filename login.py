from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import keyring
import webbrowser
from crypto_utils import encrypt_pin, decrypt_pin

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str, str)  # Signal to emit when login is successful (email, name)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - HSN Tax App")
        self.resize(400, 300)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("HSN Tax Calculator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Login or Sign Up to Continue")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email ID (Outlook.com)")
        self.email_input.setStyleSheet("padding: 8px;")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        
        # PIN input
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setStyleSheet("padding: 8px;")
        layout.addWidget(QLabel("PIN:"))
        layout.addWidget(self.pin_input)
        
        layout.addSpacing(10)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 8px;")
        layout.addWidget(self.login_btn)
        
        # Sign up button
        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setStyleSheet("background-color: #107c10; color: white; padding: 8px;")
        layout.addWidget(self.signup_btn)
        
        # Forgot PIN button
        self.forgot_btn = QPushButton("Forgot PIN")
        self.forgot_btn.setStyleSheet("color: #0078d4;")
        layout.addWidget(self.forgot_btn)
        
        # OneDrive login button
        self.onedrive_btn = QPushButton("Login with Microsoft OneDrive")
        self.onedrive_btn.setStyleSheet("background-color: #0078d4; color: white; padding: 8px;")
        layout.addWidget(self.onedrive_btn)
        
        self.setLayout(layout)
        
        # Connect signals
        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)
        self.forgot_btn.clicked.connect(self.forgot_pin)
        self.onedrive_btn.clicked.connect(self.onedrive_login)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(240, 240, 240))  # Light gray background
        painter.drawRect(self.rect())
        
        # Draw header
        header_rect = self.rect().adjusted(0, 0, 0, -self.height() + 60)
        painter.setBrush(QColor(0, 120, 212))  # Microsoft blue
        painter.drawRect(header_rect)
        
        # Draw header text
        painter.setPen(Qt.white)
        painter.drawText(header_rect, Qt.AlignCenter, "HSN Tax Calculator")
        
    def login(self):
        email = self.email_input.text()
        pin = self.pin_input.text()
        
        if not email or not pin:
            QMessageBox.warning(self, "Error", "Please enter email and PIN")
            return
            
        try:
            stored_pin = keyring.get_password("HSNApp", email)
            if stored_pin and decrypt_pin(stored_pin) == pin:
                keyring.set_password("HSNApp", "current_user", email)
                QMessageBox.information(self, "Success", "Login successful!")
                self.login_successful.emit(email, email.split('@')[0])
            else:
                QMessageBox.critical(self, "Error", "Invalid credentials.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
            
    def signup(self):
        email = self.email_input.text()
        pin = self.pin_input.text()
        
        if not email or not pin:
            QMessageBox.warning(self, "Error", "Please enter email and PIN")
            return
            
        if len(pin) != 4 or not pin.isdigit():
            QMessageBox.warning(self, "Error", "PIN must be 4 digits")
            return
            
        try:
            # Check if user already exists
            if keyring.get_password("HSNApp", email):
                QMessageBox.warning(self, "Error", "User already exists")
                return
                
            # Store encrypted PIN
            keyring.set_password("HSNApp", email, encrypt_pin(pin))
            keyring.set_password("HSNApp", "current_user", email)
            
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.login_successful.emit(email, email.split('@')[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")
            
    def forgot_pin(self):
        email = self.email_input.text()
        
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your email")
            return
            
        if keyring.get_password("HSNApp", email):
            # In a real app, you would send a reset email
            # For this demo, we'll just reset the PIN
            try:
                keyring.delete_password("HSNApp", email)
                QMessageBox.information(self, "PIN Reset", "Your PIN has been reset. Please sign up again.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"PIN reset failed: {str(e)}")
        else:
            QMessageBox.warning(self, "Not Found", "Email not found. Please Sign Up.")
            
    def onedrive_login(self):
        # Open Microsoft login page
        webbrowser.open("https://login.microsoftonline.com/common/oauth2/v2.0/authorize")
        QMessageBox.information(self, "Microsoft Login", "Please sign in with your Microsoft account in the browser.")
        
        # In a real app, you would implement OAuth flow
        # For this demo, we'll just simulate a successful login
        email = self.email_input.text() or "user@outlook.com"
        keyring.set_password("HSNApp", "current_user", email)
        self.login_successful.emit(email, email.split('@')[0])