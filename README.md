# SIMBA_store
Distributed and extensible data storage for SIMBA. The purpose is to provide the current state and history of the system. 

Each store has a schema which defines keys and values of the stored data. For the schema we will use [Frictionless Data](https://github.com/frictionlessdata/specs)

Stores can be added to other stores allowing the creation of hierarchies, e.g., time dependent geospatial data. Which can be implemented as a parrent store which comprises only the key time and added geospatial data store which contains keys logintude and latitude as well as data associated with those keys.

## API
Each store provides the follow methods
* __add__`(SIMBA_store)` Add a store
* __default__`([{keys}, ...])` Set the values for the provided keys to default.
* __set__`([{keys, values}, ...])` Set the values for the given keys. Note: multiple key value pairs might be updated at the same time
* __get__`([{keys}, ...], {values})` Retrieve the requested values for the requested key(s).
* __copy__`()` Copy a store. Note: all child stores will be copied too.
