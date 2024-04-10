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

class File(Store):
  def _init(self, configuration, directions):
    self.files = {}

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

        os.symlink(StoreFront.makeDirection(self.directions, 'start').joinpath(self.path), symlink)
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

        os.symlink(StoreFront.makeDirection(self.directions, 'start').joinpath(self.path), symlink)
      else:
        shutil.copy(StoreFront.makeDirection(self.directions, lastRunTick).joinpath(self.path), StoreFront.makeDirection(self.directions))
        
    except:
      success = False
      
    return success    

  def _open(self, tick):
    if not StoreFront.formatTick(tick) in self.files:
      if self.readOnly or tick != StoreFront.getCurrentTick():
        self.files[StoreFront.formatTick(tick)] =  StoreFront.makeDirection(self.directions, tick).joinpath(self.path).open('r')
      else:
        self.files[StoreFront.formatTick(tick)] =  StoreFront.makeDirection(self.directions, tick).joinpath(self.path).open('+')

    return self.files[StoreFront.formatTick(tick)]

  def _close(self, tick, save, data):
    if StoreFront.formatTick(tick) in self.files:
      self.files[StoreFront.formatTick(tick)].close
      del self.files[StoreFront.formatTick(tick)]
