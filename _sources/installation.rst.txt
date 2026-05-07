Getting started
===============

Overview
--------
This section describes how to install and run the transient nutation
analysis package.

Requirements
------------
The following software is required:

- Python 3.9 or higher
- ``pip``
- a terminal or command line interface

Installation
------------
It is recommended to install the package in a virtual environment.

1. Create a virtual environment

   Using ``venv``:

   .. code-block:: bash

      python -m venv venv

   Or using ``conda``:

   .. code-block:: bash

      conda create -n tna python=3.9

2. Activate the environment

   Using ``venv``:

   .. code-block:: bash

      source venv/bin/activate

   On Windows:

   .. code-block:: bash

      venv\Scripts\activate

   Using ``conda``:

   .. code-block:: bash

      conda activate tna

3. Clone the repository

   .. code-block:: bash

      git clone https://github.com/TheresiaQuintes/tna_transient_nutation_analysis

4. Navigate to the project directory

   .. code-block:: bash

      cd tna_transient_nutation_analysis

5. Install the package

   .. code-block:: bash

      pip install .

Running the application
-----------------------
After installation, the graphical user interface can be started via:

.. code-block:: bash

   tna-gui