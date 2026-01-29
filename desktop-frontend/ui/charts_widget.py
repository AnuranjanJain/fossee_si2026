"""
Enhanced Charts Widget for Chemical Equipment Visualizer.
Includes: Bar charts, Pie charts, Scatter plots, Box plots, Correlation heatmap, and Statistics.
Supports mouse scroll zoom on correlation and comparison charts.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QGridLayout, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class ChartsWidget(QWidget):
    """Enhanced widget with multiple chart types and analytics."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.equipment = []
        self.summary = {}
        self._zoom_connections = []  # Store zoom event connections
        self._tabs_rendered = [False, False, False, False]  # Track which tabs have been rendered
        self._data_pending = False  # Track if data update is pending
        self.setup_ui()
        self._setup_zoom_handlers()
        # Connect tab change for lazy loading
        self.tabs.currentChanged.connect(self._on_tab_changed)
    
    def setup_ui(self):
        """Setup UI with tabs for different chart categories."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("📊 Data Analytics & Visualization")
        title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 600;")
        layout.addWidget(title)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #16162a;
                color: #8080a0;
                padding: 10px 20px;
                margin-right: 4px;
                border-radius: 8px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #7c3aed;
                color: #ffffff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1e1e38;
            }
        """)
        
        # Tab 1: Overview (Stats + Pie + Bar)
        self.tabs.addTab(self.create_overview_tab(), "Overview")
        
        # Tab 2: Correlations (Scatter + Heatmap)
        self.tabs.addTab(self.create_correlation_tab(), "Correlations")
        
        # Tab 3: Distributions (Box plots + Histograms)
        self.tabs.addTab(self.create_distribution_tab(), "Distributions")
        
        # Tab 4: Comparison (Radar + Rankings)
        self.tabs.addTab(self.create_comparison_tab(), "Comparison")
        
        layout.addWidget(self.tabs)
        
        plt.style.use('dark_background')
    
    def create_card(self, title_text):
        """Create a styled card frame."""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #16162a;
                border: 1px solid #252545;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 16)
        card_layout.setSpacing(10)
        
        title = QLabel(title_text)
        title.setStyleSheet("color: #a0a0c0; font-size: 12px; font-weight: 500; border: none;")
        card_layout.addWidget(title)
        
        return card, card_layout
    
    def create_overview_tab(self):
        """Create overview tab with stats and main charts."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # Statistics row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        
        self.stat_cards = {}
        stats_config = [
            ("count", "Total Equipment", "#7c3aed", "🔧"),
            ("avg_flow", "Avg Flowrate", "#8b5cf6", "💧"),
            ("max_pressure", "Max Pressure", "#059669", "⚡"),
            ("avg_temp", "Avg Temperature", "#f59e0b", "🌡️"),
            ("efficiency", "Efficiency Score", "#06b6d4", "📈"),
        ]
        
        for key, label, color, icon in stats_config:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #16162a;
                    border-radius: 10px;
                    border-left: 4px solid {color};
                }}
            """)
            card.setMinimumHeight(80)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            
            header = QLabel(f"{icon} {label}")
            header.setStyleSheet("color: #8080a0; font-size: 11px;")
            card_layout.addWidget(header)
            
            value_label = QLabel("--")
            value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
            self.stat_cards[key] = value_label
            card_layout.addWidget(value_label)
            
            stats_layout.addWidget(card)
        
        layout.addLayout(stats_layout)
        
        # Charts row
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)
        
        # Bar chart
        bar_card, bar_layout = self.create_card("Flowrate & Pressure by Equipment")
        self.bar_figure = Figure(figsize=(6, 3.5), facecolor='#16162a')
        self.bar_canvas = FigureCanvas(self.bar_figure)
        bar_layout.addWidget(self.bar_canvas)
        charts_layout.addWidget(bar_card, 3)
        
        # Pie chart
        pie_card, pie_layout = self.create_card("Equipment Type Distribution")
        self.pie_figure = Figure(figsize=(3.5, 3.5), facecolor='#16162a')
        self.pie_canvas = FigureCanvas(self.pie_figure)
        pie_layout.addWidget(self.pie_canvas)
        charts_layout.addWidget(pie_card, 2)
        
        layout.addLayout(charts_layout)
        
        return widget
    
    def create_correlation_tab(self):
        """Create correlation analysis tab."""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setSpacing(8)
        
        # Zoom hint
        hint = QLabel("🔍 Scroll to zoom • Double-click to reset")
        hint.setStyleSheet("color: #606080; font-size: 11px;")
        main_layout.addWidget(hint)
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)
        
        # Scatter plot
        scatter_card, scatter_layout = self.create_card("Temperature vs Flowrate Correlation")
        self.scatter_figure = Figure(figsize=(5, 4), facecolor='#16162a')
        self.scatter_canvas = FigureCanvas(self.scatter_figure)
        scatter_layout.addWidget(self.scatter_canvas)
        charts_layout.addWidget(scatter_card)
        
        # Heatmap
        heatmap_card, heatmap_layout = self.create_card("Parameter Correlation Matrix")
        self.heatmap_figure = Figure(figsize=(4, 4), facecolor='#16162a')
        self.heatmap_canvas = FigureCanvas(self.heatmap_figure)
        heatmap_layout.addWidget(self.heatmap_canvas)
        charts_layout.addWidget(heatmap_card)
        
        main_layout.addLayout(charts_layout)
        
        return widget
    
    def create_distribution_tab(self):
        """Create distribution analysis tab."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(16)
        
        # Box plot
        box_card, box_layout = self.create_card("Parameter Distribution by Equipment Type")
        self.box_figure = Figure(figsize=(6, 4), facecolor='#16162a')
        self.box_canvas = FigureCanvas(self.box_figure)
        box_layout.addWidget(self.box_canvas)
        layout.addWidget(box_card, 3)
        
        # Histogram
        hist_card, hist_layout = self.create_card("Flowrate Distribution")
        self.hist_figure = Figure(figsize=(4, 4), facecolor='#16162a')
        self.hist_canvas = FigureCanvas(self.hist_figure)
        hist_layout.addWidget(self.hist_canvas)
        layout.addWidget(hist_card, 2)
        
        return widget
    
    def create_comparison_tab(self):
        """Create equipment comparison tab."""
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setSpacing(8)
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)
        
        # Radar chart
        radar_card, radar_layout = self.create_card("Top Equipment Multi-Parameter Comparison")
        self.radar_figure = Figure(figsize=(5, 4), facecolor='#16162a')
        self.radar_canvas = FigureCanvas(self.radar_figure)
        radar_layout.addWidget(self.radar_canvas)
        charts_layout.addWidget(radar_card)
        
        # Rankings
        rank_card, rank_layout = self.create_card("Equipment Rankings")
        self.rank_figure = Figure(figsize=(4, 4), facecolor='#16162a')
        self.rank_canvas = FigureCanvas(self.rank_figure)
        rank_layout.addWidget(self.rank_canvas)
        charts_layout.addWidget(rank_card)
        
        main_layout.addLayout(charts_layout)
        
        return widget
    
    def _setup_zoom_handlers(self):
        """Setup mouse scroll zoom for correlation charts only."""
        # Connect scroll events to zoomable canvases (correlation tab only)
        zoomable_canvases = [
            (self.scatter_canvas, self.scatter_figure),
            (self.heatmap_canvas, self.heatmap_figure),
        ]
        
        for canvas, figure in zoomable_canvases:
            # Scroll to zoom
            cid = canvas.mpl_connect('scroll_event', 
                lambda event, fig=figure, can=canvas: self._on_scroll_zoom(event, fig, can))
            self._zoom_connections.append((canvas, cid))
            
            # Double-click to reset
            cid2 = canvas.mpl_connect('button_press_event',
                lambda event, fig=figure, can=canvas: self._on_double_click_reset(event, fig, can))
            self._zoom_connections.append((canvas, cid2))
    
    def _on_double_click_reset(self, event, figure, canvas):
        """Reset zoom on double-click."""
        if event.dblclick:
            for ax in figure.axes:
                ax.autoscale()
            figure.tight_layout(pad=1)
            canvas.draw_idle()
    
    def _on_scroll_zoom(self, event, figure, canvas):
        """Handle mouse scroll for zooming."""
        if event.inaxes is None:
            return
        
        ax = event.inaxes
        
        # Don't zoom polar plots (radar chart) - just return
        if hasattr(ax, 'name') and ax.name == 'polar':
            return
        
        # Zoom factor
        base_scale = 1.2
        
        if event.button == 'up':
            scale_factor = 1 / base_scale  # Zoom in
        elif event.button == 'down':
            scale_factor = base_scale  # Zoom out
        else:
            return
        
        # Get current axis limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        
        # Get the cursor position
        xdata = event.xdata
        ydata = event.ydata
        
        # Calculate new limits
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
        # Calculate relative position of cursor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        
        # Set new limits centered on cursor
        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        
        canvas.draw_idle()
    
    def reset_zoom(self, figure, canvas):
        """Reset zoom to original view."""
        for ax in figure.axes:
            ax.autoscale()
        figure.tight_layout(pad=1)
        canvas.draw_idle()
    
    def update_data(self, equipment: list, summary: dict):
        """Update charts with new data using lazy loading."""
        self.equipment = equipment
        self.summary = summary
        
        # Reset rendered state
        self._tabs_rendered = [False, False, False, False]
        self._data_pending = True
        
        # Always update stats immediately (they're lightweight)
        self.update_stats()
        
        # Only render the current visible tab immediately
        self._render_current_tab()
    
    def _on_tab_changed(self, index):
        """Handle tab change - render if not yet rendered."""
        if self._data_pending and not self._tabs_rendered[index]:
            self._render_tab(index)
    
    def _render_current_tab(self):
        """Render charts for the current tab."""
        current_idx = self.tabs.currentIndex()
        self._render_tab(current_idx)
    
    def _render_tab(self, index):
        """Render charts for a specific tab."""
        if self._tabs_rendered[index]:
            return
        
        self._tabs_rendered[index] = True
        
        if index == 0:  # Overview
            self.draw_bar()
            self.draw_pie()
        elif index == 1:  # Correlations
            self.draw_scatter()
            self.draw_heatmap()
        elif index == 2:  # Distributions
            self.draw_boxplot()
            self.draw_histogram()
        elif index == 3:  # Comparison
            self.draw_radar()
            self.draw_rankings()
    
    def update_stats(self):
        """Update statistics cards."""
        if not self.equipment:
            return
        
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in self.equipment]
        pressures = [float(eq.get('pressure', 0) or 0) for eq in self.equipment]
        temps = [float(eq.get('temperature', 0) or 0) for eq in self.equipment]
        
        self.stat_cards['count'].setText(str(len(self.equipment)))
        self.stat_cards['avg_flow'].setText(f"{np.mean(flowrates):.1f}")
        self.stat_cards['max_pressure'].setText(f"{np.max(pressures):.1f}")
        self.stat_cards['avg_temp'].setText(f"{np.mean(temps):.1f}°")
        
        # Calculate efficiency score (normalized composite)
        if flowrates and pressures:
            norm_flow = np.mean(flowrates) / max(flowrates) if max(flowrates) > 0 else 0
            norm_press = np.mean(pressures) / max(pressures) if max(pressures) > 0 else 0
            efficiency = (norm_flow + norm_press) / 2 * 100
            self.stat_cards['efficiency'].setText(f"{efficiency:.0f}%")
    
    def draw_bar(self):
        """Draw bar chart."""
        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                   color='#606080', fontsize=11)
            ax.axis('off')
            self.bar_canvas.draw()
            return
        
        data = self.equipment[:8]
        names = [eq.get('name', '')[:10] for eq in data]
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in data]
        pressures = [float(eq.get('pressure', 0) or 0) for eq in data]
        
        x = np.arange(len(names))
        w = 0.35
        
        ax.bar(x - w/2, flowrates, w, label='Flowrate', color='#7c3aed', alpha=0.9)
        ax.bar(x + w/2, pressures, w, label='Pressure', color='#06b6d4', alpha=0.9)
        
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8, color='#8080a0')
        ax.tick_params(colors='#606080', labelsize=8)
        ax.legend(loc='upper right', facecolor='#1e1e38', edgecolor='#303050', 
                 labelcolor='#e0e0e0', fontsize=8)
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        ax.grid(True, alpha=0.1, color='#ffffff', axis='y')
        
        self.bar_figure.tight_layout(pad=1)
        self.bar_canvas.draw()
    
    def draw_pie(self):
        """Draw pie chart."""
        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        dist = self.summary.get('type_distribution', {})
        
        if not dist:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.pie_canvas.draw()
            return
        
        labels = list(dist.keys())
        sizes = list(dist.values())
        colors = ['#7c3aed', '#8b5cf6', '#059669', '#f59e0b', '#ef4444', '#06b6d4']
        
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors[:len(labels)],
            autopct='%1.0f%%', startangle=90,
            textprops={'color': '#e0e0e0', 'fontsize': 9},
            wedgeprops={'edgecolor': '#16162a', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('#16162a')
            autotext.set_fontweight('bold')
        
        self.pie_figure.tight_layout(pad=0.5)
        self.pie_canvas.draw()
    
    def draw_scatter(self):
        """Draw scatter plot showing correlation."""
        self.scatter_figure.clear()
        ax = self.scatter_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.scatter_canvas.draw()
            return
        
        temps = [float(eq.get('temperature', 0) or 0) for eq in self.equipment]
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in self.equipment]
        pressures = [float(eq.get('pressure', 0) or 0) for eq in self.equipment]
        
        # Size based on pressure
        sizes = [p * 8 for p in pressures]
        
        scatter = ax.scatter(temps, flowrates, s=sizes, c=pressures, 
                            cmap='viridis', alpha=0.7, edgecolors='white', linewidth=0.5)
        
        # Trend line
        if len(temps) > 1:
            z = np.polyfit(temps, flowrates, 1)
            p = np.poly1d(z)
            ax.plot(temps, p(temps), '--', color='#f59e0b', alpha=0.7, linewidth=2)
        
        ax.set_xlabel('Temperature', color='#8080a0', fontsize=10)
        ax.set_ylabel('Flowrate', color='#8080a0', fontsize=10)
        ax.tick_params(colors='#606080', labelsize=9)
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        
        # Colorbar
        cbar = self.scatter_figure.colorbar(scatter, ax=ax, shrink=0.8)
        cbar.set_label('Pressure', color='#8080a0', fontsize=9)
        cbar.ax.tick_params(colors='#606080', labelsize=8)
        
        self.scatter_figure.tight_layout(pad=1)
        self.scatter_canvas.draw()
    
    def draw_heatmap(self):
        """Draw correlation heatmap."""
        self.heatmap_figure.clear()
        ax = self.heatmap_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment or len(self.equipment) < 2:
            ax.text(0.5, 0.5, 'Need more data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.heatmap_canvas.draw()
            return
        
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in self.equipment]
        pressures = [float(eq.get('pressure', 0) or 0) for eq in self.equipment]
        temps = [float(eq.get('temperature', 0) or 0) for eq in self.equipment]
        
        data = np.array([flowrates, pressures, temps])
        corr = np.corrcoef(data)
        
        labels = ['Flowrate', 'Pressure', 'Temperature']
        im = ax.imshow(corr, cmap='RdYlGn', vmin=-1, vmax=1)
        
        ax.set_xticks(range(3))
        ax.set_yticks(range(3))
        ax.set_xticklabels(labels, fontsize=9, color='#8080a0')
        ax.set_yticklabels(labels, fontsize=9, color='#8080a0')
        
        # Add correlation values
        for i in range(3):
            for j in range(3):
                text_color = '#16162a' if abs(corr[i, j]) > 0.5 else '#e0e0e0'
                ax.text(j, i, f'{corr[i, j]:.2f}', ha='center', va='center', 
                       color=text_color, fontsize=10, fontweight='bold')
        
        self.heatmap_figure.colorbar(im, ax=ax, shrink=0.8)
        self.heatmap_figure.tight_layout(pad=1)
        self.heatmap_canvas.draw()
    
    def draw_boxplot(self):
        """Draw box plot by equipment type."""
        self.box_figure.clear()
        ax = self.box_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.box_canvas.draw()
            return
        
        # Group by type
        type_data = {}
        for eq in self.equipment:
            eq_type = eq.get('equipment_type', 'Other')
            if eq_type not in type_data:
                type_data[eq_type] = []
            type_data[eq_type].append(float(eq.get('flowrate', 0) or 0))
        
        if not type_data:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.box_canvas.draw()
            return
        
        # Shorten labels
        labels = [k[:6] for k in type_data.keys()]
        data = list(type_data.values())
        
        bp = ax.boxplot(data, labels=labels, patch_artist=True)
        
        colors = ['#7c3aed', '#8b5cf6', '#059669', '#f59e0b', '#ef4444', '#06b6d4']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        
        for element in ['whiskers', 'caps', 'medians']:
            for item in bp[element]:
                item.set_color('#e0e0e0')
        
        ax.set_ylabel('Flowrate', color='#a0a0c0', fontsize=9)
        ax.tick_params(colors='#606080', labelsize=8)
        plt.setp(ax.get_xticklabels(), rotation=0, ha='center', color='#a0a0c0', fontsize=8)
        ax.grid(True, alpha=0.1, axis='y', color='#ffffff')
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        
        self.box_figure.tight_layout(pad=1.2)
        self.box_canvas.draw()
    
    def draw_histogram(self):
        """Draw flowrate histogram with smooth look."""
        self.hist_figure.clear()
        ax = self.hist_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.hist_canvas.draw()
            return
        
        flowrates = [float(eq.get('flowrate', 0) or 0) for eq in self.equipment]
        
        # Better binning
        n_bins = min(10, max(5, len(flowrates) // 2))
        n, bins, patches = ax.hist(flowrates, bins=n_bins, color='#7c3aed', 
                                   alpha=0.85, edgecolor='#0f0f1a', linewidth=1.5,
                                   rwidth=0.85)
        
        # Gradient effect on bars
        for i, patch in enumerate(patches):
            brightness = 0.7 + (i / len(patches)) * 0.3
            patch.set_facecolor((0.486 * brightness, 0.227 * brightness, 0.929 * brightness, 0.9))
        
        # Add mean line
        mean_val = np.mean(flowrates)
        ax.axvline(mean_val, color='#f59e0b', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.0f}')
        
        ax.set_xlabel('Flowrate', color='#8080a0', fontsize=10)
        ax.set_ylabel('Count', color='#8080a0', fontsize=10)
        ax.tick_params(colors='#606080', labelsize=9)
        ax.legend(loc='upper right', facecolor='#1e1e38', edgecolor='#303050', 
                 labelcolor='#e0e0e0', fontsize=8)
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        
        self.hist_figure.tight_layout(pad=1)
        self.hist_canvas.draw()
    
    def draw_radar(self):
        """Draw radar chart for top equipment."""
        self.radar_figure.clear()
        
        if not self.equipment or len(self.equipment) < 2:
            ax = self.radar_figure.add_subplot(111)
            ax.set_facecolor('#16162a')
            ax.text(0.5, 0.5, 'Need more data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.radar_canvas.draw()
            return
        
        # Get top 3 equipment by flowrate
        sorted_eq = sorted(self.equipment, key=lambda x: float(x.get('flowrate', 0) or 0), reverse=True)[:3]
        
        categories = ['Flowrate', 'Pressure', 'Temperature']
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the loop
        
        ax = self.radar_figure.add_subplot(111, polar=True)
        ax.set_facecolor('#16162a')
        
        colors = ['#7c3aed', '#06b6d4', '#f59e0b']
        
        # Normalize values
        max_flow = max(float(eq.get('flowrate', 1) or 1) for eq in self.equipment)
        max_press = max(float(eq.get('pressure', 1) or 1) for eq in self.equipment)
        max_temp = max(float(eq.get('temperature', 1) or 1) for eq in self.equipment)
        
        for i, eq in enumerate(sorted_eq):
            values = [
                float(eq.get('flowrate', 0) or 0) / max_flow,
                float(eq.get('pressure', 0) or 0) / max_press,
                float(eq.get('temperature', 0) or 0) / max_temp
            ]
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, color=colors[i], label=eq.get('name', '')[:8])
            ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, color='#8080a0', fontsize=9)
        ax.tick_params(colors='#606080')
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1), facecolor='#1e1e38', 
                 edgecolor='#303050', labelcolor='#e0e0e0', fontsize=8)
        
        self.radar_figure.tight_layout(pad=1)
        self.radar_canvas.draw()
    
    def draw_rankings(self):
        """Draw horizontal bar chart rankings."""
        self.rank_figure.clear()
        ax = self.rank_figure.add_subplot(111)
        ax.set_facecolor('#16162a')
        
        if not self.equipment:
            ax.text(0.5, 0.5, 'No data', ha='center', va='center', color='#606080')
            ax.axis('off')
            self.rank_canvas.draw()
            return
        
        # Sort by flowrate
        sorted_eq = sorted(self.equipment, key=lambda x: float(x.get('flowrate', 0) or 0), reverse=True)[:6]
        
        names = [eq.get('name', '')[:12] for eq in sorted_eq]
        values = [float(eq.get('flowrate', 0) or 0) for eq in sorted_eq]
        
        colors = ['#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#ede9fe']
        
        y_pos = np.arange(len(names))
        ax.barh(y_pos, values, color=colors[:len(names)], alpha=0.9)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=9, color='#e0e0e0')
        ax.set_xlabel('Flowrate', color='#8080a0', fontsize=10)
        ax.tick_params(colors='#606080', labelsize=9)
        ax.invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(values):
            ax.text(v + 1, i, f'{v:.0f}', va='center', color='#8080a0', fontsize=9)
        
        for spine in ax.spines.values():
            spine.set_color('#303050')
        
        self.rank_figure.tight_layout(pad=1)
        self.rank_canvas.draw()
