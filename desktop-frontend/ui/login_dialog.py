"""
Polished Login Dialog for Chemical Equipment Visualizer.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LoginDialog(QDialog):
    """Modern login dialog."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        self.setWindowTitle("Login")
        self.setFixedSize(420, 480)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #0f0f1a;
            }
            QFrame#card {
                background-color: #16162a;
                border-radius: 16px;
                border: 1px solid #252545;
            }
            QLabel {
                color: #e0e0e0;
                background: transparent;
            }
            QLineEdit {
                padding: 14px 16px;
                background-color: #1e1e38;
                border: 1px solid #303055;
                border-radius: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
            }
            QPushButton#loginBtn {
                padding: 14px;
                background-color: #7c3aed;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#loginBtn:hover {
                background-color: #6d28d9;
            }
            QPushButton#loginBtn:pressed {
                background-color: #5b21b6;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(32, 40, 32, 36)
        
        # Icon
        icon = QLabel("⚗️")
        icon.setFont(QFont("Segoe UI Emoji", 44))
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)
        
        # Title
        title = QLabel("Chemical Equipment\nVisualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #ffffff; line-height: 1.4;")
        card_layout.addWidget(title)
        
        card_layout.addSpacing(20)
        
        # Username label
        user_label = QLabel("Username")
        user_label.setStyleSheet("color: #9090a0; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(user_label)
        
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setMinimumHeight(48)
        card_layout.addWidget(self.username)
        
        card_layout.addSpacing(4)
        
        # Password label
        pass_label = QLabel("Password")
        pass_label.setStyleSheet("color: #9090a0; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(pass_label)
        
        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(48)
        card_layout.addWidget(self.password)
        
        card_layout.addSpacing(16)
        
        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        # Hint
        hint = QLabel("Demo: admin / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #505070; font-size: 11px; margin-top: 12px;")
        card_layout.addWidget(hint)
        
        layout.addWidget(card)
        
        self.password.returnPressed.connect(self.handle_login)
        self.username.returnPressed.connect(self.password.setFocus)
    
    def handle_login(self):
        """Handle login."""
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password")
            return
        
        try:
            self.login_btn.setText("Signing in...")
            self.login_btn.setEnabled(False)
            self.user_data = self.api_client.login(username, password)
            self.accept()
        except:
            QMessageBox.critical(self, "Error", "Invalid credentials")
        finally:
            self.login_btn.setText("Sign In")
            self.login_btn.setEnabled(True)
