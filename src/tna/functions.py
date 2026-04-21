import numpy as np
import matplotlib.pyplot as plt
import tna.classes as cl
from pathlib import Path

def run_tna(data_path: Path, params: cl.Parameters) -> cl.TransientNutations:
    """
    Run transient nutation analysis for a single dataset (1D or selected slice of 2D).

    This function loads the experimental data, applies the selected processing
    steps, performs a Fourier transformation, and returns the processed data
    object.

    Parameters
    ----------
    data_path : Path
        Absolute path to the experimental data without suffix.
    params : cl.Parameters
        Parameter object controlling data loading, processing pipeline, and
        Fourier transformation settings.

    Returns
    -------
    data : cl.TransientNutations
        Processed data object containing time-domain and frequency-domain
        results.

    Notes
    -----
    - If ``params.two_d`` is True, a 2D dataset is loaded and a single field
      slice is selected using ``params.current_field``.
    - Processing steps are applied according to the flags defined in ``params``.
    - Fourier transformation parameters are resolved via
      ``_resolve_fourier_params``.
    """

    data = cl.TransientNutations()

    # loading
    if params.two_d:
        data.load_2d(data_path, params.prodel)
        data.choose_field(params.current_field)
    else:
        data.load_1d(data_path, params.prodel)

    # processing
    _apply_processing(data, params)

    # fourier transformation
    zf, rf = _resolve_fourier_params(params)
    data.fourier_transformation(zf, rf)

    return data

def run_tna_2d(data_path: Path, params: cl.Parameters) -> cl.TransientNutations:
    """
    Run transient nutation analysis for a full 2D dataset.

    This function processes each field slice of a 2D transient nutation dataset
    individually, applies the selected processing steps, performs Fourier
    transformation, and returns the resulting frequency-domain spectra.

    Parameters
    ----------
    data_path : Path
        Absolute path to the experimental data without suffix.
    params : cl.Parameters
        Parameter object controlling processing steps and Fourier transformation.

    Returns
    -------
    data : cl.TransientNutations
        Data object where ``data.freq_signal`` contains the 2D array of Fourier-
        transformed spectra with shape (n_fields, n_frequencies).

    Notes
    -----
    - The dataset is loaded using ``load_2d``.
    - Each field slice is processed independently using the same parameter set.
    - The resulting spectra are stacked into a NumPy array and stored in
      ``data.freq_signal``.
    """
    data = cl.TransientNutations()

    # loading
    data.load_2d(data_path, params.prodel)

    # process & transform each field slice
    ft_spc = []
    for i in range(len(data.field)):
        data.t_signal = data.spc[i]
        data.t = data.time

        _apply_processing(data, params)

        zf, rf = _resolve_fourier_params(params)
        data.fourier_transformation(zf, rf)

        ft_spc.append(data.freq_signal)

    data.freq_signal = np.array(ft_spc)
    return  data

def _resolve_fourier_params(params: cl.Parameters) -> tuple[int, float]:
    """
    Resolve effective Fourier transformation parameters.

    This function converts boolean control flags in the parameter object into
    numerical values required for the Fourier transformation.

    Parameters
    ----------
    params : cl.Parameters
        Parameter object containing Fourier-related settings.

    Returns
    -------
    zero_filling : int
        Zero-filling factor. Returns ``params.zero_filling_factor`` if
        zero-filling is enabled, otherwise 1.
    reference_freq : float
        Reference frequency value. Returns ``params.reference_freq_value`` if
        reference frequency correction is enabled, otherwise 1.

    Notes
    -----
    This function separates user intent (boolean flags) from numerical values
    required by the processing backend.
    """
    zero_filling_factor = params.zero_filling_factor if params.zero_filling else 1
    reference_freq_value = params.reference_freq_value if params.reference_freq else 1
    return zero_filling_factor, reference_freq_value

def _apply_processing(data: cl.TransientNutations, params: cl.Parameters):
    """
    Apply processing steps to transient nutation data.

    This function executes a sequence of signal processing operations on the
    provided data object based on the flags and parameters defined in ``params``.

    Parameters
    ----------
    data : cl.TransientNutations
        Data object containing the transient nutation signal to be processed.
    params : cl.Parameters
        Parameter object specifying which processing steps to apply and their
        corresponding settings.

    Returns
    -------
    None
        The function modifies the ``data`` object in place.

    Notes
    -----
    The following processing steps may be applied (depending on ``params``):

    - Baseline correction
    - Signal reconstruction
    - Window functions:
        * Dolph-Chebyshev
        * Hamming
        * Kaiser
        * Sinebell
        * Lorentz-Gauss
    - Mean subtraction

    The order of operations follows the sequence defined in this function and
    may influence the final result.
    """
    # TODO Als Pipeline schreiben anstatt wie bisher und dabei Reihenfolge
    #  variabel machen? -> Finde Heraus, ob die Reihenfolge überhaupt Variabel
    #  sein darf oder ob das hier die einzig korrekte Reihenfolge ist

    if params.baseline_correction:
        data.baseline_correction(deg=params.baseline_correction_deg)

    if params.reconstruction:
        data.reconstruction()

    if params.wdw_chebwin:
        data.wdw_chebwin(params.chebwin_attenuation)

    if params.wdw_hamming:
        data.wdw_hamming(params.hamming_window_coefficient)

    if params.wdw_kaiser:
        data.wdw_kaiser(params.kaiser_window_shape_parameter)

    if params.wdw_sinebell:
        data.wdw_sinebell(params.sinebell_phase_shift)

    if params.wdw_lorentz_gauss:
        data.wdw_lorentz_gauss(params.tau, params.sigma)

    if params.mean_subtraction:
        data.mean_subtraction()