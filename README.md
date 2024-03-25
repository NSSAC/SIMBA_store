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


## HSM Comments/notes ##


## Data for SIMBA modules ##

1. File on location file system
2. Database
3. Remove file-like data (accessed through, e.g., globus or other API)
4. Streaming data data

For SIMBA's immediate use, data types 1 and 2 seem moste important. Type 3 may apply to some of the geo/hydrological data, at least in the way they are set up (where do they get their initial data?) Type 3 may be used to transfer data from Box to Rivanna for use with modules and pipelines. Option 3 may also be what is applied to stage data for the equite atlas (from Rivanna to Box). For now, type 4 seems less relevant.

## Types of data stores ##
(see, e.g., https://medium.com/swlh/the-5-data-store-patterns-data-lakes-data-hubs-data-virtualization-data-federation-data-27fd75486e2c)

- Lakes
- Hubs
- Virtualization/Federation
- Warehouse
- Operational data store
