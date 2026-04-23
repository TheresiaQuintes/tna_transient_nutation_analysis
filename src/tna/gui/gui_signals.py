from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigCan
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavTool
import matplotlib.pyplot as plt
import numpy as np
import pickle
import tna.classes as cl
import traceback



class TNAController:
    """
    Controller class for the TNA GUI application.

    This class connects the GUI (view) with the data structures (model)
    and manages all user interactions as well as data processing pipelines.

    """
    def __init__(self, view):
        """
        Parameters
        ----------
        view : object
            GUI object (view) containing the Qt widgets.

        """
        self.view = view
        self.data = cl.TransientNutations()
        self.par = cl.Parameters()

        self.gui_init_plot_1(view.plot_area_1)
        self.gui_init_plot_2(view.plot_area_2)

    def connect_signals(self):
        """
        Connects GUI signals to the corresponding controller methods.

        Includes:

        - Checkbox and spinbox updates
        - Button actions
        - Dimension switching (1D / 2D)

        """
        # update spinboxes
        self.view.show_experimental_button.clicked.connect(safe_slot(self.update_spinboxes))
        self.view.load_data_button.clicked.connect(safe_slot(self.update_spinboxes))
        self.view.one_d_button.clicked.connect(safe_slot(self.update_spinboxes))
        self.view.two_d_button.clicked.connect(safe_slot(self.update_spinboxes))
        self.view.save_button.clicked.connect(safe_slot(self.update_spinboxes))

        # update checkboxes
        self.view.load_data_button.clicked.connect(safe_slot(self.update_checkboxes))
        self.view.one_d_button.clicked.connect(safe_slot(self.update_checkboxes))
        self.view.two_d_button.clicked.connect(safe_slot(self.update_checkboxes))
        self.view.save_button.clicked.connect(safe_slot(self.update_checkboxes))
        self.view.one_d_radio.toggled.connect(safe_slot(self.update_dimension))

        # start functions
        self.view.show_experimental_button.clicked.connect(safe_slot(self.click_show_experimental_button))
        self.view.load_data_button.clicked.connect(safe_slot(self.click_load_data_button))
        self.view.one_d_button.clicked.connect(safe_slot(self.click_one_d_button))
        self.view.two_d_button.clicked.connect(safe_slot(self.click_two_d_button))
        self.view.save_button.clicked.connect(safe_slot(self.click_save_button))

    def click_load_data_button(self, *args):
        """
        Loads one or more data files via a file dialog.

        If multiple files are selected, their data is summed.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """

        dateien, _ = QFileDialog.getOpenFileNames(
            self.view,
            "Datei wählen",
            options=QFileDialog.Option.DontUseNativeDialog
        )
        if len(dateien) == 1:
            self.par.path = dateien[0][:-4]
            self.loading_one_file()
        elif len(dateien) == 0:
            return
        else:
            # TODO: Was passiert hier? Hier wollte ich glaube ich mehrere
            # Dateien Aufaddieren aber das stimmt so glaube ich nicht??
            self.par.path = dateien[0][:-4]
            self.loading_one_file()
            full_spectrum = np.zeros(self.data.spc.shape)
            for data in dateien:
                self.par.path = dateien[0][:-4]
                self.loading_one_file()
                full_spectrum += self.data.spc

            self.data.spc = full_spectrum.copy()
            self.data.time_signal = self.data.spc

        try:
            if self.par.two_d:
                self.view.figure1.clear()
                self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
                field, time = np.meshgrid(self.data.field, self.data.time)
                self.view.ax1.pcolormesh(field, time, self.data.spc.T)
                self.view.ax1.contour(field, time, self.data.spc.T, colors='k')
                self.view.canvas_1.draw()

                self.view.figure2.clear()
                self.view.ax2 = reset_plot(self.view.figure2, self.view.ax2)
                time_point = (np.abs(self.data.time - self.par.current_time)).argmin()
                self.view.ax2.plot(self.data.field, self.data.spc[:, time_point])
                self.view.canvas_2.draw()

            else:
                try:
                    self.view.figure1.clear()
                    self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
                    self.view.ax1.plot(self.data.t, self.data.t_signal)
                    self.view.canvas_1.draw()

                    self.view.figure2.clear()
                    self.view.ax2 = reset_plot(self.view.figure2, self.view.ax2)
                except ValueError:
                    pass

        except AttributeError:
            return

    def loading_one_file(self):
        """
        Loads a single file depending on the selected dimensionality (1D/2D).

        Raises
        ------
        QMessageBox
            If an incorrect dataset type is selected (1D vs 2D mismatch).

        """
        if self.par.two_d:
            try:
                self.data.load_2d(self.par.path, self.par.prodel)
                self.data.choose_field(self.par.current_field)

                self.view.show_experimental_button.setEnabled(True)

            except UnboundLocalError:
                info = QMessageBox()
                info.setText("Please choose a  2 dimensional dataset.")
                info.setWindowTitle("Can not open dataset")
                info.exec()
                return

        else:
            try:
                self.data.load_1d(self.par.path, self.par.prodel)

                if len(self.data.spc.shape) == 1:
                    info = QMessageBox()
                    info.setText("Please choose a  1 dimensional dataset.")
                    info.setWindowTitle("Can not open dataset")
                    info.exec()

            except ValueError:
                info = QMessageBox()
                info.setText("Please choose a  1 dimensional dataset.")
                info.setWindowTitle("Can not open dataset")
                info.exec()
                return

    def click_show_experimental_button(self, *args):
        """
        Displays the loaded raw data in the plots.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        if self.par.two_d:
            try:
                self.data.choose_field(self.par.current_field)

                time_point = (np.abs(self.data.time - self.par.current_time)).argmin()

                self.view.figure1.clear()
                self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
                field, time = np.meshgrid(self.data.field, self.data.time)
                self.view.ax1.pcolormesh(field, time, self.data.spc.T)
                self.view.ax1.contour(field, time, self.data.spc.T, colors='k')
                self.view.canvas_1.draw()

                self.view.figure2.clear()
                self.view.ax2 = reset_plot(self.view.figure2, self.view.ax2)
                self.view.ax2.plot(self.data.field, self.data.spc[:, time_point])
                self.view.canvas_2.draw()

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

        else:
            try:
                self.view.figure1.clear()
                self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
                self.view.ax1.plot(self.data.t, self.data.t_signal)
                self.view.canvas_1.draw()

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

    def click_one_d_button(self, *args):
        """
        Executes the 1D data processing pipeline.

        Includes:
        - Pre-processing (filters, window functions, baseline correction, etc.)
        - Fourier transformation
        - Plot updates

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        if self.par.two_d:
            self.data.choose_field(self.par.current_field)
        else:
            self.data.t_signal = self.data.spc.copy()
            self.data.t = self.data.time.copy()

        # define pipeline
        processing_steps = [
            (self.par.baseline_correction,
             lambda: self.data.baseline_correction(deg=self.par.baseline_correction_deg)),
            (self.par.reconstruction, self.data.reconstruction),
            (self.par.wdw_chebwin,
             lambda: self.data.wdw_chebwin(self.par.chebwin_attenuation)),
            (self.par.wdw_hamming,
             lambda: self.data.wdw_hamming(self.par.hamming_window_coefficient)),
            (self.par.wdw_kaiser,
             lambda: self.data.wdw_kaiser(self.par.kaiser_window_shape_parameter)),
            (self.par.wdw_sinebell,
             lambda: self.data.wdw_sinebell(self.par.sinebell_phase_shift)),
            (self.par.wdw_lorentz_gauss,
             lambda: self.data.wdw_lorentz_gauss(self.par.tau, self.par.sigma)),
            (self.par.mean_subtraction, self.data.mean_subtraction),
        ]

        # run pipeline
        for condition, func in processing_steps:
            if condition:
                func()

        # fourier transformation
        zero_fill = 1 if not self.par.zero_filling else self.par.zero_filling_factor
        self.data.fourier_transformation(
            zero_fill,
            self.par.reference_freq_value
        )

        self.view.figure1.clear()
        self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
        self.view.ax1.plot(self.data.t, self.data.t_signal)
        self.view.canvas_1.draw()

        self.view.figure2.clear()
        self.view.ax2 = reset_plot(self.view.figure2, self.view.ax2)
        self.view.ax2.plot(self.data.freq, self.data.freq_signal)
        self.view.canvas_2.draw()

    def click_two_d_button(self, *args):
        """
        Performs 2D data processing.

        Applies the 1D processing pipeline for each field and then constructs
        a 2D frequency spectrum.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """

        self.click_one_d_button()

        ft_spc = []

        # define pipeline
        processing_steps = [
            (self.par.baseline_correction,
             lambda: self.data.baseline_correction(deg=self.par.baseline_correction_deg)),
            (self.par.reconstruction, self.data.reconstruction),
            (self.par.wdw_chebwin,
             lambda: self.data.wdw_chebwin(self.par.chebwin_attenuation)),
            (self.par.wdw_hamming,
             lambda: self.data.wdw_hamming(self.par.hamming_window_coefficient)),
            (self.par.wdw_kaiser,
             lambda: self.data.wdw_kaiser(self.par.kaiser_window_shape_parameter)),
            (self.par.wdw_sinebell,
             lambda: self.data.wdw_sinebell(self.par.sinebell_phase_shift)),
            (self.par.wdw_lorentz_gauss,
             lambda: self.data.wdw_lorentz_gauss(self.par.tau, self.par.sigma)),
            (self.par.mean_subtraction, self.data.mean_subtraction),
        ]

        for field_index in range(len(self.data.field)):
            self.data.t_signal = self.data.spc[field_index]
            self.data.t = self.data.time

            # run pipeline
            for condition, func in processing_steps:
                if condition:
                    func()

            self.data.fourier_transformation(
                self.par.zero_filling_factor,
                self.par.reference_freq_value
            )

            ft_spc.append(self.data.freq_signal)

        self.data.ft_spc = np.array(ft_spc)

        self.view.figure1.clear()
        self.view.ax1 = reset_plot(self.view.figure1, self.view.ax1)
        field, freq = np.meshgrid(self.data.field, self.data.freq)
        self.view.ax1.pcolormesh(field, freq, self.data.ft_spc.T)
        self.view.ax1.contour(field, freq, self.data.ft_spc.T, colors='k')
        self.view.canvas_1.draw()

    def click_save_button(self, *args):
        """
        Saves the current data and parameters as pickle files.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        options = QFileDialog.Option.DontUseNativeDialog
        datei, _ = QFileDialog.getSaveFileName(
            self.view, "Speichern unter", options=options)
        if not datei:
            return
        self.par.save_location = datei

        with open(str(self.par.save_location) + ".data", 'wb') as file:
            pickle.dump(vars(self.data), file)


        with open(str(self.par.save_location) + ".parameters", 'wb') as file:
            pickle.dump(vars(self.par), file)

    def update_checkboxes(self, *args):
        """
        Synchronizes GUI checkboxes with the parameter object.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        mapping = {
            "baseline_correction_check": "baseline_correction",
            "reconstruction_check": "reconstruction",
            "mean_subtraction_check": "mean_subtraction",
            "zero_filling_check": "zero_filling",
            "reference_frequency_check": "reference_freq",
            "dolph_chebyshev_check": "wdw_chebwin",
            "hamming_check": "wdw_hamming",
            "kaiser_check": "wdw_kaiser",
            "lorentz_gauss_check": "wdw_lorentz_gauss",
            "sinebell_check": "wdw_sinebell",
            "prodel_check": "prodel",
        }

        for checkbox_name, param_name in mapping.items():
            checkbox = getattr(self.view, checkbox_name)
            setattr(self.par, param_name, checkbox.isChecked())

        if not self.view.reference_frequency_check.isChecked():
            self.par.reference_freq_value = 1

    def update_dimension(self, *args):
        """
        Switches between 1D and 2D mode.

        Enables or disables the corresponding GUI elements.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        if self.view.one_d_radio.isChecked():
            self.view.show_experimental_button.setEnabled(False)
            self.view.two_d_button.setEnabled(False)
            self.view.prodel_check.setEnabled(False)
            self.view.time_point_box.setEnabled(False)
            self.view.field_point_box.setEnabled(False)
            self.par.two_d = False
        elif self.view.two_d_radio.isChecked():
            self.view.two_d_button.setEnabled(True)
            self.view.prodel_check.setEnabled(True)
            self.view.time_point_box.setEnabled(True)
            self.view.field_point_box.setEnabled(True)
            self.par.two_d = True

    def update_spinboxes(self, *args):
        """
        Updates parameters from GUI spinbox values.

        Parameters
        ----------
        *args : tuple
            Dummy arguments for Qt signals.

        """
        self.par.current_field = self.view.field_point_box.value()
        self.par.current_time = self.view.time_point_box.value()

        self.par.baseline_correction_deg = self.view.baseline_value_box.value()
        self.par.zero_filling_factor = self.view.zero_filling_value_box.value()
        self.par.reference_freq_value = \
            self.view.reference_frequency_value_box.value() * 1e6

        self.par.chebwin_attenuation = self.view.dolph_chebyshev_value_box.value()
        self.par.hamming_window_coefficient = self.view.hamming_value_box.value()
        self.par.kaiser_window_shape_parameter = self.view.kaiser_value_box.value()
        self.par.sinebell_phase_shift = self.view.sinebell_value_box.value()
        self.par.tau = self.view.lorentz_gauss_tau_value_box.value()
        self.par.sigma = self.view.lorentz_gauss_sigma_value_box.value()


    def gui_init_plot_1(self, plot_window: QtWidgets.QWidget):
        """
        Initializes the first Matplotlib plot widget.

        Parameters
        ----------
        plot_window : QtWidgets.QWidget
            Widget container for plot 1.

        Returns
        -------
        None
        """
        self.view.figure1 = plt.figure(tight_layout=True)
        self.view.canvas_1 = FigCan(self.view.figure1)
        self.toolbar1 = NavTool(self.view.canvas_1, self.view)
        layout = QtWidgets.QVBoxLayout(plot_window)
        layout.addWidget(self.toolbar1)
        layout.addWidget(self.view.canvas_1)
        self.view.ax1 = self.view.figure1.add_subplot(111)

    def gui_init_plot_2(self, plot_window: QtWidgets.QWidget):
        """
        Initializes the second Matplotlib plot widget.

        Parameters
        ----------
        plot_window : QtWidgets.QWidget
            Widget container for plot 2.

        Returns
        -------
        None

        """
        self.view.figure2 = plt.figure(tight_layout=True)
        self.view.canvas_2 = FigCan(self.view.figure2)
        self.toolbar2 = NavTool(self.view.canvas_2, self.view)
        layout = QtWidgets.QVBoxLayout(plot_window)
        layout.addWidget(self.toolbar2)
        layout.addWidget(self.view.canvas_2)
        self.view.ax2 = self.view.figure2.add_subplot(111)

def safe_slot(func):
    """
    Decorator for safe execution of Qt slots.

    Catches all exceptions and displays them in a message box.

    Parameters
    ----------
    func : callable
        Function to be used as a Qt slot.

    Returns
    -------
    callable
        Wrapped function with exception handling.

    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            error_msg = traceback.format_exc()
            print(error_msg)
            QMessageBox.critical(None, "Error", error_msg)
    return wrapper

def reset_plot(fig, ax):
    """
    Resets a Matplotlib figure and creates a new axis.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure object to be cleared.
    ax : matplotlib.axes.Axes
        Previous axis (will be replaced).

    Returns
    -------
    matplotlib.axes.Axes
        New axis added to the figure.
    """
    fig.clear()
    ax = fig.add_subplot(111)
    return ax
