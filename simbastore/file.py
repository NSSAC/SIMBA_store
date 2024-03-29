import os
import shutil
from pathlib import Path
from simbastore.storefront import StoreFront
from simbastore.store import Store

class File(Store):
  def _init(self, configuration, directions):
    self.files = {}

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
    if not str(tick) in self.files:
      if self.readOnly or tick != StoreFront.getCurrentTick():
        self.files[str(tick)] =  StoreFront.makeDirection(self.directions, tick).joinpath(self.path).open('r')
      else:
        self.files[str(tick)] =  StoreFront.makeDirection(self.directions, tick).joinpath(self.path).open('+')

    return self.files[str(tick)]

  def _close(self, tick, save, data):
    if str(tick) in self.files:
      self.files[str(tick)].close
      del self.files[str(tick)]
