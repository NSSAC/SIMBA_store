# BEGIN: Copyright 
# Copyright (C) 2024 Rector and Visitors of the University of Virginia 
# All rights reserved 
# END: Copyright 

# BEGIN: License 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#   http://www.apache.org/licenses/LICENSE-2.0 
# END: License 

import sys
import os
from pathlib import Path
import json
from jsonschema import validate

class StoreFront:
  __configuration = None
  __root = None
  __stores = {}
  __currentTick = None
  __tickFormat = '{}'
  
  @classmethod
  def load(cls, configuration):
    cls.__configuration = Path(configuration).absolute()

    try:
      jsonFile = open(cls.__configuration,'r')

    except:
      sys.exit("ERROR: File '" + configuration + "' does not exist.")

    dictionary = json.load(jsonFile)

    jsonFile.close()

    cls.__root = cls.resolvePath(dictionary['path'])

    if not cls.__root.exists():
      os.mkdir(cls.__root)
      
    if 'stores' in dictionary:
      cls.__stores = cls.createStores(dictionary['stores'])

    return

  @classmethod
  def get(cls, store):
    if store in cls.__stores:
      return cls.__stores[store]

    return None

  @classmethod
  def setTickFormat(cls, tickFormat):
    cls.__tickFormat = tickFormat

  @classmethod
  def formatTick(cls, tick):
    return cls.__tickFormat.format(tick)

  @classmethod
  def setCurrentTick(cls, tick):
    cls.__currentTick = tick

  @classmethod
  def getCurrentTick(cls):
    return cls.__currentTick

  @classmethod
  def root(cls):
    return cls.__root

  @classmethod
  def createStores(cls, ss, directions = []):
    from simbastore.file import File
    from simbastore.csv import CSV

    stores = {}

    for s in ss:
      store = None

      if s['type'] == 'file':
        store = File(s, directions)

      if s['type'] == 'csv':
        store = CSV(s, directions)

      if store == None:
        continue

      if store.getName() in stores:
        sys.exit("ERROR: Store names must be unique in '" + str(cls.__configuration) + "'.")

      stores[store.getName()] = store

    return stores

  @classmethod
  def resolvePath(cls, path):
    if Path(path).is_absolute():
      return path

    if cls.__configuration and cls.__configuration.parent.joinpath(path).exists():
      return cls.__configuration.parent.joinpath(path)

    if cls.__root and cls.__root.joinpath(path).exists():
      return cls.__root.joinpath(path)

    if Path.cwd().joinpath(path).exists():
      return Path.cwd().joinpath(path)

    return Path(path)

  @classmethod
  def makeDirection(cls, directions, tick = None):
    if tick == None:
      Direction = cls.__root.joinpath(cls.__currentTick)
    elif isinstance(tick, int):
      Direction = cls.__root.joinpath(cls.formatTick(tick))
    else:
      Direction = cls.__root.joinpath(tick)
      
    for d in directions:
      Direction = Direction.joinpath(d)

    return Direction

  @classmethod
  def execute(cls, configuration):
    try:
      jsonFile = open(configuration,'r')

    except:
      sys.exit("ERROR: File '" + configuration + "' does not exist.")

    dictionary = json.load(jsonFile)

    jsonFile.close()

    if 'commonData' in dictionary and 'storeFront' in dictionary['commonData']:
        dictionary['commonData']['storeFront'] = str(cls.__configuration)
    
    if (dictionary['mode'] == 'start'):
        success = StoreFront.start(dictionary['currentTick'], dictionary['currentTime'])

    if (dictionary['mode'] == 'step'):
        success = StoreFront.step(dictionary['lastRunTick'], dictionary['lastRunTime'], dictionary['currentTick'], dictionary['currentTime'], dictionary['targetTick'], dictionary['targetTime'])

    if (dictionary['mode'] == 'end'):
        success = StoreFront.end(dictionary['lastRunTick'], dictionary['lastRunTime'], dictionary['currentTick'], dictionary['currentTime'])

    if 'commonData' in dictionary and 'storeFront' in dictionary['commonData']:
        dictionary['commonData']['storeFront'] = str(cls.__configuration)
        
    dictionary['status'] = 'success' if success else 'failed'
    jsonFile = open(dictionary['statusFile'],'w')
    json.dump(dictionary, jsonFile, indent=2)
    jsonFile.close()

    return success
  
  @classmethod
  def start(cls, currentTick, currentTime):
    success = True
    
    try:
      cls.__currentTick = cls.formatTick(currentTick)
      direction = cls.makeDirection([])

      if not direction.exists():
        os.mkdir(direction)

      symlink = cls.makeDirection([], 'start')

      if symlink.exists():
        os.remove(symlink)

      os.symlink(cls.__currentTick, symlink)

      for store in cls.__stores.values():
        success &= store.start(currentTick, currentTime)
        
    except:
      success = False
                      
    return success    

  @classmethod
  def step(cls, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    success = True
    
    try:
      cls.__currentTick = cls.formatTick(targetTick)
      direction = cls.makeDirection([])

      if not direction.exists():
        os.mkdir(direction)

      for store in cls.__stores.values():
        success &= store.step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)
        
    except:
      success = False
      
    return success    

  @classmethod
  def end(cls, lastRunTick, lastRunTime, endTick, endTime):
    success = True
    
    try:
      cls.__currentTick = cls.formatTick(endTick)
      direction = cls.makeDirection([])

      if not direction.exists():
        os.mkdir(direction)

      symlink = cls.makeDirection([], 'end')

      if symlink.exists():
        os.remove(symlink)

      os.symlink(cls.__currentTick, symlink)
      
      for store in cls.__stores.values():
        store.end(lastRunTick, lastRunTime, endTick, endTime)
        
    except:
      success = False
      
    return success    

