import numpy as np
import scipy as sp
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
from pydantic import BaseModel, Field
from typing import Optional


class TransientNutations:
    """
    Transient nutation data class.

    Transient nutation data can be loaded and processed.

    Attributes
    ----------
    The __init__ functions creates the following attributes but sets them to
    None. Attributes are filled with values using the methods.

    field : np.ndarray
        Magnetic field array (for 2D data sets).
    time : np.ndarray
        Time point array.
    spc : np.ndarray
        Intensities of the experimental data. May be 1D or 2D.
    chosen_field : float
        Chosen magnetic field point to get the time trace of two dimensional
        spectra.
    t_signal : np.ndarray
        Signal intensities along the time axis, (processed) experimental data.
    freq_signal : np.ndarray
        Fourier transform of the t_signal.
    t : np.ndarray
        (Processed) time axis.
    freq : np.ndarray
        Frequency axis for the freq_signal.
    """

    def __init__(self):
        self.field = None
        self.time = None
        self.spc = None

        self.chosen_field = 0

        self.t_signal = None
        self.freq_signal = None
        self.t = None
        self.freq = None

# TODO
# Loader für specatalog-hdf5 hinzufügen

    def load_2d(self, filename: str, prodel=False):
        """
        Load two dimensional transient nutation data in .DSC/.DTA format.
        Set the attributes time, field and spc.

        Parameters
        ----------
        filename : str
            Absolute path to the data excluding the file extension.
        prodel : boolean, optional
            Defines if data were recorded using prodel. Real and imaginary
            parts of the signal are swapped. The default is False.

        Returns
        -------
        None.

        """
        f = open(filename + ".DTA", "rb")
        intensities = np.fromfile(f, dtype=np.dtype('>f8'))
        intensities = intensities.astype(float)
        f.close()

        f = open(filename + ".DSC", 'r')

        for line in f.readlines():
            # complex signal?
            if line.startswith('IKKF'):
                s = line.split()
                if s[1] == 'CPLX':
                    complex_signal = True
                else:
                    complex_signal = False

            # number of delays
            if line.startswith('XPTS'):
                s = line.split()
                t_points = int(s[1])

            # minimum time
            if line.startswith('XMIN'):
                s = line.split()
                t_min = float(s[1])

            # time range
            if line.startswith('XWID'):
                s = line.split()
                t_width = float(s[1])

            # number of magnetic field points
            if line.startswith('YPTS'):
                s = line.split()
                b_points = int(s[1])

            # minimum magnetic field
            if line.startswith('YMIN'):
                s = line.split()
                b_min = float(s[1])

            # magnetic field range
            if line.startswith('YWID'):
                s = line.split()
                b_width = float(s[1])

        f.close()

        if complex_signal is True:
            if prodel is False:
                spc = intensities[0::2]
            elif prodel is True:
                spc = intensities[1::2]

        elif complex_signal is False:
            spc = intensities

        self.time = np.linspace(t_min, t_min+t_width, t_points)
        self.field = np.linspace(b_min, b_min+b_width, b_points)
        self.spc = spc.reshape((len(self.field), len(self.time)))
        return

    def load_1d(self, filename: str, prodel=False):
        """
        Load one dimensional transient nutation data in .DSC/.DTA format.
        Set the attributes time, spc, t and time_signal.

        Parameters
        ----------
        filename : str
            Absolute path to the data excluding the file extension.
        prodel : boolean, optional
            Defines if data were recorded using prodel. Real and imaginary
            parts of the signal are swapped. The default is False.

        Returns
        -------
        None.

        """
        f = open(filename + ".DTA", "rb")
        intensities = np.fromfile(f, dtype=np.dtype('>f8'))
        intensities = intensities.astype(float)
        f.close()

        f = open(filename + ".DSC", 'r')

        for line in f.readlines():
            # complex signal?
            if line.startswith('IKKF'):
                s = line.split()
                if s[1] == 'CPLX':
                    complex_signal = True
                else:
                    complex_signal = False

            # number of delays
            if line.startswith('XPTS'):
                s = line.split()
                t_points = int(s[1])

            # minimum time
            if line.startswith('XMIN'):
                s = line.split()
                t_min = float(s[1])

            # time range
            if line.startswith('XWID'):
                s = line.split()
                t_width = float(s[1])

        f.close()

        if complex_signal is True:
            if prodel is False:
                spc = intensities[0::2]
            elif prodel is True:
                spc = intensities[1::2]

        elif complex_signal is False:
            spc = intensities

        self.time = np.linspace(t_min, t_min+t_width, t_points)
        self.spc = spc
        self.t = self.time
        self.t_signal = self.spc
        return

    def choose_field(self, field: float):
        """
        Get the time signal at the given field point out of a 2dimensional
        spectrum (spc).

        Parameters
        ----------
        field : float
            Chosen magnetic field point in the same unit as in the experimental
            data set.

        Returns
        -------
        None.

        """
        idx = (np.abs(self.field - field)).argmin()
        self.chosen_field = self.field[idx].copy()
        self.t_signal = self.spc[idx].copy()
        self.t = self.time.copy()
        return

    def baseline_correction(self, deg=1):
        """
        Baseline correction of the signal by using a polynominal fit function.

        Parameters
        ----------
        deg : int, optional
            Degree of the polynominal fit. The default is 1.

        Returns
        -------
        None.

        """
        coefficients = np.polyfit(self.t, self.t_signal, deg)
        fit = np.poly1d(coefficients)
        baseline = fit(self.t)
        self.t_signal -= baseline
        return

    def reconstruction(self):
        """
        Reconstruction of a time signal use the Yule-Walker algorithm. Time
        signal is reconstructed to zero.

        Returns
        -------
        None.

        """
        x = self.t.copy()
        y = self.t_signal.copy()
        # prepare the new array
        x_step = x[1] - x[0]
        if x[0] % x_step != 0:
            x_fill_points = int(x[0] / x_step) + 1
        else:
            x_fill_points = int(x[0] / x_step)
        x_new = np.concatenate(
            (np.linspace(x[0]-x_step*x_fill_points, x[0]-x_step, x_fill_points), x)
        )

        # determine the order of the p value for the reconstruction
        order = ar_select_order(y[::-1], maxlag=40)
        nlag = len(order.ar_lags)

        # Fit the model to the data and make a predicition
        AutoRegFit = AutoReg(y[::-1], lags=order.ar_lags).fit()
        y_pred = AutoRegFit.predict(start=0, end=x_new.shape[0]+nlag-1)

        y_pred = np.roll(y_pred[nlag:], nlag)
        y_flip = y_pred
        y_flip = np.concatenate((y[::-1], y_flip[len(y):]))

        self.t = x_new
        self.t_signal = y_flip[::-1]
        return

    def wdw_chebwin(self, at=45):
        """
        Convolve a time signal with the Dolph-Chebyshev window. This window
        may be used for ripple suppression but broadenes the fourier
        transformed signal. The ripple level is given in dB.

        Parameters
        ----------
        at : float, optional
            Attenuation in dB. The bigger the ripple level the broader and
            smoother gets the signal. The default and minimum value is 45.

        Returns
        -------
        None.

        """
        wdw_chebwin = sp.signal.windows.chebwin(2*len(self.t), at, sym=False)
        wdw_chebwin = np.array_split(wdw_chebwin, 2)[-1]
        self.t_signal *= wdw_chebwin
        return

    def wdw_hamming(self, alpha=0.54):
        """
        Convolve a time singal with the Hamming window. This is a standard
        window for ripple suppression and broadenes the fourier transformed
        signal.

        Parameters
        ----------
        alpha : float, optional
            Window coefficient. Use 0.54 for the default Hamming function.
            The bigger the coefficient is chosen the better gets the smoothing.
            The default is 0.54.

        Returns
        -------
        None.

        """
        wdw_hamming = sp.signal.windows.general_hamming(
            2*len(self.t), alpha, sym=False)
        wdw_hamming = np.array_split(wdw_hamming, 2)[-1]
        self.t_signal *= wdw_hamming
        return

    def wdw_kaiser(self, beta=2):
        """
        Convolve the signal with the Kaiser window for ripple supression and
        causes signal broadening of the fourier transformed signal. The window
        can be scaled by the shape parameter beta.

        Parameters
        ----------
        beta : float, optional
            Window shape parameter. The higher the parameter the more the
            signal is smoothened. A shape parameter of 2 is normally a good
            compromise between line broadening and smoothing. The default is 2.

        Returns
        -------
        None.

        """
        wdw_kaiser = sp.signal.windows.kaiser(2*len(self.t), beta, sym=False)
        wdw_kaiser = np.array_split(wdw_kaiser, 2)[-1]
        self.t_signal *= wdw_kaiser
        return

    def wdw_sinebell(self, phi=0):
        """
        Convolve the time signal by the phase-shifted Sinebell window. For
        phi=0 the first point of the time-domain signal is set to zero. The
        Sinebell window causes a decrease of the signal-to-noise ratio but a
        improvement of the resolution of the fourier transformed signal.

        Parameters
        ----------
        phi : float, optional
            Phase shift of the Sinebell window. Larger phase shifts correspond
            to less resolution enhancement. The default is 0.

        Returns
        -------
        None.

        """
        wdw_sinebell = np.sin(np.pi*self.t/(self.t[-1]) + phi)
        self.t_signal *= wdw_sinebell
        return

    def wdw_lorentz_gauss(self, tau: float, sigma: float):
        """
        Convolve the time signal by the Lorentz-Gauss window. The signal decays
        less fast which causes a improvement of resolution in the fourier
        transformed spectrum. Signal-to-noise ratio is decreased.
        Lorntzian lines with the linewidth 1/pi*tau are transformed to Gaussian
        lines with a linewidth sqrt(2ln2)/pi*sigma. The parameters tau and
        sigma have to be chosen.

        Parameters
        ----------
        tau : float
            Defining the Lorentzian lineshape. tau=T2, if no good estimate for
            tau is known, start by setting tau=t_max/3.
        sigma : float
            Defining the Gaussian lineshape. For resolution enhancement set
            sigma = 1/2*tau.

        Returns
        -------
        None.

        """
        wdw_lorentz_gauss = np.exp(self.t/tau - (sigma**2 * self.t**2)/2)
        self.t_signal *= wdw_lorentz_gauss
        return

    def mean_subtraction(self):
        """
        Subtraction of the mean of the signal from the signal. This kills the
        mean frequency peak in the fourier transformed spectrum at zero
        frequency.

        Returns
        -------
        None.

        """
        self.t_signal -= self.t_signal.mean()
        return

    def fourier_transformation(self, zero_filling=2, reference_freq=1):
        """
        Do a discrete fast fourier transformation of the time signal using
        the scipy function fft.fft. The time signal is filled with zeros
        first to improve the resoulution. The transformed signal can be
        scaled by a reference frequency. The attributes freq and freq_signal
        are assigned by this function.

        Parameters
        ----------
        zero_filling : int, optional
            The signal is filled with zeros before fourier transformation. This
            parameter is a factor for the length of the signal. If it is set to
            2 the signal is filled to doubled length. This produces the best
            possible resoulution. The default is 2.
        reference_freq : float, optional
            The frequency can be scaled to a reference frequency. The
            frequencies are divided by the reference frequency. A reference
            frequency of 1 causes no changees in the frequencies.
            The default is 1.

        Returns
        -------
        None.

        """

        freq_signal = sp.fft.fft(
            self.t_signal, n=zero_filling*len(self.t))
        freq_signal = np.array_split(freq_signal, 2)[0]
        freq_signal = abs(freq_signal)

        freq = sp.fft.fftfreq(
            zero_filling*len(self.t), (self.t[1]-self.t[0])*1e-9)
        freq = np.array_split(freq, 2)[0]

        freq /= reference_freq

        self.freq = freq
        self.freq_signal = freq_signal
        return


class OldParameters():
    """
    Create a set of parameters to control the correction of transient nutation
    data.

    Attributes
    ----------

    current_time : float
        Time point at which the magnetic field spectrum shall be shown.
    current_field : float
        Magnetic field point at which the time spectrum shall be shown.
    prodel : boolean
        Swap the imaginary and the real part of the signal.
    two_d : boolean
        Define the data to be one or two dimensional.
    path : string
        Absolute path to experimental data.
    baseline_correction : boolean
        Do a baseline correction?
    baseline_correction_deg : int
        Degree of the polynominal function of the baseline correction
    reconstruction : boolean
        Do a signal reconstruction?
    mean_subtraction : boolean
        Do the mean subtraction?
    wdw_chebwin : boolean
        Convolve the signal with the Dolph-Chebyshew window?
    chebwin_attenuation : float
        Attenuation of the Dolph-Chebyshew window in dB.
    wdw_hamming : boolean
        Convolve the signal with the Hamming window?
    hamming_window_coefficient : float
        Coefficient giving the broadening of the Hamming window. For a default
        window this should be 0.54.
    wdw_kaiser : boolean
        Convolve the signal with the Kaiser window?
    kaiser_window_shape_parameter : float
        Shape parameter of the Kaiser window. A good value is 2.
    wdw_sinebell : boolean
        Convolve the signal with the Sinebell window?
    sinebell_phase_shift : float
        Phase shift of the sinebell function.
    wdw_lorentz_gauss : boolean
        Convolve the signal with the Lorentz-Gauss-Window?
    tau : float
        Define FWHH of the Lorentz-Function by 1/pi*tau.
    sigma : float
        Define FWHH of the Gaussian-Function by sqrt(2ln2)/pi*sigma.
    zero_filling : boolean
        Do zero filling before fourier transformation?
    zero_filling_factor : float
        Signal is filled to zero_filling_factor*length(signal) with zeros.
    reference_freq : boolean
        Correct frequencies to a reference frequency?
    reference_freq_value : float
        Value of the reference frequency to which all frequencies are
        corrected.
    save_location : str
        Full path to save the results.

    """

    def __init__(self):
        self.current_time = 0
        self.current_field = 12020

        self.prodel = False
        self.two_d = True
        self.path = None

        self.baseline_correction = False
        self.baseline_correction_deg = 1
        self.reconstruction = False
        self.mean_subtraction = False

        self.wdw_chebwin = False
        self.chebwin_attenuation = 45

        self.wdw_hamming = False
        self.hamming_window_coefficient = 0.54

        self.wdw_kaiser = False
        self.kaiser_window_shape_parameter = 2

        self.wdw_sinebell = False
        self.sinebell_phase_shift = 0

        self.wdw_lorentz_gauss = False
        self.tau = 170
        self.sigma = 0.003

        self.zero_filling = False
        self.zero_filling_factor = 2
        self.reference_freq = False
        self.reference_freq_value = 1e7

        self.save_location = None




class Parameters(BaseModel):
    model_config = {
        "frozen": True,
        "extra": "forbid"
    }
    current_time: float = 0
    current_field: float = 12020

    prodel: bool = False
    two_d: bool = True
    path: Optional[str] = None

    baseline_correction: bool = False
    baseline_correction_deg: int = 1
    reconstruction: bool = False
    mean_subtraction: bool = False

    wdw_chebwin: bool = False
    chebwin_attenuation: float = 45

    wdw_hamming: bool = False
    hamming_window_coefficient: float = 0.54

    wdw_kaiser: bool = False
    kaiser_window_shape_parameter: float = 2

    wdw_sinebell: bool = False
    sinebell_phase_shift: float = 0

    wdw_lorentz_gauss: bool = False
    tau: float = 170
    sigma: float = 0.003

    zero_filling: bool = False
    zero_filling_factor: int = 2

    reference_freq: bool = False
    reference_freq_value: float = 1e7

    save_location: Optional[str] = None
