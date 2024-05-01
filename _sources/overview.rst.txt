Overview
========

TylerD is tile asset tool for generate title screens with NES nametables.


Installation
============

Just pip install it:

.. code-block:: bash

   pip install tylerd

Or poetry add this

.. code-block:: bash

   pip install tylerd


Usage
=====

Usage example.

.. code-block:: bash

    tylerd -p nes -f 2bpp_metatiles -b basename input.png -o output.s


That will generate an .s file to be used in your CC65 project.
For now it only supports NES as a platform and the 2bpp_metatiles file format.

Features
========

For now it only supports NES as a platform and the 2bpp_metatiles file format.
