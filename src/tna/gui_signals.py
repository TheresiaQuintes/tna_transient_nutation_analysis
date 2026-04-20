from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCan
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavTool
import matplotlib.pyplot as plt
import numpy as np
import pickle


def gui_init_plot_1(self, plot_window: QtWidgets.QWidget):
    """
    Initialize the matplotlib widget for the first main window.

    Parameters
    ----------
    plot_window : QtWidgets.QWidget
        QWidget which will be used as the plot area.

    Returns
    -------
    None.

    """
    self.figure1 = plt.figure(tight_layout=True)
    self.canvas_1 = FigCan(self.figure1)
    self.toolbar1 = NavTool(self.canvas_1, self)
    layout = QtWidgets.QVBoxLayout(plot_window)
    layout.addWidget(self.toolbar1)
    layout.addWidget(self.canvas_1)
    self.ax1 = self.figure1.add_subplot(111)
    # self.setLayout(layout)


def gui_init_plot_2(self, plot_window: QtWidgets.QWidget):
    """
    Initialize the matplotlib widget for the first main window.

    Parameters
    ----------
    plot_window : QtWidgets.QWidget
        QWidget which will be used as the plot area.

    Returns
    -------
    None.

    """
    self.figure2 = plt.figure(tight_layout=True)
    self.canvas_2 = FigCan(self.figure2)
    self.toolbar2 = NavTool(self.canvas_2, self)
    layout = QtWidgets.QVBoxLayout(plot_window)
    layout.addWidget(self.toolbar2)
    layout.addWidget(self.canvas_2)
    self.ax2 = self.figure2.add_subplot(111)
    # self.setLayout(layout)


def gui_connections(self):
    # update spinboxes
    self.show_experimental_button.clicked.connect(lambda: update_spinboxes(self))
    self.load_data_button.clicked.connect(lambda: update_spinboxes(self))
    self.one_d_button.clicked.connect(lambda: update_spinboxes(self))
    self.two_d_button.clicked.connect(lambda: update_spinboxes(self))
    self.save_button.clicked.connect(lambda: update_spinboxes(self))

    # update checkboxes
    self.load_data_button.clicked.connect(lambda: update_checkboxes(self))
    self.one_d_button.clicked.connect(lambda: update_checkboxes(self))
    self.two_d_button.clicked.connect(lambda: update_checkboxes(self))
    self.save_button.clicked.connect(lambda: update_checkboxes(self))
    self.one_d_radio.toggled.connect(lambda: update_dimension(self))

    # start functions
    self.show_experimental_button.clicked.connect(lambda: click_show_experimental_button(self))
    self.load_data_button.clicked.connect(lambda: click_load_data_button(self))
    self.one_d_button.clicked.connect(lambda: click_one_d_button(self))
    self.two_d_button.clicked.connect(lambda: click_two_d_button(self))
    self.save_button.clicked.connect(lambda: click_save_button(self))


def click_load_data_button(self):
    plt.style.use("style.mplstyle")

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dialog = QFileDialog()
    dialog.setFileMode(3)
    dateien = dialog.getOpenFileNames(self, "Datei wählen", options=options)[0]
    if len(dateien) == 1:
        self.par.path = dateien[0][:-4]
        loading_one_file(self)
    elif len(dateien) == 0:
        info = QMessageBox()
        info.setText("Please choose a file.")
        info.setWindowTitle("File not found")
        info.exec()
    else:
        self.par.path = dateien[0][:-4]
        loading_one_file(self)
        full_spectrum = np.zeros(self.data.spc.shape)
        for data in dateien:
            self.par.path = dateien[0][:-4]
            loading_one_file(self)
            full_spectrum += self.data.spc

        self.data.spc = full_spectrum.copy()
        self.data.time_signal = self.data.spc

    try:
        if self.par.two_d is True:
            plt.close(plt.gcf())
            self.figure1.clear()
            self.ax1.cla()
            self.ax1 = self.figure1.add_subplot(111)
            field, time = np.meshgrid(self.data.field, self.data.time)
            self.ax1.pcolormesh(field, time, self.data.spc.T)
            self.ax1.contour(field, time, self.data.spc.T, colors='k')
            self.canvas_1.draw()

            plt.close(plt.gcf())
            self.figure2.clear()
            self.ax2.cla()
            self.ax2 = self.figure2.add_subplot(111)
            time_point = (np.abs(self.data.time - self.par.current_time)).argmin()
            self.ax2.plot(self.data.field, self.data.spc[:, time_point])
            self.canvas_2.draw()

        elif self.par.two_d is False:
            plt.close(plt.gcf())
            self.figure1.clear()
            self.ax1.cla()
            self.ax1 = self.figure1.add_subplot(111)
            self.ax1.plot(self.data.t, self.data.t_signal)
            self.canvas_1.draw()

            plt.close(plt.gcf())
            self.figure2.clear()
            self.ax2.cla()
            self.ax2 = self.figure2.add_subplot(111)

    except AttributeError:
        return

def loading_one_file(self):
    if self.par.two_d is True:
        try:
            self.data.load_2d(self.par.path, self.par.prodel)
            self.data.choose_field(self.par.current_field)


            self.show_experimental_button.setEnabled(True)

        except UnboundLocalError:
            info = QMessageBox()
            info.setText("Please choose a  2 dimensional dataset.")
            info.setWindowTitle("Can not open dataset")
            info.exec()
            return

    elif self.par.two_d is False:
        try:
            self.data.load_1d(self.par.path, self.par.prodel)

        except ValueError:
            info = QMessageBox()
            info.setText("Please choose a  1 dimensional dataset.")
            info.setWindowTitle("Can not open dataset")
            info.exec()
            return


def click_show_experimental_button(self):
    plt.style.use("style.mplstyle")

    if self.par.two_d is True:
        try:
            self.data.choose_field(self.par.current_field)

            time_point = (np.abs(self.data.time - self.par.current_time)).argmin()

            plt.close(plt.gcf())
            self.figure1.clear()
            self.ax1.cla()
            self.ax1 = self.figure1.add_subplot(111)
            field, time = np.meshgrid(self.data.field, self.data.time)
            self.ax1.pcolormesh(field, time, self.data.spc.T)
            self.ax1.contour(field, time, self.data.spc.T, colors='k')
            self.canvas_1.draw()

            plt.close(plt.gcf())
            self.figure2.clear()
            self.ax2.cla()
            self.ax2 = self.figure2.add_subplot(111)
            self.ax2.plot(self.data.field, self.data.spc[:, time_point])
            self.canvas_2.draw()

        except FileNotFoundError:
            info = QMessageBox()
            info.setText("Please choose a file.")
            info.setWindowTitle("File not found")
            info.exec()

        except UnboundLocalError:
            info = QMessageBox()
            info.setText("Please choose a  2 dimensional dataset.")
            info.setWindowTitle("Can not open dataset")
            info.exec()

    elif self.par.two_d is False:
        try:
            plt.close(plt.gcf())
            self.figure1.clear()
            self.ax1.cla()
            self.ax1 = self.figure1.add_subplot(111)
            self.ax1.plot(self.data.t, self.data.t_signal)
            self.canvas_1.draw()

        except FileNotFoundError:
            info = QMessageBox()
            info.setText("Please choose a file.")
            info.setWindowTitle("File not found")
            info.exec()

        except ValueError:
            info = QMessageBox()
            info.setText("Please choose a  1 dimensional dataset.")
            info.setWindowTitle("Can not open dataset")
            info.exec()


def click_one_d_button(self):
    plt.style.use("style.mplstyle")

    if self.par.two_d is True:
        self.data.choose_field(self.par.current_field)
    elif self.par.two_d is False:
        self.data.t_signal = self.data.spc.copy()
        self.data.t = self.data.time.copy()

    if self.par.baseline_correction is True:
        self.data.baseline_correction(deg=self.par.baseline_correction_deg)

    if self.par.reconstruction is True:
        self.data.reconstruction()

    if self.par.wdw_chebwin is True:
        self.data.wdw_chebwin(self.par.chebwin_attenuation)

    if self.par.wdw_hamming is True:
        self.data.wdw_hamming(self.par.hamming_window_coefficient)

    if self.par.wdw_kaiser is True:
        self.data.wdw_kaiser(self.par.kaiser_window_shape_parameter)

    if self.par.wdw_sinebell is True:
        self.data.wdw_sinebell(self.par.sinebell_phase_shift)

    if self.par.wdw_lorentz_gauss is True:
        self.data.wdw_lorentz_gauss(self.par.tau, self.par.sigma)

    if self.par.mean_subtraction is True:
        self.data.mean_subtraction()

    if self.par.zero_filling is False:
        self.data.fourier_transformation(1, self.par.reference_freq_value)
    else:
        self.data.fourier_transformation(
            self.par.zero_filling_factor, self.par.reference_freq_value)

    plt.close(plt.gcf())
    self.figure1.clear()
    self.ax1.cla()
    self.ax1 = self.figure1.add_subplot(111)
    self.ax1.plot(self.data.t, self.data.t_signal)
    self.canvas_1.draw()

    plt.close(plt.gcf())
    self.figure2.clear()
    self.ax2.cla()
    self.ax2 = self.figure2.add_subplot(111)
    self.ax2.plot(self.data.freq, self.data.freq_signal)
    self.canvas_2.draw()


def click_two_d_button(self):
    plt.style.use("style.mplstyle")

    click_one_d_button(self)
    ft_spc = []
    for field_index in range(len(self.data.field)):
        self.data.t_signal = self.data.spc[field_index]
        self.data.t = self.data.time

        if self.par.baseline_correction is True:
            self.data.baseline_correction(deg=self.par.baseline_correction_deg)

        if self.par.reconstruction is True:
            self.data.reconstruction()

        if self.par.wdw_chebwin is True:
            self.data.wdw_chebwin(self.par.chebwin_attenuation)

        if self.par.wdw_hamming is True:
            self.data.wdw_hamming(self.par.hamming_window_coefficient)

        if self.par.wdw_kaiser is True:
            self.data.wdw_kaiser(self.par.kaiser_window_shape_parameter)

        if self.par.wdw_sinebell is True:
            self.data.wdw_sinebell(self.par.sinebell_phase_shift)

        if self.par.wdw_lorentz_gauss is True:
            self.data.wdw_lorentz_gauss(self.par.tau, self.par.sigma)

        if self.par.mean_subtraction is True:
            self.data.mean_subtraction()

        self.data.fourier_transformation(
            self.par.zero_filling_factor, self.par.reference_freq_value)
        ft_spc.append(self.data.freq_signal)

    self.data.ft_spc = np.array(ft_spc)

    plt.close(plt.gcf())
    self.figure1.clear()
    self.ax1.cla()
    self.ax1 = self.figure1.add_subplot(111)
    field, freq = np.meshgrid(self.data.field, self.data.freq)
    self.ax1.pcolormesh(field, freq, self.data.ft_spc.T)
    self.ax1.contour(field, freq, self.data.ft_spc.T, colors='k')
    self.canvas_1.draw()


def click_save_button(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    datei = QFileDialog.getSaveFileName(
        self, "Speichern unter", options=options)
    self.par.save_location = datei[0]

    with open(str(self.par.save_location)+".data", 'wb') as file:
        pickle.dump(vars(self.data), file)
    file.close()

    with open(str(self.par.save_location)+".parameters", 'wb') as file:
        pickle.dump(vars(self.par), file)
    file.close()


def update_checkboxes(self):
    if self.baseline_correction_check.isChecked():
        self.par.baseline_correction = True
    else:
        self.par.baseline_correction = False

    if self.reconstruction_check.isChecked():
        self.par.reconstruction = True
    else:
        self.par.reconstruction = False

    if self.mean_subtraction_check.isChecked():
        self.par.mean_subtraction = True
    else:
        self.par.mean_subtraction = False

    if self.zero_filling_check.isChecked():
        self.par.zero_filling = True
    else:
        self.par.zero_filling = False

    if self.reference_frequency_check.isChecked():
        self.par.reference_freq = True
    else:
        self.par.reference_freq = False
        self.par.reference_freq_value = 1

    if self.dolph_chebyshev_check.isChecked():
        self.par.wdw_chebwin = True
    else:
        self.par.wdw_chebwin = False

    if self.hamming_check.isChecked():
        self.par.wdw_hamming = True
    else:
        self.par.wdw_hamming = False

    if self.kaiser_check.isChecked():
        self.par.wdw_kaiser = True
    else:
        self.par.wdw_kaiser = False

    if self.lorentz_gauss_check.isChecked():
        self.par.wdw_lorentz_gauss = True
    else:
        self.par.wdw_lorentz_gauss = False

    if self.sinebell_check.isChecked():
        self.par.wdw_sinebell = True
    else:
        self.par.wdw_sinebell = False

    if self.prodel_check.isChecked():
        self.par.prodel = True
    else:
        self.par.prodel = False


def update_dimension(self):
    if self.one_d_radio.isChecked():
        self.show_experimental_button.setEnabled(False)
        self.two_d_button.setEnabled(False)
        self.prodel_check.setEnabled(False)
        self.time_point_box.setEnabled(False)
        self.field_point_box.setEnabled(False)
        self.par.two_d = False
    elif self.two_d_radio.isChecked():
        self.two_d_button.setEnabled(True)
        self.prodel_check.setEnabled(True)
        self.time_point_box.setEnabled(True)
        self.field_point_box.setEnabled(True)
        self.par.two_d = True


def update_spinboxes(self):
    self.par.current_field = self.field_point_box.value()
    self.par.current_time = self.time_point_box.value()

    self.par.baseline_correction_deg = self.baseline_value_box.value()
    self.par.zero_filling_factor = self.zero_filling_value_box.value()
    self.par.reference_freq_value =\
        self.reference_frequency_value_box.value()*1e6

    self.par.chebwin_attenuation = self.dolph_chebyshev_value_box.value()
    self.par.hamming_window_coefficient = self.hamming_value_box.value()
    self.par.kaiser_window_shape_parameter = self.kaiser_value_box.value()
    self.par.sinebell_phase_shift = self.sinebell_value_box.value()
    self.par.tau = self.lorentz_gauss_tau_value_box.value()
    self.par.sigma = self.lorentz_gauss_sigma_value_box.value()
