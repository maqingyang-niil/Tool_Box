import sys
from PyQt6.QtWidgets import QApplication
from core.app import MainWindow


def main():
    app=QApplication(sys.argv)
    app.setApplicationName("ToolBox")
    window=MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ =="__main__":
    main()