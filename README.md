# SIMBA_store
Distributed and extensible data storage for SIMBA. The purpose is to provide the current state and history of the system. 

Each store has a schema which defines keys and values of the stored data. For the schema we will use [Frictionless Data](https://github.com/frictionlessdata/specs)

Stores can be added to other stores allowing the creation of hierarchies, e.g., time dependent geospatial data. Which can be implemented as a parrent store which comprises only the key time and added geospatial data store which contains keys logintude and latitude as well as data associated with those keys.

## API
Each store provides the following methods
* __add__`(SIMBA_store)` Add a store
* __default__`([{keys}, ...])` Set the values for the provided keys to default.
* __set__`([{keys, values}, ...])` Set the values for the given keys. Note: multiple key value pairs might be updated at the same time
* __get__`([{keys}, ...], {values})` Retrieve the requested values for the requested key(s).
* __copy__`([{old_keys, new_keys}, ...])` Copy a store if provided old_keys, will be replaced with new. Note: all child stores will be copied too.


## Comments/notes ##


## Data for SIMBA modules ##

1. File on location file system
2. Database
3. Remove file-like data (accessed through, e.g., globus or other API)
4. Streaming data data

For SIMBA's immediate use, data types 1 and 2 seem moste important. Type 3 may apply to some of the geo/hydrological data, at least in the way they are set up (where do they get their initial data?) Type 3 may be used to transfer data from Box to Rivanna for use with modules and pipelines. Option 3 may also be what is applied to stage data for the equite atlas (from Rivanna to Box). For now, type 4 seems less relevant.


## Delineation of data used with SIMBA modules ##

_Initial data v. dynamic data_: initial data is provided prior to the start of any SIMBA runs. If such data involves processing, it is recommended that the processing is captured as a script or in some other manner supporting its reconstruction. 

_Dependencies: internal data v. external data_: a data set (or source) is internal with respect to a specific module if that module provides (or generates) that data. Otherwise, the data is external to that module.  


## Types of data stores ##
(see, e.g., https://medium.com/swlh/the-5-data-store-patterns-data-lakes-data-hubs-data-virtualization-data-federation-data-27fd75486e2c)

- Lakes
- Hubs
- Virtualization/Federation
- Warehouse
- Operational data store

## CoPe examples ##

- Storm inundation data: collected from Box; initial data for BI internal purposes. CSV files.
- Road network data: DB data generated as initial data through small pipeline. Files on locaal disk.
- POI data: initial data generated as query against DB. CSV and JSON files on disk.
- River/road crossing data: data generated as spatial query of road data (in DB) against external creek/river data (found by Dawen). Only for VA. Files on disk.
- Population data for ESVA+: data from the detailed population pipeline. CSV files on disk.
- Inundation impacted network: dynamic and is stored as a file on disk. Potentially one instance generated per iteration.

Workflow example for Ashik's cases: at tick 5:
1. Get road network from tick 0
2. Get inundation time series (tick 0) at specified point in time.
3. Perform join of 1 and 2, then computed updated speed limits.
4. Write network from 3 to disk (somewhere) and record that written data with data store for tick 5. Should it write directly to data store?
5. Determine travel time for each household to nearest hospital location. Write/record.

## Questions: ##

- How to organize tick-indexed dynamic data with respect to data stores?
- Creation of data stores:
  - what are common patterns?
  - When initial data is collected:
    - Are data stored created?
    - If yes, how is such data recorded? E.g., so that it can be used at runtime.
- Data store and tick-indexing?
- Data store and data access:
  - To file data? File data belonging to a given tick?
  - Database tables? Database tables belonging to a given tick? 
