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
import shutil
from pathlib import Path
from simbastore.storefront import StoreFront
from simbastore.store import Store
from pandas import read_csv
from pandas import DataFrame
from pandas.api.extensions import no_default
import numpy as np

class CSV(Store):
  def _init(self, configuration, directions):
    self.header = 'infer'
    self.names = no_default
    self.dtype = None
    self.index_col = None
    self.dataFrames = {}

    if 'schema' in configuration:
      schema = configuration['schema']

      if 'fields' in schema:
        self.header = 0
        self.dtype = {}
        self.names = []

        for f in schema['fields']:
          self.names.append(f['name'])
          self.dtype[f['name']] = np.float64

      if 'primaryKey' in schema:
        self.index_col = []

        for k in schema['primaryKey']:
          self.index_col.append(k)

  def _start(self, currentTick, currentTime):
    success = True
    
    try:
      shutil.copy(StoreFront.resolvePath(self.path), StoreFront.makeDirection(self.directions))
        
    except:
      success = False
      
    return success    

  def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    success = True
    
    try:
      if self.readOnly:
        symlink = StoreFront.makeDirection(self.directions).joinpath(self.path)

        if symlink.exists():
          os.remove(symlink)

        os.symlink(self.path, symlink)
      else:
        shutil.copy(StoreFront.makeDirection(self.directions, lastRunTick).joinpath(self.path), StoreFront.makeDirection(self.directions).joinpath(self.path))
        
    except:
      success = False
      
    return success    

  def _end(self, lastRunTick, lastRunTime, endTick, endTime):
    success = True
    
    try:
      if self.readOnly:
        symlink = StoreFront.makeDirection(self.directions).joinpath(self.path)

        if symlink.exists():
          os.remove(symlink)

        os.symlink(self.path, symlink)
      else:
        shutil.copy(StoreFront.makeDirection(self.directions, lastRunTick).joinpath(self.path), StoreFront.makeDirection(self.directions))
        
    except:
      success = False
      
    return success    

  def _open(self, tick):
    if not StoreFront.formatTick(tick) in self.dataFrames:
      self.dataFrames[StoreFront.formatTick(tick)] = read_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path), header = self.header, names = self.names, index_col = self.index_col, dtype = self.dtype)

    return self.dataFrames[StoreFront.formatTick(tick)]

  def _close(self, tick, save, data):
    if StoreFront.formatTick(tick) in self.dataFrames:
      if save and tick == StoreFront.getCurrentTick() and not self.readOnly:
        if isinstance(data, DataFrame):
          data.to_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path))
        else:
          self.dataFrames[StoreFront.formatTick(tick)].to_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path))
        
      del self.dataFrames[StoreFront.formatTick(tick)]
