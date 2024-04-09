SIMBA Driver
============
**Contents:**

* |simba-store-introduction-synopsis|_
* |simba-store-specification-synopsis|_
* :ref:`simba-store-examples`

.. |simba-store-introduction-synopsis| replace:: SIMBA driver configuration.
.. _`simba-store-introduction-synopsis`: `simba-store-introduction`_

.. _simba-store-introduction:

Introduction
------------

.. admonition:: Synopsis

   |simba-store-introduction-synopsis|

The SIMBA driver configuration specifies the run parameters of a the simulation

.. |simba-store-specification-synopsis| replace:: Specification: how to specify the simulation parameters. 
.. _`simba-store-specification-synopsis`: `simba-store-specification`_

.. _simba-store-specification:

Specification
-------------

.. admonition:: Synopsis

   |simba-store-specification-synopsis|

A SIMBA store manages tick dependent data and provides access to it. 


.. list-table:: Store Specification. 
  :name: store-specification
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | runId
    - | string 
    - | A unique ID identifying the run to be executed.
  * - | cellId
    - | string 
    - | A ID identifying the currently running experimental setup.
  * - | initialTick
    - | integer
    - | The initial tick. Default: 0
  * - | initialTime
    - | string
    - | The initial time (ISO data time format)
  * - | endTime
    - | string
    - | The simulation stops once ``initialTime`` plus all accumulated 
      | durations (``tickDuration``) exceeds the endTime
  * - | continueFromTick
    - | string
    - | This attribute allows to continue a previously executed simulation 
      | at the given tick
  * - | scheduleIntervals
    - | array
    - | The intervals are executed in the listed order and must not overlap. 
      | At least one interval must be defined.


The intervals in the schedule are executed in order. This implies that the ``endTick`` attributes must be increasing. The only required attribute is ``tickDuration``.

.. list-table:: Schedule Interval. 
  :name: store-schedule-interval
  :header-rows: 1

  * - | Name
    - | Type 
    - | Description
  * - | startTick
    - | integer 
    - | Start tick of the interval. Default: ``initialTick`` or previous ``endTick + 1``
  * - | endTick
    - | string 
    - | End tick of the interval. Default: infinity
  * - | tickDuration
    - | string
    - | Time duration per tick of the interval (ISO duration format rfc3339)

The normative JSON schema can be found at:  :doc:`Store Front Schema </schema/store-front>` 

.. _simba-store-examples:

Examples
--------

Example using a 3 intervals with different simulation duration times.

.. code-block:: JSON

  {
    "$schema": "https://raw.githubusercontent.com/NSSAC/SIMBA_driver/schema/driver.json",
    "endTime" : "PT1209600S",
    "scheduleIntervals" : [
      {
        "endTick" : 6,
        "tickDuration" :  "PT600S"
      },
      {
        "endTick" : 100,
        "tickDuration" :  "PT1800S"
      },
      {
        "tickDuration" :  "PT3600S"
      }
    ]
  }

