# Transient Nutation Analysis (TNA)

A Python package for the analysis of transient nutation data, including
pre-processing, signal reconstruction, and Fourier transformation.

The package provides both a scripting interface and a graphical user interface
for interactive data analysis.

---

## Features

- Processing of 1D and 2D transient nutation datasets
- Configurable preprocessing pipeline:
  - baseline correction
  - autoregressive signal reconstruction
  - window functions (Hamming, Kaiser, Dolph–Chebyshev, Sine-bell, Lorentz–Gauss)
  - mean subtraction
- Fourier transformation with zero-filling and frequency scaling
- GUI for interactive data exploration
- Script-based workflow for reproducible analysis

---

## Installation

### Requirements

- Python 3.9 or higher
- `pip`

### Setup

```bash
git clone https://github.com/TheresiaQuintes/tna_transient_nutation_analysis
cd tna_transient_nutation_analysis
pip install .
```

For a more detailed setup (including virtual environments), see the documentation.

---
## Quick start
```python
import tna.classes as cl
import tna.functions as fun
from pathlib import Path
import matplotlib.pyplot as plt

params = cl.Parameters(
    two_d=True,
    path=Path("your_dataset.DSC"),
    reconstruction=True,
    mean_subtraction=True,
    wdw_hamming=True,
    zero_filling=True,
    reference_freq=True
)

data = fun.run_tna_2d(params.path, params)

plt.plot(data.freq, data.freq_signal[0])
plt.show()

```
---
## GUI

Start the graphical interface with:

```bash
tna
```
---
## Documentation

Full documentation is available at:

https://theresiaquintes.github.io/tna_transient_nutation_analysis/
