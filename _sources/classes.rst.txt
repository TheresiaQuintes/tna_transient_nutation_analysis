classes
=======

Overview
--------
This module defines the core data structures for the analysis and processing
of transient nutation data.

It provides:

- the ``TransientNutations`` class for representing and processing
  experimental data (loading, pre-processing, Fourier transformation)
- the ``Parameters`` class for configuring analysis and processing steps

The separation of data and parameters enables a clear and reproducible
analysis pipeline.

Contents
--------

.. autosummary::
   :toctree: generated/

   tna.classes.TransientNutations
   tna.classes.Parameters
