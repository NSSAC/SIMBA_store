SIMBA Store Front
=================
**Contents:**

* |simba-store-front-introduction-synopsis|_
* |simba-store-front-specification-synopsis|_
* :ref:`simba-store-front-examples`

.. |simba-store-front-introduction-synopsis| replace:: SIMBA Store Front configuration.
.. _`simba-store-front-introduction-synopsis`: `simba-store-front-introduction`_

.. _simba-store-front-introduction:

Introduction
------------

.. admonition:: Synopsis

   |simba-store-front-introduction-synopsis|

The SIMBA Store Front comprises stores. Each store is an independent data storage provider optionally containing further stores to allow hierarchical composition of data.

.. |simba-store-front-specification-synopsis| replace:: Specification: how to specify a SIMBA store front. 
.. _`simba-store-front-specification-synopsis`: `simba-store-front-specification`_

.. _simba-store-front-specification:

Specification
-------------

.. admonition:: Synopsis

   |simba-store-front-specification-synopsis|

The Store Front JSON configuration file has two properties: ``path`` and ``stores``. 

.. list-table:: Store Front.
  :name: store-front-store-front
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | path
    - | string 
    - | a directory path where the store front will be physically located
  * - | stores
    - | array 
    - | a list of stores 

The normative JSON schema can be found at:  :doc:`Store Front Schema </schema/store-front>` 

.. _simba-store-front-examples:

Examples
--------

Please see :doc:`Examples </examples/example>` 