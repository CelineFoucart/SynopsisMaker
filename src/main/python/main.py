import sys

from fbs_runtime.application_context.PySide2 import ApplicationContext
from gui.main_window import MainWindow

if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = MainWindow()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
