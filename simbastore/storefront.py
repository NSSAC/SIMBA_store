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

    if 'stores' in dictionary:
      cls.__stores = cls.createStores(dictionary['stores'])

    return

  @classmethod
  def get(cls, store):
    if store in cls.__stores:
      return cls.__stores[store]

    return None

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

    return path

  @classmethod
  def makeDirection(cls, directions, tick = None):
    if tick == None:
      Direction = cls.__root.joinpath(cls.__currentTick)
    else:
      Direction = cls.__root.joinpath(str(tick))

    for d in directions:
      Direction = Direction.joinpath(d)

    return Direction

  @classmethod
  def start(cls, currentTick, currentTime):
    cls.__currentTick = str(currentTick)
    direction = cls.makeDirection([])

    if not direction.exists():
      os.mkdir(direction)

    symlink = cls.makeDirection([], 'start')

    if symlink.exists():
      os.remove(symlink)

    os.symlink(direction, symlink)

    for store in cls.__stores.values():
      store.start(currentTick, currentTime)

  @classmethod
  def step(cls, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
    cls.__currentTick = str(targetTick)
    direction = cls.makeDirection([])

    if not direction.exists():
      os.mkdir(direction)

    for store in cls.__stores.values():
      store.step(lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime)

  @classmethod
  def end(cls, lastRunTick, lastRunTime, endTick, endTime):
    cls.__currentTick = str(endTick)
    direction = cls.makeDirection([])

    if not direction.exists():
      os.mkdir(direction)

    symlink = cls.makeDirection([], 'end')

    if symlink.exists():
      os.remove(symlink)

    os.symlink(direction, symlink)
    for store in cls.__stores.values():
      store.end(lastRunTick, lastRunTime, endTick, endTime)

