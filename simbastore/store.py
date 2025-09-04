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

import os
from pathlib import Path
from abc import ABCMeta, abstractmethod
from simbastore.storefront import StoreFront

class Store:
  __metaclass__ = ABCMeta

  def __init__(self, configuration, directions = []):
    self.name = configuration['name']
    self.directions = directions[:]
    self.directions.append(configuration['name'])
    self.path = configuration['path']
    self.initialPath = configuration['initialPath']
    
    if 'readOnly' in configuration:
      self.readOnly = configuration['readOnly']
    else:
      self.readOnly = False

    if 'table' in configuration:
      self.table = configuration['table']
    else:
      self.table = None

    self.stores = {}

    if 'stores' in configuration:
      self.stores = StoreFront.createStores(configuration['stores'], self.directions)

    self._init(configuration, directions)

  def getName(self):
    return self.name

  def start(self, currentTick, currentTime):
    success = True
    
    try:
      direction = StoreFront.makeDirection(self.directions)

      if not direction.exists():
        os.mkdir(direction)

      success &= self._start(currentTick, currentTime)

      for store in self.stores.values():
        success &= store.start(currentTick, currentTime)
        
    except:
      success = False
      
    return success    

  def step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    success = True
    
    try:
      direction = StoreFront.makeDirection(self.directions)

      if not direction.exists():
        os.mkdir(direction)

      success &= self._step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)

      for store in self.stores.values():
        success &= store.step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)
        
    except:
      success = False
      
    return success    

  def end(self, lastRunTick, lastRunTime, endTick, endTime):
    success = True
    
    try:
      direction = StoreFront.makeDirection(self.directions)

      if not direction.exists():
        os.mkdir(direction)

      success &= self._end(lastRunTick, lastRunTime, endTick, endTime)

      for store in self.stores.values():
        success &= store.end(lastRunTick, lastRunTime, endTick, endTime)
        
    except:
      success = False
      
    return success    

  def open(self, tick = None):
    if tick == None:
      tick = StoreFront.getCurrentTick()

    return self._open(tick)

  def close(self, tick = None, save = False, data = None):
    if tick == None:
      tick = StoreFront.getCurrentTick()

    return self._close(tick, save, data)

  @abstractmethod
  def _init(self, configuration, directions):
    pass

  @abstractmethod
  def _start(self, currentTick, currentTime):
    return False

  @abstractmethod
  def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    return False

  @abstractmethod
  def _end(self, lastRunTick, lastRunTime, endTick, endTime):
    return False

  @abstractmethod
  def _open(self, tick):
    pass

  @abstractmethod
  def _close(self, tick, save, data):
    pass
