"""
Login/Register Dialog with Sliding Animation for Chemical Equipment Visualizer.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QFrame, QStackedWidget, QWidget, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, pyqtProperty, 
    QThread, pyqtSignal, QParallelAnimationGroup, QRect
)
from PyQt5.QtGui import QFont, QPainter, QColor, QRadialGradient, QBrush


class AuthThread(QThread):
    """Background thread for authentication to prevent UI blocking."""
    success = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, action, **kwargs):
        super().__init__()
        self.api_client = api_client
        self.action = action  # 'login' or 'register'
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.action == 'login':
                data = self.api_client.login(
                    self.kwargs['username'], 
                    self.kwargs['password']
                )
            else:
                data = self.api_client.register(
                    self.kwargs['username'],
                    self.kwargs['email'],
                    self.kwargs['password'],
                    self.kwargs['confirm_password']
                )
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
    """Modern login/register dialog with sliding animation."""
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        self.is_signup_mode = False
        
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI with sliding panels."""
        self.setWindowTitle("Login")
        self.setFixedSize(450, 620)
        
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(15, 15, 26, 220);
                border-radius: 16px;
            }
            QFrame#card {
                background-color: rgba(22, 22, 42, 230);
                border-radius: 16px;
                border: 1px solid #252545;
            }
            QLabel {
                color: #e0e0e0;
                background: transparent;
            }
            QLineEdit {
                padding: 12px 14px;
                background-color: rgba(30, 30, 56, 230);
                border: 1px solid #303055;
                border-radius: 10px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit::placeholder {
                color: #7070a0;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
            }
            QPushButton#primaryBtn {
                padding: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(124, 58, 237, 240), 
                    stop:0.3 rgba(167, 139, 250, 200),
                    stop:0.7 rgba(139, 92, 246, 220),
                    stop:1 rgba(109, 40, 217, 240));
                border: 1px solid rgba(255, 255, 255, 80);
                border-radius: 12px;
                color: white;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton#primaryBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(139, 92, 246, 255), 
                    stop:0.5 rgba(192, 168, 255, 230),
                    stop:1 rgba(124, 58, 237, 255));
            }
            QPushButton#primaryBtn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(91, 33, 182, 255), 
                    stop:1 rgba(109, 40, 217, 255));
            }
            QPushButton#linkBtn {
                background: transparent;
                border: none;
                color: #a78bfa;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton#linkBtn:hover {
                color: #c4b5fd;
                text-decoration: underline;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Card container
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(32, 28, 32, 24)
        
        # Icon
        icon = QLabel("⚗️")
        icon.setFont(QFont("Segoe UI Emoji", 36))
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)
        
        # Title (will change based on mode)
        self.title_label = QLabel("Chemical Equipment")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title_label.setStyleSheet("color: #ffffff;")
        card_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Visualizer")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.subtitle_label.setStyleSheet("color: #a78bfa;")
        card_layout.addWidget(self.subtitle_label)
        
        card_layout.addSpacing(16)
        
        # Stacked widget for sliding animation
        self.stack = QStackedWidget()
        self.stack.setMinimumHeight(280)
        
        # Login page
        login_page = self._create_login_page()
        self.stack.addWidget(login_page)
        
        # Signup page
        signup_page = self._create_signup_page()
        self.stack.addWidget(signup_page)
        
        card_layout.addWidget(self.stack)
        
        # Toggle link
        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignCenter)
        
        self.toggle_text = QLabel("Don't have an account?")
        self.toggle_text.setStyleSheet("color: #8080a0; font-size: 12px;")
        toggle_layout.addWidget(self.toggle_text)
        
        self.toggle_btn = QPushButton("Sign Up")
        self.toggle_btn.setObjectName("linkBtn")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        toggle_layout.addWidget(self.toggle_btn)
        
        card_layout.addLayout(toggle_layout)
        
        # Demo hint (login only)
        self.demo_hint = QLabel("Demo: admin / admin123")
        self.demo_hint.setAlignment(Qt.AlignCenter)
        self.demo_hint.setStyleSheet("color: #606080; font-size: 11px;")
        card_layout.addWidget(self.demo_hint)
        
        layout.addWidget(card)
    
    def _create_login_page(self):
        """Create login form page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Username
        user_label = QLabel("Username")
        user_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(user_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setMinimumHeight(44)
        layout.addWidget(self.login_username)
        
        layout.addSpacing(6)
        
        # Password
        pass_label = QLabel("Password")
        pass_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(pass_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setMinimumHeight(44)
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)
        
        layout.addSpacing(12)
        
        # Login button
        self.login_btn = GlassRippleButton("Sign In")
        self.login_btn.setObjectName("primaryBtn")
        self.login_btn.setMinimumHeight(48)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        layout.addStretch()
        return page
    
    def _create_signup_page(self):
        """Create signup form page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Username
        user_label = QLabel("Username")
        user_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(user_label)
        
        self.signup_username = QLineEdit()
        self.signup_username.setPlaceholderText("Choose a username")
        self.signup_username.setMinimumHeight(40)
        layout.addWidget(self.signup_username)
        
        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(email_label)
        
        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Enter your email")
        self.signup_email.setMinimumHeight(40)
        layout.addWidget(self.signup_email)
        
        # Password
        pass_label = QLabel("Password")
        pass_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(pass_label)
        
        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Create a password")
        self.signup_password.setEchoMode(QLineEdit.Password)
        self.signup_password.setMinimumHeight(40)
        layout.addWidget(self.signup_password)
        
        # Confirm Password
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("color: #b0b0c0; font-size: 12px; font-weight: 500;")
        layout.addWidget(confirm_label)
        
        self.signup_confirm = QLineEdit()
        self.signup_confirm.setPlaceholderText("Confirm your password")
        self.signup_confirm.setEchoMode(QLineEdit.Password)
        self.signup_confirm.setMinimumHeight(40)
        self.signup_confirm.returnPressed.connect(self.handle_signup)
        layout.addWidget(self.signup_confirm)
        
        layout.addSpacing(8)
        
        # Signup button
        self.signup_btn = GlassRippleButton("Create Account")
        self.signup_btn.setObjectName("primaryBtn")
        self.signup_btn.setMinimumHeight(48)
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(self.signup_btn)
        
        return page
    
    def toggle_mode(self):
        """Toggle between login and signup with animation."""
        self.is_signup_mode = not self.is_signup_mode
        
        if self.is_signup_mode:
            self.stack.setCurrentIndex(1)
            self.title_label.setText("Create Account")
            self.subtitle_label.setText("Join us today")
            self.toggle_text.setText("Already have an account?")
            self.toggle_btn.setText("Sign In")
            self.demo_hint.hide()
            self.setFixedSize(450, 680)
        else:
            self.stack.setCurrentIndex(0)
            self.title_label.setText("Chemical Equipment")
            self.subtitle_label.setText("Visualizer")
            self.toggle_text.setText("Don't have an account?")
            self.toggle_btn.setText("Sign Up")
            self.demo_hint.show()
            self.setFixedSize(450, 620)
    
    def handle_login(self):
        """Handle login."""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password")
            return
        
        self._set_loading(True, self.login_btn, "Signing in...")
        
        self.auth_thread = AuthThread(
            self.api_client, 'login',
            username=username, password=password
        )
        self.auth_thread.success.connect(self._on_success)
        self.auth_thread.error.connect(lambda e: self._on_error(e, self.login_btn, "Sign In"))
        self.auth_thread.start()
    
    def handle_signup(self):
        """Handle signup."""
        username = self.signup_username.text().strip()
        email = self.signup_email.text().strip()
        password = self.signup_password.text().strip()
        confirm = self.signup_confirm.text().strip()
        
        if not all([username, email, password, confirm]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        
        self._set_loading(True, self.signup_btn, "Creating account...")
        
        self.auth_thread = AuthThread(
            self.api_client, 'register',
            username=username, email=email,
            password=password, confirm_password=confirm
        )
        self.auth_thread.success.connect(self._on_success)
        self.auth_thread.error.connect(lambda e: self._on_error(e, self.signup_btn, "Create Account"))
        self.auth_thread.start()
    
    def _set_loading(self, loading, btn, text):
        """Set loading state."""
        btn.setText(text)
        btn.setEnabled(not loading)
        
        # Disable all inputs
        for widget in [self.login_username, self.login_password, 
                       self.signup_username, self.signup_email,
                       self.signup_password, self.signup_confirm]:
            widget.setEnabled(not loading)
    
    def _on_success(self, data):
        """Handle successful auth."""
        self.user_data = data
        self.accept()
    
    def _on_error(self, error_msg, btn, original_text):
        """Handle auth error."""
        self._set_loading(False, btn, original_text)
        
        # Parse error message
        if "already exists" in error_msg.lower():
            QMessageBox.critical(self, "Error", "Username already exists")
        elif "already registered" in error_msg.lower():
            QMessageBox.critical(self, "Error", "Email already registered")
        else:
            QMessageBox.critical(self, "Error", "Authentication failed. Please try again.")
