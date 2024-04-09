.. SIMBA documentation master file, created by
   sphinx-quickstart on Fri Feb 17 11:11:18 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SIMBA Store documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

SIMBA is a framework for performing multi-scale simulations in an HPC environment. Each simulation step can involve multiple modules which update the current state of the system. The order and the frequency in which these modules are executed is handled by a flexible :doc:`store front <configuration/store-front>`

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   quickstart/get-started.rst

.. toctree::
   :maxdepth: 2
   :caption: Configuration

   configuration/store.rst
   configuration/store-front.rst

.. toctree::
   :maxdepth: 2
   :caption: Examples
   
   examples/example.rst
   
.. toctree::
   :maxdepth: 2
   :caption: Schema
   
   schema/store-front.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
