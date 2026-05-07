Processing theory
=================

Overview
--------
This page summarises the physical and signal-processing concepts underlying
the preprocessing steps used in transient nutation analysis.

The processing chain is designed to improve signal quality, suppress noise,
and prepare the time-domain signal for Fourier transformation.

Baseline correction
-------------------
Baseline correction removes slowly varying offsets in the time-domain signal.

These offsets typically originate from instrumental drift, background
contributions, or imperfect phase cycling.

A polynomial of adjustable degree is fitted to the signal and subtracted.
The default is a linear fit (degree = 1), which removes constant and linear
drifts.

Signal reconstruction
---------------------
Signal reconstruction extends the time-domain signal using an
autoregressive (Yule–Walker) model.

This method estimates missing or unmeasured data points based on the
statistical structure of the measured signal.

It is particularly useful for:
- truncated signals
- strongly damped oscillations
- improving Fourier transform stability

The reconstruction is performed on the time-reversed signal to improve
prediction stability and then mapped back to the original time axis.

Window functions
-----------------

Window functions are applied to reduce spectral leakage caused by finite
time-domain sampling and abrupt signal truncation.

Dolph–Chebyshev window
~~~~~~~~~~~~~~~~~~~~~~
Provides optimal control of sidelobe suppression for a given attenuation level.

The attenuation parameter (in dB) controls the trade-off between:
- spectral leakage suppression
- main-lobe broadening

Higher attenuation results in smoother spectra but reduced resolution.

Hamming window
~~~~~~~~~~~~~~
A general-purpose apodisation function defined by a weighted cosine shape.

The coefficient (typically ~0.54) controls the balance between:
- sidelobe suppression
- spectral resolution

Kaiser window
~~~~~~~~~~~~~
A flexible window function with a tunable shape parameter.

The parameter controls the trade-off between:
- resolution (narrow main lobe)
- noise suppression (low sidelobes)

It is often used when adaptive control of spectral properties is required.

Sine-bell window
~~~~~~~~~~~~~~~~~
Applies a smooth sinusoidal taper to the signal.

The phase shift parameter controls the starting point of the window and
therefore the degree of signal suppression at early times.

This improves spectral resolution but reduces signal-to-noise ratio.

Lorentz–Gauss window
~~~~~~~~~~~~~~~~~~~~
Combines Lorentzian decay compensation with Gaussian broadening control.

The parameters have physical interpretations:

- ``tau`` corresponds to an effective transverse relaxation time (T2-like
  behaviour)
- ``sigma`` controls Gaussian damping and resolution enhancement

This window is commonly used for damped oscillatory systems.

Mean subtraction
-----------------
Mean subtraction removes the DC component of the signal.

This eliminates the zero-frequency peak in the Fourier spectrum and improves
dynamic range in frequency space.

Fourier transformation
----------------------
The discrete Fourier transform converts the time-domain signal into the
frequency domain.

Zero-filling is used to increase spectral interpolation density. It does not
add physical information but improves visual frequency resolution.

The frequency axis is computed from the sampling interval of the time signal.

A reference frequency scaling may be applied to normalise the spectrum to a
physically meaningful frequency scale.