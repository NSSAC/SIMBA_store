#!/usr/bin/env python3

import sys
import os
import copy
import argparse
from pathlib import Path
import json
from jsonschema import validate
from simbastore.storefront import StoreFront


class SimbaStores:
    def __init__(self, configuration=None) -> None:
        self.configuration = None
        self.storeFronts = {}

        if configuration:
            self.load(configuration)

    def load(self, configuration):
        self.configuration = Path(configuration).absolute()

        try:
            jsonFile = open(self.configuration, "r")

        except:
            sys.exit("ERROR: File '" + configuration + "' does not exist.")

        dictionary = json.load(jsonFile)
        jsonFile.close()

        if not "commonData" in dictionary:
            sys.exit(
                "ERROR: Missing attribute 'commonData' in '" + configuration + "'."
            )

        if not "storeFronts" in dictionary["commonData"]:
            sys.exit(
                "ERROR: Missing attribute 'commonData/storeFronts' in '"
                + configuration
                + "'."
            )

        for name, config in dictionary["commonData"]["storeFronts"].items():
            if name in self.storeFronts:
                sys.exit("ERROR: Duplicate store front name: '" + name + "'.")

            if not "moduleData" in config:
                sys.exit(
                    "ERROR: Missing attribute 'moduleData' for store front '"
                    + name
                    + "'."
                )

            if not "configuration" in config["moduleData"]:
                sys.exit(
                    "ERROR: Missing attribute 'moduleData/configuration' for store front '"
                    + name
                    + "'."
                )

            storeFront = StoreFront()
            storeFront.load(
                StoreFront.ResolvePath(
                    config["moduleData"]["configuration"], self.configuration
                )
            )

            self.storeFronts[name] = storeFront

    def findStore(self, store, storeFronts):
        if not isinstance(storeFronts, list):
            storeFronts = [storeFronts]

        parentStoreFront = None
        availableStoreFronts = self.storeFronts

        for storeFront in storeFronts:
            if parentStoreFront:
                tmpStore = parentStoreFront.get(storeFront)

                if (not tmpStore) or (not tmpStore.getStoreFront()):
                    sys.exit(
                        "Error: Store front '"
                        + storeFront
                        + "'not found in '"
                        + parentStoreFront.getName()
                    )

                parentStoreFront = tmpStore.getStoreFront()
                continue

            if storeFront in availableStoreFronts:
                parentStoreFront = availableStoreFronts[storeFront]

        if parentStoreFront:
            return parentStoreFront.get(store)

        return None


def main():
    parser = argparse.ArgumentParser(description="SIMBA Store Front data framework.")
    parser.add_argument(
        "configuration", nargs=1, help="The configuration of the SIMBA Store Front."
    )

    arguments = parser.parse_args()

    simbaStores = SimbaStores(arguments.configuration[0])

    store = simbaStores.findStore("farmer_data", "Store_Front_Static")


if __name__ == "__main__":
    main()
