gui_controller
==============

Overview
--------
This module implements the controller layer of the TNA graphical user
interface.

It connects the Qt-based view with the data model and manages all user
interactions, including:

- data loading and visualisation
- processing pipeline execution
- parameter updates from the GUI
- plot management using Matplotlib

The controller follows a model–view–controller (MVC)-like structure, where
the ``TNAController`` acts as the central interface between user actions and
data processing.

Contents
--------

.. autosummary::
   :toctree: generated/

   tna.gui.gui_signals.TNAController
   tna.gui.gui_signals.safe_slot
   tna.gui.gui_signals.reset_plot