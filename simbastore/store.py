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
    direction = StoreFront.makeDirection(self.directions)

    if not direction.exists():
      os.mkdir(direction)

    self._start(currentTick, currentTime)

    for store in self.stores.values():
       store.start(currentTick, currentTime)

  def step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    direction = StoreFront.makeDirection(self.directions)

    if not direction.exists():
      os.mkdir(direction)

    self._step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)

    for store in self.stores.values():
       store.step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)

  def end(self, lastRunTick, lastRunTime, endTick, endTime):
    direction = StoreFront.makeDirection(self.directions)

    if not direction.exists():
      os.mkdir(direction)

    self._end(lastRunTick, lastRunTime, endTick, endTime)

    for store in self.stores.values():
       store.end(lastRunTick, lastRunTime, endTick, endTime)

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
    pass

  @abstractmethod
  def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    pass

  @abstractmethod
  def _end(self, lastRunTick, lastRunTime, endTick, endTime):
    pass

  @abstractmethod
  def _open(self, tick):
    pass

  @abstractmethod
  def _close(self, tick, save, data):
    pass
