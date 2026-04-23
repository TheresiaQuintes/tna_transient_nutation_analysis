from PyQt6 import QtWidgets
import tna.gui.GUI_neu as GUI
import sys
import tna.gui.gui_signals as sgn
import tna.classes as fun
import traceback

def excepthook(exc_type, exc_value, exc_tb):
    # TODO: Logger statt print
    traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

class MainWindow(QtWidgets.QMainWindow, GUI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = sgn.TNAController(self)
        self.controller.connect_signals()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Transient Nutation - Spectra Analysis')

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
