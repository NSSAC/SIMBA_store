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
import shutil
import numpy as np
import pandas as pd

from simbastore.store import Store


class CSV(Store):
    def _init(self, configuration, directions):
        self.header = "infer"
        self.names = pd.api.extensions.no_default
        self.dtype = None
        self.index_col = None
        self.dataFrames = {}

        if "schema" in configuration:
            schema = configuration["schema"]

            if "fields" in schema:
                self.header = 0
                self.dtype = {}
                self.names = []

                pandas_type_map = {
                    "string": str,
                    "number": np.float64,
                    "integer": np.int64,
                    "bool": np.bool,
                    "geojson": str,
                }

                for f in schema["fields"]:
                    self.names.append(f["name"])
                    self.dtype[f["name"]] = pandas_type_map[f["type"]]

            if "primaryKey" in schema:
                self.index_col = []

                if isinstance(schema["primaryKey"], list):
                    for k in schema["primaryKey"]:
                        self.index_col.append(k)
                else:
                    self.index_col.append(schema["primaryKey"])

    def _start(self, currentTick, currentTime):
        success = True

        try:
            shutil.copy(
                self.parent.resolvePath(self.initialPath),
                self.parent.makeDirection(self.directions).joinpath(self.path),
            )

        except Exception as e:
            print(
                "ERROR: Could not copy file '"
                + str(self.parent.resolvePath(self.path))
                + "' to '"
                + str(self.parent.makeDirection(self.directions).joinpath(self.path))
                + "'.",
                file=sys.stderr,
            )
            success = False

        return success

    def _step(
        self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime
    ):
        success = True

        if self.readOnly:
            symlink = self.parent.makeDirection(self.directions).joinpath(self.path)

            if symlink.exists():
                os.remove(symlink)

            try:
                os.symlink(
                    self.parent.makeDirection(self.directions, "start").joinpath(
                        self.path
                    ),
                    symlink,
                )

            except Exception as e:
                print(
                    "ERROR: Could not create symlink '"
                    + str(
                        self.parent.makeDirection(self.directions, "start").joinpath(
                            self.path
                        )
                    )
                    + "' to '"
                    + str(symlink)
                    + "'.",
                    file=sys.stderr,
                )
                success = False

        else:
            try:
                shutil.copy(
                    self.parent.makeDirection(self.directions, lastRunTick).joinpath(
                        self.path
                    ),
                    self.parent.makeDirection(self.directions).joinpath(self.path),
                )

            except Exception as e:
                print(
                    "ERROR: Could not copy file '"
                    + str(
                        self.parent.makeDirection(
                            self.directions, lastRunTick
                        ).joinpath(self.path)
                    )
                    + "' to '"
                    + str(
                        self.parent.makeDirection(self.directions).joinpath(self.path)
                    )
                    + "'.",
                    file=sys.stderr,
                )
                success = False

        return success

    def _end(self, lastRunTick, lastRunTime, endTick, endTime):
        success = True

        if self.readOnly:
            symlink = self.parent.makeDirection(self.directions).joinpath(self.path)

            if symlink.exists():
                os.remove(symlink)

            try:
                os.symlink(
                    self.parent.makeDirection(self.directions, "start").joinpath(
                        self.path
                    ),
                    symlink,
                )

            except Exception as e:
                print(
                    "ERROR: Could not create symlink '"
                    + str(
                        self.parent.makeDirection(self.directions, "start").joinpath(
                            self.path
                        )
                    )
                    + "' to '"
                    + str(symlink)
                    + "'.",
                    file=sys.stderr,
                )
                success = False
        else:
            try:
                shutil.copy(
                    self.parent.makeDirection(self.directions, lastRunTick).joinpath(
                        self.path
                    ),
                    self.parent.makeDirection(self.directions).joinpath(self.path),
                )

            except Exception as e:
                print(
                    "ERROR: Could not copy file '"
                    + str(
                        self.parent.makeDirection(
                            self.directions, lastRunTick
                        ).joinpath(self.path)
                    )
                    + "' to '"
                    + str(
                        self.parent.makeDirection(self.directions).joinpath(self.path)
                    )
                    + "'.",
                    file=sys.stderr,
                )
                success = False

        return success

    def _open(self, tick):
        if not self.parent.formatTick(tick) in self.dataFrames:
            self.dataFrames[self.parent.formatTick(tick)] = pd.read_csv(
                self.parent.makeDirection(self.directions, tick).joinpath(self.path),
                header=self.header,
                names=self.names,
                index_col=self.index_col,
                dtype=self.dtype,
            )  # pyright: ignore[reportArgumentType]

        return self.dataFrames[self.parent.formatTick(tick)]

    def _close(self, tick, save, data):
        if self.parent.formatTick(tick) in self.dataFrames:
            if save and tick == self.parent.getCurrentTick() and not self.readOnly:
                if isinstance(data, pd.DataFrame):
                    data.to_csv(
                        self.parent.makeDirection(self.directions, tick).joinpath(
                            self.path
                        )
                    )
                else:
                    self.dataFrames[self.parent.formatTick(tick)].to_csv(
                        self.parent.makeDirection(self.directions, tick).joinpath(
                            self.path
                        )
                    )

            del self.dataFrames[self.parent.formatTick(tick)]
