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
    shutil.copy(StoreFront.resolvePath(self.path), StoreFront.makeDirection(self.directions))

  def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    if self.readOnly:
      symlink = StoreFront.makeDirection(self.directions).joinpath(self.path)

      if symlink.exists():
        os.remove(symlink)

      os.symlink(StoreFront.makeDirection(self.directions, 'start').joinpath(self.path), symlink)
    else:
      shutil.copy(StoreFront.makeDirection(self.directions, lastRunTick).joinpath(self.path), StoreFront.makeDirection(self.directions).joinpath(self.path))

  def _end(self, lastRunTick, lastRunTime, endTick, endTime):
    if self.readOnly:
      symlink = StoreFront.makeDirection(self.directions).joinpath(self.path)

      if symlink.exists():
        os.remove(symlink)

      os.symlink(StoreFront.makeDirection(self.directions, 'start').joinpath(self.path), symlink)
    else:
      shutil.copy(StoreFront.makeDirection(self.directions, lastRunTick).joinpath(self.path), StoreFront.makeDirection(self.directions))

  def _open(self, tick):
    if not str(tick) in self.dataFrames:
      self.dataFrames[str(tick)] = read_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path), header = self.header, names = self.names, index_col = self.index_col, dtype = self.dtype)

    return self.dataFrames[str(tick)]

  def _close(self, tick, save, data):
    if str(tick) in self.dataFrames:
      if save and tick == StoreFront.getCurrentTick() and not self.readOnly:
        if isinstance(data, DataFrame):
          data.to_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path))
        else:
          self.dataFrames[str(tick)].to_csv(StoreFront.makeDirection(self.directions, tick).joinpath(self.path))
        
      del self.dataFrames[str(tick)]
