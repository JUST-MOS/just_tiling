============
just_tiling
============

Introduction
============

This repository is intended for the scheduling of tiles for JUST galaxy/galaxy cluster survey.

.. _JUST: https://just.sjtu.edu.cn/EN/about.php



Installation
============

The package requires Python 3.8 or later and is installable with ``pip``.
For the fastest setup, install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/JUST-MOS/just_tiling.git

Install from source
-------------------

If you want to run the example scripts in place (they read data files from
relative paths inside the repository), clone the repository and install it in
editable mode:

.. code-block:: bash

    git clone https://github.com/JUST-MOS/just_tiling.git
    cd just_tiling
    pip install -e .

Editable mode keeps the source files where they are, so the examples can be
run directly from ``py/just_tiling/hyperuniform/`` and
``py/just_tiling/minimize_updf/``.

Install dependencies only
-------------------------

If you prefer to run the scripts without installing the package itself, just
install the runtime dependencies from ``requirements.txt``:

.. code-block:: bash

    pip install -r requirements.txt

The dependencies include ``numpy``, ``matplotlib``, ``healpy``, ``astropy``,
``scipy``, and ``joblib``.

Troubleshooting
---------------

``healpy`` and the compiled parts of ``numpy`` require pre-built wheels for
your Python version and operating system. If ``pip`` tries to build them from
source and fails, use a Python environment with available wheels (for
example, a recent conda_ environment) or install the dependencies first with
``pip install -r requirements.txt`` before installing ``just_tiling``.

.. _conda: https://docs.conda.io/en/latest/


Running the hyperuniform tiling example
=======================================

The hyperuniform tiling example is located at
``example/test_hyperuniform_tiling.py``. 

.. code-block:: bash

    cd example
    python test_hyperuniform_tiling.py

The script calls ``py/just_tiling/hyperuniform_tiling.py``, reads the galaxy catalog
``/home/Survey/JUST/mini/junyumock/lightcone_ra_0_90_dec_0_90_rmagcut20.5_cluster_mask.fits`` on GRAVITY and
writes the initial, intermediate, and final tile distributions as ``.npz``
files in ``./output``. Overwrite the default by ``-i`` or ``--input-catalog`` and ``-o`` or ``--output-dir`` plus your input file and your output directory.

Plots can be made by ``python plot_uniform.py`` in the same directory. It reads the tile files in ``./output`` and output the plots in the same directory in default. Use ``-i`` or ``--input-dir`` and ``-o`` or ``--output-dir`` to overwrite.


Running the minimize updf example
=================================

The tile-position optimization example is located at
``example/test_optimize_tile_pos.py``. It imports ``process_one_pixid`` from
the installed ``just_tiling.minimize_updf.optimize_tile_pos`` package and
expects the demo input file ``example/input/demo_4x4.npz``, so run it from
``example/``:

.. code-block:: bash

    cd example
    python test_optimize_tile_pos.py

By default the script writes its outputs to ``./output/``. You can override
this and other options from the command line:

.. code-block:: bash

    python test_optimize_tile_pos.py --odir ./my_output --n_jobs 4 --n_pix_jobs 2 --Npasses 3

Available options:

- ``--n_jobs``: total number of parallel workers available to the optimizer.
- ``--n_pix_jobs``: number of HEALPix pixels processed in parallel
  (inner workers per pixel will be ``n_jobs // n_pix_jobs``).
- ``--Npasses``: number of survey passes used to set tile move bounds.
- ``--odir``: output directory for the FITS table and diagnostic plot.
