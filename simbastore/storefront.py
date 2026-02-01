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
import copy
from pathlib import Path
import json
from jsonschema import validate
from simbastore.store import Store


class StoreFront:
    @classmethod
    def ResolvePath(
        cls, pathToResolve, RelativeTo, forceExistence: bool = True
    ) -> Path:
        if Path(pathToResolve).is_absolute():
            return Path(pathToResolve)

        if not isinstance(RelativeTo, list):
            RelativeTo = [RelativeTo]

        for r in RelativeTo:
            if not r:
                continue

            relativeTo = Path(r)

            if relativeTo.is_file():
                relativeTo = relativeTo.absolute().parent

            if relativeTo.joinpath(pathToResolve).exists() or not forceExistence:
                return relativeTo.joinpath(pathToResolve)

        return Path(pathToResolve)

    def __init__(self, parent=None):
        self.parent = parent
        self.configuration = None
        self.name = None
        self.root = None
        self.stores = {}
        self.currentTick = None
        self.tickFormat = "{}"

    def load(self, configuration):
        self.configuration = Path(configuration).absolute()

        try:
            jsonFile = open(self.configuration, "r")

        except:
            sys.exit("ERROR: File '" + configuration + "' does not exist.")

        dictionary = json.load(jsonFile)

        jsonFile.close()

        self.name = dictionary["path"]

        if "stores" in dictionary:
            self.stores = self.createStores(dictionary["stores"])

        return

    def get(self, store) -> Store | None:
        if store in self.stores:
            return self.stores[store]

        return None

    def setTickFormat(self, tickFormat):
        self.tickFormat = tickFormat

    def formatTick(self, tick) -> str:
        return self.tickFormat.format(tick)

    def setCurrentTick(self, tick):
        self.currentTick = tick

    def getCurrentTick(self):
        return self.currentTick

    def root(self):
        return self.root

    def createStores(self, ss, directions=[]):
        from simbastore.file import File
        from simbastore.csv import CSV

        stores = {}

        for s in ss:
            store = None

            if s["type"] == "file":
                store = File(self, s, directions)

            if s["type"] == "csv":
                store = CSV(self, s, directions)

            if store == None:
                continue

            if store.getName() in stores:
                sys.exit(
                    "ERROR: Store names must be unique in '"
                    + str(self.configuration)
                    + "'."
                )

            stores[store.getName()] = store

        return stores

    def resolvePath(self, path) -> Path:
        return StoreFront.ResolvePath(path, [self.configuration, self.root, Path.cwd()])

    def makeDirection(self, directions, tick=None):
        if self.parent:
            Direction = self.parent.makeDirections([self.name], tick)
        else:
            if tick == None:
                Direction = self.root.joinpath(self.currentTick)  # type: ignore
            elif isinstance(tick, int):
                Direction = self.root.joinpath(self.formatTick(tick))  # type: ignore
            else:
                Direction = self.root.joinpath(tick)  # type: ignore

        for d in directions:
            Direction = Direction.joinpath(d)

        return Direction

    def execute(self, configuration):
        success = False

        try:
            jsonFile = open(configuration, "r")

        except:
            sys.exit("ERROR: File '" + configuration + "' does not exist.")

        dictionary = json.load(jsonFile)

        jsonFile.close()

        storeFronts = {}

        if "commonData" in dictionary and "storeFronts" in dictionary["commonData"]:
            storeFronts = dictionary["commonData"]["storeFronts"]
            dictionary["commonData"]["storeFronts"] = {}
            storeFronts[self.name] = copy.deepcopy(dictionary)

        if not self.root:
            if "outputDirectory" in dictionary:
                self.root = StoreFront.ResolvePath(dictionary["outputDirectory"], configuration, False).absolute().joinpath(self.name)  # type: ignore
            else:
                self.root = Path(self.name).resolve()  # type: ignore

            if not self.root.exists():
                self.root.mkdir(parents=True)

        if dictionary["mode"] == "start":
            success = self.start(dictionary["currentTick"], dictionary["currentTime"])

        if dictionary["mode"] == "step":
            success = self.step(
                dictionary["lastRunTick"],
                dictionary["lastRunTime"],
                dictionary["currentTick"],
                dictionary["currentTime"],
                dictionary["targetTick"],
                dictionary["targetTime"],
            )

        if dictionary["mode"] == "end":
            success = self.end(
                dictionary["lastRunTick"],
                dictionary["lastRunTime"],
                dictionary["currentTick"],
                dictionary["currentTime"],
            )

        if "commonData" in dictionary and "storeFronts" in dictionary["commonData"]:
            dictionary["commonData"]["storeFronts"] = storeFronts

        dictionary["status"] = "success" if success else "failed"

        current_directory = os.getcwd()
        print(f"Current working directory: {current_directory}")

        jsonFile = self.resolvePath(dictionary["statusFile"]).open(mode="w")

        json.dump(dictionary, jsonFile, indent=2)
        jsonFile.close()

        return success

    def start(self, currentTick, currentTime):
        success = True

        try:
            self.currentTick = self.formatTick(currentTick)
            direction = self.makeDirection([])

            if not direction.exists():
                os.mkdir(direction)

            symlink = self.makeDirection([], "start")

            if symlink.exists():
                os.remove(symlink)

            os.symlink(self.currentTick, symlink)

            for store in self.stores.values():
                success &= store.start(currentTick, currentTime)

        except:
            success = False

        return success

    def step(
        self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime
    ):
        success = True

        try:
            self.currentTick = self.formatTick(targetTick)
            direction = self.makeDirection([])

            if not direction.exists():
                os.mkdir(direction)

            for store in self.stores.values():
                success &= store.step(
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
            self.currentTick = self.formatTick(endTick)
            direction = self.makeDirection([])

            if not direction.exists():
                os.mkdir(direction)

            symlink = self.makeDirection([], "end")

            if symlink.exists():
                os.remove(symlink)

            os.symlink(self.currentTick, symlink)

            for store in self.stores.values():
                store.end(lastRunTick, lastRunTime, endTick, endTime)

        except:
            success = False

        return success
