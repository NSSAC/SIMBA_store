SIMBA Schedule
==============
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

The SIMBA schedule comprises modules, which are flexibly scheduled at certain ticks (time points) during a simulation. Furthermore each module has fine grained options on how to execute the module. The later utilizes `parsl <https://parsl.readthedocs.io/en/stable/index.html>`_ allowing SIMBA to execute the modules on different computing resources.

.. |simba-store-front-specification-synopsis| replace:: Specification: how to specify a SIMBA store front. 
.. _`simba-store-front-specification-synopsis`: `simba-store-front-specification`_

.. _simba-store-front-specification:

Specification
-------------

.. admonition:: Synopsis

   |simba-store-front-specification-synopsis|

The schedule JSON configuration file has two attributes: ``schedule`` and ``commonData``. 

.. list-table:: Store Front.
  :name: store-front-store-front
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | schedule
    - | array 
    - | items consist of all of: 
      | :ref:`schedule-module-details`
      | :ref:`schedule-module-schedule`
      | `Parsl Module. <../schema/schedule.html#parsl-module>`_
  * - | commonData
    - | object 
    - | Common data provided to all modules upon execution (default: none)

.. list-table:: Module Identification and Details.
  :name: schedule-module-details
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | name
    - | string 
    - | The name of the module.
  * - | command
    - | string 
    - | The command to execute the module.
  * - | updateCommonData
    - | Boolean
    - | Specifies whether this module may update common data 
      | (default: false)
  * - | moduleData
    - | object
    - | Module specific data provided to the module upon execution 
      | (default: none)

.. list-table:: Module Schedule. 
  :name: schedule-module-schedule
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | priority
    - | number 
    - | Priority of Module Execution, higher priority is executed first and  
      | priorities must be unique.
  * - | startTick
    - | string 
    - | The current tick at which the module is executed first
      | (default: -infinity).
  * - | endTick
    - | integer
    - | The targetTick for which the module is executed last
      | (default: infinity).
  * - | tickIncrement
    - | positive integer
    - | The tick increment in which the module is executed (default: 1).


The normative JSON schema can be found at:  :doc:`Schedule Schema </schema/schedule>` 

.. _simba-store-front-examples:

Examples
--------

Please see :doc:`Examples </examples/example>` 