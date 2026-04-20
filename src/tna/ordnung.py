import numpy as np
import matplotlib.pyplot as plt
import functions as fun


def run_tna(data_path: str, params: fun.Parameters):
    data = fun.TransientNutations()

    # ---------- LOAD ----------
    if params.two_d:
        data.load_2d(data_path, params.prodel)
        data.choose_field(params.current_field)
    else:
        data.load_1d(data_path, params.prodel)

    # ---------- PROCESS ----------
    _apply_processing(data, params)

    # ---------- TRANSFORM ----------
    zf, rf = _resolve_fourier_params(params)
    data.fourier_transformation(zf, rf)

    return data

def run_tna_2d(data_path: str, params: fun.Parameters):
    data = fun.TransientNutations()

    data.load_2d(data_path, params.prodel)

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

def _resolve_fourier_params(params):
    zero_filling = params.zero_filling_factor if params.zero_filling else 1
    reference_freq = params.reference_freq_value if params.reference_freq else 1
    return zero_filling, reference_freq

def _apply_processing(data, params):
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



params = fun.Parameters(
    current_field=12020,
    wdw_lorentz_gauss=True,
    tau=530/3,
    sigma=1/(2*(530/3)),
    zero_filling = True,
    reference_freq = True,
)

path = "/home/quintes/NAS/Theresia/programme/transient_nutations/data/21_07_13_14_esenut_vs_B_LV_trinagulene_2_5mM_5eq_14dB_VG9_noAmp_h4n2_120K/test"

data = run_tna_2d(path, params)

plt.plot(data.freq, data.freq_signal[140])
