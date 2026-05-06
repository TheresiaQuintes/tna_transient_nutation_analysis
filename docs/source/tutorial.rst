Tutorial
========

Overview
--------
This tutorial demonstrates how to use the transient nutation analysis
package in a Python script.

The workflow consists of:

- defining analysis parameters
- running the processing pipeline
- visualising the results

Imports
-------
Start by importing the required modules:

.. code-block:: python

   import tna.classes as cl
   import tna.functions as fun
   from pathlib import Path
   import matplotlib.pyplot as plt

Define the data path:

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent


Example 1: Two-dimensional analysis
-----------------------------------

In this example, a full 2D dataset is processed and transformed into the
frequency domain.

1. Define parameters

   .. code-block:: python

      params = cl.Parameters(
          two_d=True,
          path=BASE_DIR / "data" / "your_dataset.DSC",
          baseline_correction=False,
          reconstruction=True,
          mean_subtraction=True,
          wdw_hamming=True,
          hamming_window_coefficient=0.54,
          zero_filling=True,
          zero_filling_factor=2,
          reference_freq=True,
          reference_freq_value=1e7
      )

2. Run the analysis

   .. code-block:: python

      trans_nut = fun.run_tna_2d(params.path, params)

3. Plot a frequency slice

   .. code-block:: python

      plt.figure()
      plt.plot(trans_nut.freq, trans_nut.freq_signal[99])
      plt.draw()


Example 2: One-dimensional analysis
-----------------------------------

In this example, a single field slice is selected from a 2D dataset and
processed as a one-dimensional signal.

1. Define parameters

   .. code-block:: python

      params = cl.Parameters(
          two_d=True,
          path=BASE_DIR / "data" / "your_dataset.DSC",
          baseline_correction=False,
          reconstruction=True,
          mean_subtraction=True,
          wdw_hamming=True,
          hamming_window_coefficient=0.54,
          zero_filling=True,
          zero_filling_factor=2,
          reference_freq=True,
          reference_freq_value=1e7,
          current_field=12020
      )

2. Run the analysis

   .. code-block:: python

      trans_nut = fun.run_tna(params.path, params)

3. Plot the spectrum

   .. code-block:: python

      plt.figure()
      plt.plot(trans_nut.freq, trans_nut.freq_signal)
      plt.show()


Notes
-----

- The parameter object controls the entire processing pipeline.
- Processing steps (e.g. reconstruction, window functions) are enabled
  via boolean flags.
- The order of processing steps follows the internal pipeline definition.
- The output object contains both time-domain and frequency-domain data.

Further information
-------------------

For a complete description of available parameters and data structures,
see :doc:`classes`.

The :class:`tna.classes.Parameters` class defines all configurable options
for the processing pipeline, while :class:`tna.classes.TransientNutations`
provides access to the resulting data.