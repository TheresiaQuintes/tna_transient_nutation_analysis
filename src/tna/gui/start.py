from PyQt6 import QtWidgets
import tna.gui.GUI as GUI
import sys
import tna.gui.gui_signals as sgn
import traceback

def excepthook(exc_type, exc_value, exc_tb):
    """
    Global exception handler for uncaught exceptions.

    Prints the traceback and forwards to the default system handler.

    """
    # TODO: Logger statt print
    traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

class MainWindow(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    """
    Main application window.

    Initializes the UI and connects the TNA controller
    to handle user interaction and data processing.

    """

    def __init__(self):
        """
        Initialises the main window and connects the controller.

        """
        super().__init__()
        self.setupUi(self)
        self.controller = sgn.TNAController(self)
        self.controller.connect_signals()



def main():
    """
    Entry point of the application.

    Creates the Qt application, initializes the main window,
    and starts the event loop.

    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Transient Nutation - Spectra Analysis')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
