"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point for the PyQt5 desktop frontend.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from services.api_client import api_client
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow


def main():
    """Main entry point."""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Show login dialog
    login_dialog = LoginDialog(api_client)
    
    if login_dialog.exec_() == LoginDialog.Accepted:
        # Show main window
        main_window = MainWindow(api_client)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
