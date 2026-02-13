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
import json

from simbastore.store import Store


class Front(Store):
    def _init(self, configuration, directions):
        from simbastore.storefront import StoreFront

        if "configuration" not in configuration:
            print(
                f"ERROR: Attribute 'configuration' is missing for store front '{self.name}'.",
                file=sys.stderr,
            )

        self.configuration = self.parent.resolvePath(configuration["configuration"])

        try:
            jsonFile = open(self.configuration, "r")

        except Exception as e:
            sys.exit("ERROR: File '" + configuration + "' does not exist.")

        dictionary = json.load(jsonFile)
        jsonFile.close()

        self.path = dictionary["path"]
        self.storeFront = StoreFront(self.parent)
        self.storeFront.load(self.configuration)

    def _start(self, currentTick, currentTime):
        return True

    def _step(
        self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime
    ):
        return True

    def _end(self, lastRunTick, lastRunTime, endTick, endTime):
        return True

    def _open(self, tick):
        return None

    def _close(self, tick, save, data):
        pass
