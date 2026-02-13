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
import sys
import shutil

from simbastore.store import Store


class Directory(Store):
    def _init(self, configuration, directions):
        self.files = {}

    def _start(self, currentTick, currentTime):
        success = True

        try:
            shutil.copytree(
                self.parent.resolvePath(self.initialPath),
                self.parent.makeDirection(self.directions).joinpath(self.path),
            )

        except Exception as e:
            print(
                f"ERROR: Could not copy directory '{str(self.parent.resolvePath(self.initialPath))}' to '{str(self.parent.makeDirection(self.directions).joinpath(self.path))}'.",
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
                    f"ERROR: Could not create symlink '{str(
                        self.parent.makeDirection(self.directions, "start").joinpath(
                            self.path
                        )
                    )}' to '{str(symlink)}'.",
                    file=sys.stderr,
                )
                success = False

        else:
            try:
                shutil.copytree(
                    self.parent.makeDirection(self.directions, lastRunTick).joinpath(
                        self.path
                    ),
                    self.parent.makeDirection(self.directions).joinpath(self.path),
                )

            except Exception as e:
                print(
                    f"ERROR: Could not copy directory '{str(
                        self.parent.makeDirection(
                            self.directions, lastRunTick
                        ).joinpath(self.path)
                    )}' to '{str(
                        self.parent.makeDirection(self.directions).joinpath(self.path)
                    )}'.",
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
                    f"ERROR: Could not create symlink '{str(
                        self.parent.makeDirection(self.directions, "start").joinpath(
                            self.path
                        )
                    )}' to '{str(symlink)}'.",
                    file=sys.stderr,
                )
                success = False

        else:
            try:
                shutil.copytree(
                    self.parent.makeDirection(self.directions, lastRunTick).joinpath(
                        self.path
                    ),
                    self.parent.makeDirection(self.directions).joinpath(self.path),
                )

            except Exception as e:
                print(
                    f"ERROR: Could not copy directory '{str(
                        self.parent.makeDirection(
                            self.directions, lastRunTick
                        ).joinpath(self.path)
                    )}' to '{str(
                        self.parent.makeDirection(self.directions).joinpath(self.path)
                    )}'.",
                    file=sys.stderr,
                )
                success = False

        return success

    def _open(self, tick):
        return None

    def _close(self, tick, save, data):
        pass
