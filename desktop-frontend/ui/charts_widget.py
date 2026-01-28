"""
Polished Charts Widget for Chemical Equipment Visualizer.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ChartsWidget(QWidget):
    """Widget with polished Matplotlib charts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment = []
        self.summary = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Data Visualization")
        title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 600;")
        layout.addWidget(title)
        
        # Charts
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Bar chart card
        bar_card = QFrame()
        bar_card.setStyleSheet("""
            QFrame {
                background-color: #16162a;
                border: 1px solid #252545;
                border-radius: 12px;
            }
        """)
        bar_layout = QVBoxLayout(bar_card)
        bar_layout.setContentsMargins(20, 16, 20, 20)
        bar_layout.setSpacing(12)
        
        bar_title = QLabel("Flowrate & Pressure by Equipment")
        bar_title.setStyleSheet("color: #8080a0; font-size: 13px; font-weight: 500;")
        bar_layout.addWidget(bar_title)
        
        self.bar_figure = Figure(figsize=(7, 4), facecolor='#16162a')
        self.bar_canvas = FigureCanvas(self.bar_figure)
        bar_layout.addWidget(self.bar_canvas)
        
        charts_layout.addWidget(bar_card, 3)
        
        # Pie chart card
        pie_card = QFrame()
        pie_card.setStyleSheet("""
            QFrame {
                background-color: #16162a;
                border: 1px solid #252545;
                border-radius: 12px;
            }
        """)
        pie_layout = QVBoxLayout(pie_card)
        pie_layout.setContentsMargins(20, 16, 20, 20)
        pie_layout.setSpacing(12)
        
        pie_title = QLabel("Equipment Type Distribution")
        pie_title.setStyleSheet("color: #8080a0; font-size: 13px; font-weight: 500;")
        pie_layout.addWidget(pie_title)
        
        self.pie_figure = Figure(figsize=(4, 4), facecolor='#16162a')
        self.pie_canvas = FigureCanvas(self.pie_figure)
        pie_layout.addWidget(self.pie_canvas)
        
        charts_layout.addWidget(pie_card, 2)
        
        layout.addLayout(charts_layout)
        
        plt.style.use('dark_background')
    
    def update_data(self, equipment: list, summary: dict):
        """Update with new data."""
        self.equipment = equipment
        self.summary = summary
        self.draw_bar()
        self.draw_pie()
    
    def draw_bar(self):
        """Draw bar chart."""
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data available\nUpload a CSV to see charts', 
                   ha='center', va='center', color='#606080', fontsize=12,
                   multialignment='center')
            ax.axis('off')
            self.bar_canvas.draw()
            return
        
        data = self.equipment[:10]
        names = [eq.get('name', '')[:12] for eq in data]
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in data]
        pressures = [float(eq.get('pressure', 0) or 0) for eq in data]
        
        x = range(len(names))
        w = 0.35
        
        ax.bar([i - w/2 for i in x], flowrates, w, label='Flowrate', color='#7c3aed', alpha=0.9)
        ax.bar([i + w/2 for i in x], pressures, w, label='Pressure', color='#8b5cf6', alpha=0.9)
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9, color='#8080a0')
        ax.tick_params(colors='#606080', labelsize=9)
        ax.legend(loc='upper right', facecolor='#1e1e38', edgecolor='#303050', 
                 labelcolor='#e0e0e0', fontsize=9)
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        ax.grid(True, alpha=0.15, color='#ffffff', linestyle='-')
        ax.set_axisbelow(True)
        
        self.bar_figure.tight_layout(pad=1.5)
        self.bar_canvas.draw()
    
    def draw_pie(self):
        """Draw pie chart."""
        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        dist = self.summary.get('type_distribution', {})
        
        if not dist:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                   color='#606080', fontsize=12)
            ax.axis('off')
            self.pie_canvas.draw()
            return
        
        labels = list(dist.keys())
        sizes = list(dist.values())
        colors = ['#7c3aed', '#8b5cf6', '#059669', '#f59e0b', '#ef4444', '#06b6d4']
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors[:len(labels)],
            autopct='%1.0f%%',
            startangle=90,
            textprops={'color': '#e0e0e0', 'fontsize': 10},
            wedgeprops={'edgecolor': '#16162a', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('#16162a')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        self.pie_figure.tight_layout(pad=1)
        self.pie_canvas.draw()
