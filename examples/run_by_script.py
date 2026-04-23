import tna.classes as cl
import tna.functions as fun
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent

# Example 1: two-dimensional transformation
params = cl.Parameters(
    two_d = True,
    path = BASE_DIR/"data"/"14_esenut_vs_B_LV_trinagulene_2-5mM_5eq_14dB_VG9_noAmp_h4n2_120K.DSC",
    baseline_correction = False,
    reconstruction = True,
    mean_subtraction = True,
    wdw_hamming = True,
    hamming_window_coefficient = 0.54,
    zero_filling = True,
    zero_filling_factor = 2,
    reference_freq = True,
    reference_freq_value = 1e7)

trans_nut = fun.run_tna_2d(params.path, params)

plt.figure()
plt.plot(trans_nut.freq, trans_nut.freq_signal[99])
plt.draw()

# Example 2: one-dimensional transformation at a single field slice
params = cl.Parameters(
    two_d = True,
    path = BASE_DIR/"data"/"14_esenut_vs_B_LV_trinagulene_2-5mM_5eq_14dB_VG9_noAmp_h4n2_120K.DSC",
    baseline_correction = False,
    reconstruction = True,
    mean_subtraction = True,
    wdw_hamming = True,
    hamming_window_coefficient = 0.54,
    zero_filling = True,
    zero_filling_factor = 2,
    reference_freq = True,
    reference_freq_value = 1e7,
    current_field=12020)

trans_nut = fun.run_tna(params.path, params)

plt.figure()
plt.plot(trans_nut.freq, trans_nut.freq_signal)
plt.show()