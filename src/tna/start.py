from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
import tna.GUI as GUI
import sys
import tna.gui_signals as sgn
import tna.functions as fun
#import funktionen as fun
#import signals as sg
#import time as time



class MainWindow(QtWidgets.QMainWindow, GUI.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.data = fun.TransientNutations()
        self.par = fun.Parameters()
        sgn.gui_init_plot_1(self, self.plot_area_1)
        sgn.gui_init_plot_2(self, self.plot_area_2)
        sgn.gui_connections(self)



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle('Transient Nutation - Spectra Analysis')

    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
