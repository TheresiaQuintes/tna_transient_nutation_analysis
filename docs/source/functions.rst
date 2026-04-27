functions
=========

Overview
--------
This module provides high-level functions for running transient nutation
analysis workflows.

It includes:

- functions for processing single datasets (1D or selected slices of 2D data)
- functions for processing full 2D datasets
- internal utilities for configuring Fourier transformation and processing steps

The module connects data structures and parameter configurations to form a
complete analysis pipeline.

Contents
--------

.. autosummary::
   :toctree: generated/

   tna.functions.run_tna
   tna.functions.run_tna_2d
   tna.functions._apply_processing
   tna.functions._resolve_fourier_params