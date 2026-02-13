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
from abc import ABC, abstractmethod


class Store(ABC):
    @classmethod
    def create(cls, parent, configuration, directions=[]):
        store = None

        if configuration["type"] == "storeFront":
            from simbastore.storefrontstore import Front

            store = Front(parent, configuration, directions)

        if configuration["type"] == "directory":
            from simbastore.directorystore import Directory

            store = Directory(parent, configuration, directions)

        if configuration["type"] == "file":
            from simbastore.filestore import File

            store = File(parent, configuration, directions)

        if configuration["type"] == "csv":
            from simbastore.csvstore import CSV

            store = CSV(parent, configuration, directions)

        return store

    def __init__(self, parent, configuration, directions=[]):
        from simbastore.storefront import StoreFront

        self.parent = parent
        self.name = configuration["name"]
        self.directions = directions[:]
        self.directions.append(configuration["name"])
        self.path = configuration["path"] if "path" in configuration else None
        self.initialPath = (
            parent.resolvePath(configuration["initialPath"])
            if "initialPath" in configuration
            else None
        )
        self.readOnly = (
            configuration["readOnly"] if "readOnly" in configuration else False
        )
        self.table = configuration["table"] if "table" in configuration else None
        self.storeFront = None

        if "stores" in configuration:
            self.storeFront = StoreFront()
            self.storeFront.load(configuration)

        self._init(configuration, directions)

    def getName(self):
        return self.name

    def getStoreFront(self):
        return self.storeFront

    def start(self, currentTick, currentTime):
        success = True

        try:
            from simbastore.storefront import StoreFront

            direction = self.parent.makeDirection(self.directions)

            if not direction.exists():
                os.mkdir(direction)

            success &= self._start(currentTick, currentTime)

            if self.storeFront:
                success &= self.storeFront.start(currentTick, currentTime)

        except:
            success = False

        return success

    def step(
        self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime
    ):
        success = True

        try:
            from simbastore.storefront import StoreFront

            direction = self.parent.makeDirection(self.directions)

            if not direction.exists():
                os.mkdir(direction)

            success &= self._step(
                lastRunTick,
                lastRunTime,
                currentTick,
                currentTime,
                targetTick,
                targetTime,
            )

            if self.storeFront:
                success &= self.storeFront.step(
                    lastRunTick,
                    lastRunTime,
                    currentTick,
                    currentTime,
                    targetTick,
                    targetTime,
                )

        except:
            success = False

        return success

    def end(self, lastRunTick, lastRunTime, endTick, endTime):
        success = True

        try:
            from simbastore.storefront import StoreFront

            direction = self.parent.makeDirection(self.directions)

            if not direction.exists():
                os.mkdir(direction)

            success &= self._end(lastRunTick, lastRunTime, endTick, endTime)

            if self.storeFront:
                success &= self.storeFront.end(
                    lastRunTick, lastRunTime, endTick, endTime
                )

        except:
            success = False

        return success

    def open(self, tick=None):
        if tick == None:
            from simbastore.storefront import StoreFront

            tick = self.parent.getCurrentTick()

        return self._open(tick)

    def close(self, tick=None, save=False, data=None):
        if tick == None:
            from simbastore.storefront import StoreFront

            tick = self.parent.getCurrentTick()

        return self._close(tick, save, data)

    @abstractmethod
    def _init(self, configuration, directions):
        pass

    @abstractmethod
    def _start(self, currentTick, currentTime) -> bool:
        return False

    @abstractmethod
    def _step(
        self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime
    ) -> bool:
        return False

    @abstractmethod
    def _end(self, lastRunTick, lastRunTime, endTick, endTime) -> bool:
        return False

    @abstractmethod
    def _open(self, tick):
        pass

    @abstractmethod
    def _close(self, tick, save, data):
        pass
