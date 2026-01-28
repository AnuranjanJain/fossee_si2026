"""
Polished Main Window for Chemical Equipment Visualizer.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QMessageBox, QFrame, QListWidget, QListWidgetItem, QHeaderView, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from .charts_widget import ChartsWidget


class DataLoaderThread(QThread):
    """Background thread for loading data."""
    finished = pyqtSignal(list, dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, session_id=None):
        super().__init__()
        self.api_client = api_client
        self.session_id = session_id
    
    def run(self):
        try:
            equipment = self.api_client.get_equipment(self.session_id)
            summary = self.api_client.get_summary(self.session_id)
            self.finished.emit(equipment, summary)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Polished main window."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.equipment = []
        self.summary = {}
        self.current_session_id = None
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI."""
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1280, 850)
        
        # Modern dark theme with purple accents
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f1a;
            }
            QWidget {
                background-color: transparent;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
            }
            
            /* Tabs */
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #16162a;
                color: #8080a0;
                padding: 12px 28px;
                margin-right: 6px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #7c3aed;
                color: #ffffff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1e1e38;
                color: #c0c0d0;
            }
            
            /* Tables */
            QTableWidget {
                background-color: #16162a;
                border: 1px solid #252545;
                border-radius: 10px;
                gridline-color: #252545;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1e1e38;
            }
            QTableWidget::item:selected {
                background-color: #7c3aed;
            }
            QHeaderView::section {
                background-color: #1e1e38;
                color: #8080a0;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 12px;
            }
            
            /* Buttons */
            QPushButton {
                padding: 10px 20px;
                background-color: #7c3aed;
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #6d28d9;
            }
            QPushButton:pressed {
                background-color: #5b21b6;
            }
            QPushButton:disabled {
                background-color: #303050;
                color: #606080;
            }
            
            /* List */
            QListWidget {
                background-color: #16162a;
                border: 1px solid #252545;
                border-radius: 10px;
            }
            QListWidget::item {
                padding: 14px 16px;
                border-bottom: 1px solid #1e1e38;
            }
            QListWidget::item:selected {
                background-color: #7c3aed;
            }
            QListWidget::item:hover:!selected {
                background-color: #1e1e38;
            }
            
            /* Scrollbar */
            QScrollBar:vertical {
                background: #16162a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #303050;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #404060;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_upload_tab(), "📤 Upload")
        self.tabs.addTab(self.create_data_tab(), "📊 Data")
        self.tabs.addTab(self.create_charts_tab(), "📈 Charts")
        self.tabs.addTab(self.create_history_tab(), "📜 History")
        layout.addWidget(self.tabs)
    
    def create_header(self):
        """Create header."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #16162a;
                border-radius: 12px;
                border: 1px solid #252545;
            }
        """)
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Logo
        logo = QLabel("⚗️ Chemical Equipment Visualizer")
        logo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        logo.setStyleSheet("color: #ffffff; border: none;")
        layout.addWidget(logo)
        
        layout.addStretch()
        
        # PDF button
        self.pdf_btn = QPushButton("📥 Download PDF")
        self.pdf_btn.setCursor(Qt.PointingHandCursor)
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        layout.addWidget(self.pdf_btn)
        
        # Logout
        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #303050;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background-color: #404060;
            }
        """)
        layout.addWidget(logout_btn)
        
        return header
    
    def create_upload_tab(self):
        """Create upload tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 20, 0, 0)
        
        # Upload card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #16162a;
                border: 2px dashed #303050;
                border-radius: 16px;
            }
            QFrame:hover {
                border-color: #7c3aed;
            }
        """)
        card.setMinimumHeight(300)
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)
        
        icon = QLabel("📁")
        icon.setFont(QFont("Segoe UI Emoji", 56))
        icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon)
        
        text = QLabel("Drop your CSV file here or click to browse")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color: #8080a0; font-size: 15px;")
        card_layout.addWidget(text)
        
        hint = QLabel("Format: Equipment Name, Type, Flowrate, Pressure, Temperature")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #505070; font-size: 12px;")
        card_layout.addWidget(hint)
        
        card_layout.addSpacing(12)
        
        self.upload_btn = QPushButton("Select CSV File")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setMinimumWidth(160)
        self.upload_btn.clicked.connect(self.select_file)
        card_layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)
        
        layout.addWidget(card)
        layout.addStretch()
        
        return tab
    
    def create_data_tab(self):
        """Create data tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(20)
        
        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_labels = {}
        stats = [
            ("total_count", "Total Equipment", "#7c3aed"),
            ("avg_flowrate", "Avg Flowrate", "#8b5cf6"),
            ("avg_pressure", "Avg Pressure", "#059669"),
            ("avg_temperature", "Avg Temperature", "#f59e0b"),
        ]
        
        for key, label_text, color in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #16162a;
                    border-radius: 12px;
                    border: 1px solid #252545;
                    border-left: 4px solid {color};
                }}
            """)
            card.setMinimumHeight(90)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)
            card_layout.setSpacing(6)
            
            label = QLabel(label_text)
            label.setStyleSheet("color: #8080a0; font-size: 12px; border: none;")
            card_layout.addWidget(label)
            
            value = QLabel("0")
            value.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold; border: none;")
            self.stat_labels[key] = value
            card_layout.addWidget(value)
            
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        
        # Table label
        table_label = QLabel("Equipment Data")
        table_label.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 600;")
        layout.addWidget(table_label)
        
        # Table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setShowGrid(False)
        layout.addWidget(self.data_table)
        
        return tab
    
    def create_charts_tab(self):
        """Create charts tab."""
        self.charts_widget = ChartsWidget()
        return self.charts_widget
    
    def create_history_tab(self):
        """Create history tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(16)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Upload History")
        title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 600;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        subtitle = QLabel("Last 5 uploads are saved")
        subtitle.setStyleSheet("color: #606080; font-size: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_click)
        layout.addWidget(self.history_list)
        
        return tab
    
    def load_data(self, session_id=None):
        """Load data."""
        self.loader = DataLoaderThread(self.api_client, session_id)
        self.loader.finished.connect(self.on_data_loaded)
        self.loader.error.connect(lambda e: None)
        self.loader.start()
        self.load_history()
    
    def on_data_loaded(self, equipment, summary):
        """Handle data."""
        self.equipment = equipment
        self.summary = summary
        self.update_ui()
    
    def update_ui(self):
        """Update UI."""
        # Stats
        for key, label in self.stat_labels.items():
            val = self.summary.get(key, 0)
            if val is None:
                val = 0
            if isinstance(val, float):
                label.setText(f"{val:.1f}")
            else:
                label.setText(str(val))
        
        # Table
        self.data_table.setRowCount(len(self.equipment))
        for row, eq in enumerate(self.equipment):
            self.data_table.setItem(row, 0, QTableWidgetItem(eq.get('name', '')))
            self.data_table.setItem(row, 1, QTableWidgetItem(eq.get('equipment_type', '')))
            self.data_table.setItem(row, 2, QTableWidgetItem(str(eq.get('flowrate', ''))))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(eq.get('pressure', ''))))
            self.data_table.setItem(row, 4, QTableWidgetItem(str(eq.get('temperature', ''))))
        
        self.charts_widget.update_data(self.equipment, self.summary)
    
    def load_history(self):
        """Load history."""
        try:
            history = self.api_client.get_history()
            self.history_list.clear()
            for s in history:
                date = s.get('uploaded_at', '')[:10]
                count = s.get('equipment_count', 0)
                item = QListWidgetItem(f"📄 {s['filename']}    •    {date}    •    {count} records")
                item.setData(Qt.UserRole, s['id'])
                self.history_list.addItem(item)
        except:
            pass
    
    def on_history_click(self, item):
        """Handle history click."""
        self.current_session_id = item.data(Qt.UserRole)
        self.load_data(self.current_session_id)
        self.tabs.setCurrentIndex(1)
    
    def select_file(self):
        """Select file."""
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if path:
            self.upload_file(path)
    
    def upload_file(self, path):
        """Upload file."""
        try:
            self.upload_btn.setText("Uploading...")
            self.upload_btn.setEnabled(False)
            
            result = self.api_client.upload_csv(path)
            QMessageBox.information(self, "Success", f"Uploaded {result.get('record_count', 0)} records!")
            
            self.current_session_id = result.get('session_id')
            self.load_data(self.current_session_id)
            self.tabs.setCurrentIndex(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.upload_btn.setText("Select CSV File")
            self.upload_btn.setEnabled(True)
    
    def download_pdf(self):
        """Download PDF."""
        try:
            self.pdf_btn.setText("Generating...")
            self.pdf_btn.setEnabled(False)
            
            data = self.api_client.download_pdf(self.current_session_id)
            path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "equipment_report.pdf", "PDF (*.pdf)")
            
            if path:
                with open(path, 'wb') as f:
                    f.write(data)
                QMessageBox.information(self, "Success", f"Report saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.pdf_btn.setText("📥 Download PDF")
            self.pdf_btn.setEnabled(True)
    
    def logout(self):
        """Logout."""
        self.api_client.logout()
        self.close()
