"""
Polished Login Dialog for Chemical Equipment Visualizer.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, pyqtProperty, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QRadialGradient, QBrush


class LoginThread(QThread):
    """Background thread for login to prevent UI blocking."""
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, username, password):
        super().__init__()
        self.api_client = api_client
        self.username = username
        self.password = password
    
    def run(self):
        try:
            data = self.api_client.login(self.username, self.password)
            self.success.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class GlassRippleButton(QPushButton):
    """Glassy button with ripple effect."""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._ripple_radius = 0
        self._ripple_opacity = 0
        self._ripple_pos = QPoint(0, 0)
        
        # Ripple animation
        self._radius_anim = QPropertyAnimation(self, b"ripple_radius")
        self._radius_anim.setDuration(400)
        self._radius_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self._opacity_anim = QPropertyAnimation(self, b"ripple_opacity")
        self._opacity_anim.setDuration(400)
        self._opacity_anim.setEasingCurve(QEasingCurve.OutCubic)
    
    @pyqtProperty(int)
    def ripple_radius(self):
        return self._ripple_radius
    
    @ripple_radius.setter
    def ripple_radius(self, value):
        self._ripple_radius = value
        self.update()
    
    @pyqtProperty(int)
    def ripple_opacity(self):
        return self._ripple_opacity
    
    @ripple_opacity.setter
    def ripple_opacity(self, value):
        self._ripple_opacity = value
        self.update()
    
    def mousePressEvent(self, event):
        self._ripple_pos = event.pos()
        max_radius = max(self.width(), self.height()) * 1.5
        
        self._radius_anim.setStartValue(0)
        self._radius_anim.setEndValue(int(max_radius))
        
        self._opacity_anim.setStartValue(120)
        self._opacity_anim.setEndValue(0)
        
        self._radius_anim.start()
        self._opacity_anim.start()
        
        super().mousePressEvent(event)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self._ripple_opacity > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Radial gradient for ripple
            gradient = QRadialGradient(self._ripple_pos, self._ripple_radius)
            ripple_color = QColor(255, 255, 255, self._ripple_opacity)
            gradient.setColorAt(0, ripple_color)
            gradient.setColorAt(0.7, QColor(255, 255, 255, self._ripple_opacity // 2))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 10, 10)
            painter.end()


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
        self.setFixedSize(450, 560)
        
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
            QLineEdit::placeholder {
                color: #7070a0;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
            }
            QPushButton#loginBtn {
                padding: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(124, 58, 237, 240), 
                    stop:0.3 rgba(167, 139, 250, 200),
                    stop:0.7 rgba(139, 92, 246, 220),
                    stop:1 rgba(109, 40, 217, 240));
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 12px;
                color: white;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton#loginBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(139, 92, 246, 255), 
                    stop:0.5 rgba(192, 168, 255, 230),
                    stop:1 rgba(124, 58, 237, 255));
                border: 1px solid rgba(255, 255, 255, 120);
            }
            QPushButton#loginBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(91, 33, 182, 255), 
                    stop:1 rgba(109, 40, 217, 255));
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(36, 36, 36, 32)
        
        # Icon
        icon = QLabel("⚗️")
        icon.setFont(QFont("Segoe UI Emoji", 40))
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)
        
        card_layout.addSpacing(4)
        
        # Title
        title = QLabel("Chemical Equipment")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        card_layout.addWidget(title)
        
        subtitle = QLabel("Visualizer")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 16, QFont.Bold))
        subtitle.setStyleSheet("color: #a78bfa;")
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(24)
        
        # Username label
        user_label = QLabel("Username")
        user_label.setStyleSheet("color: #b0b0c0; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(user_label)
        
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username")
        self.username.setMinimumHeight(50)
        card_layout.addWidget(self.username)
        
        card_layout.addSpacing(12)
        
        # Password label
        pass_label = QLabel("Password")
        pass_label.setStyleSheet("color: #b0b0c0; font-size: 13px; font-weight: 500;")
        card_layout.addWidget(pass_label)
        
        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(50)
        card_layout.addWidget(self.password)
        
        card_layout.addSpacing(20)
        
        # Login button
        self.login_btn = GlassRippleButton("Sign In")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.setMinimumHeight(52)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        card_layout.addSpacing(12)
        
        # Hint - make it more visible
        hint = QLabel("Demo credentials:  admin / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #8080a0; font-size: 12px;")
        card_layout.addWidget(hint)
        
        layout.addWidget(card)
        
        self.password.returnPressed.connect(self.handle_login)
        self.username.returnPressed.connect(self.password.setFocus)
    
    def handle_login(self):
        """Handle login using background thread."""
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password")
            return
        
        self.login_btn.setText("Signing in...")
        self.login_btn.setEnabled(False)
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        
        # Use background thread for login
        self.login_thread = LoginThread(self.api_client, username, password)
        self.login_thread.success.connect(self._on_login_success)
        self.login_thread.error.connect(self._on_login_error)
        self.login_thread.start()
    
    def _on_login_success(self, data):
        """Handle successful login."""
        self.user_data = data
        self.accept()
    
    def _on_login_error(self, error_msg):
        """Handle login error."""
        QMessageBox.critical(self, "Error", "Invalid credentials")
        self.login_btn.setText("Sign In")
        self.login_btn.setEnabled(True)
        self.username.setEnabled(True)
        self.password.setEnabled(True)

