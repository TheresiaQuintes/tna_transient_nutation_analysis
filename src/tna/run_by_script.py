#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 10:52:36 2023

@author: quintes
"""

import classes as fun
import matplotlib.pyplot as plt

params = fun.Parameters(current_time=2)

# Variablen
prodel = False
two_d = True
path = "/home/quintes/NAS/Theresia/programme/transient_nutations/data/21_07_13_14_esenut_vs_B_LV_trinagulene_2_5mM_5eq_14dB_VG9_noAmp_h4n2_120K/test"

baseline_correction = 0
reconstruction = False
mean_subtraction = False

wdw_chebwin = False
chebwin_attenuation = 45

wdw_hamming = False
hamming_window_coefficient = 0.54

wdw_kaiser = False
kaiser_window_shape_parameter = 2

wdw_sinebell = False
sinebell_phase_shift = 0

wdw_lorentz_gauss = True
tau = 530/3
sigma = 1/(2*tau)

zero_filling = 2
reference_freq = 1e7


# Script 1D
data = fun.TransientNutations()

if two_d is True:
    data.load_2d(path, prodel)
    data.choose_field(12020)
elif two_d is False:
    data.load_1d(path, prodel)

if baseline_correction > 0:
    data.baseline_correction(deg=baseline_correction)

if reconstruction is True:
    data.reconstruction()

if wdw_chebwin is True:
    data.wdw_chebwin(chebwin_attenuation)

if wdw_hamming is True:
    data.wdw_hamming(hamming_window_coefficient)

if wdw_kaiser is True:
    data.wdw_kaiser(kaiser_window_shape_parameter)

if wdw_sinebell is True:
    data.wdw_sinebell(sinebell_phase_shift)

if wdw_lorentz_gauss is True:
    data.wdw_lorentz_gauss(tau, sigma)

if mean_subtraction is True:
    data.mean_subtraction()

data.fourier_transformation(zero_filling, reference_freq)

plt.plot(data.freq, data.freq_signal)

#%%
# Script 2D

data2 = fun.TransientNutations()

data2.load_2d(path, prodel)
ft_spc = []

for field_index in range(len(data2.field)):
    data2.t_signal = data2.spc[field_index]
    data2.t = data2.time

    if baseline_correction > 0:
        data2.baseline_correction(deg=baseline_correction)

    if reconstruction is True:
        data2.reconstruction()

    if wdw_chebwin is True:
        data2.wdw_chebwin(chebwin_attenuation)

    if wdw_hamming is True:
        data2.wdw_hamming(hamming_window_coefficient)

    if wdw_kaiser is True:
        data2.wdw_kaiser(kaiser_window_shape_parameter)

    if wdw_sinebell is True:
        data2.wdw_sinebell(sinebell_phase_shift)

    if wdw_lorentz_gauss is True:
        data2.wdw_lorentz_gauss(tau, sigma)

    if mean_subtraction is True:
        data2.mean_subtraction()

    data2.fourier_transformation(zero_filling, reference_freq)
    ft_spc.append(data2.freq_signal)

ft_spc = fun.np.array(ft_spc)
