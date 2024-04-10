#!/usr/bin/env python3

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

import argparse
import json
import sys
from jsonschema import validate
from simbastore.storefront import StoreFront
from pathlib import Path

def loadJsonFile(fileName, schema = None):

    try:
        jsonFile = open(fileName,"r")
    
    except:
        sys.exit("ERROR: File '" + fileName + "' does not exist.")
    
    dictionary = json.load(jsonFile)
    
    if schema != None:
        validate(dictionary, schema)
        
    jsonFile.close()

    return dictionary

def main(config):
    dictionary = loadJsonFile(config)

    if not 'moduleData' in dictionary:
        sys.exit("ERROR: Missing attribute 'moduleData' in '" + config + "'.")
      
    if not 'configuration' in dictionary['moduleData']:
        sys.exit("ERROR: Missing attribute 'moduleData/configuration' in '" + config + "'.")
    
    if not 'tickFormat' in dictionary:
        sys.exit("ERROR: Missing attribute 'tickFormat' in '" + config + "'.")
        
    try:
        StoreFront.load(dictionary['moduleData']['configuration'])
      
    except:
        sys.exit("ERROR: Invalid store configuration in '" + dictionary['moduleData']['configuration'] + "'.")
    
    StoreFront.setTickFormat(dictionary['tickFormat'])
    
    success = False
    
    if (dictionary['mode'] == 'start'):
        success = StoreFront.start(dictionary['currentTick'], dictionary['currentTime'])

    if (dictionary['mode'] == 'step'):
        success = StoreFront.step(dictionary['lastRunTick'], dictionary['lastRunTime'], dictionary['currentTick'], dictionary['currentTime'], dictionary['targetTick'], dictionary['targetTime'])

    if (dictionary['mode'] == 'end'):
        success = StoreFront.end(dictionary['lastRunTick'], dictionary['lastRunTime'], dictionary['currentTick'], dictionary['currentTime'])

    if success:
        open(Path(dictionary['statusFile']), mode = 'w').write('{"status": "success"}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="SIMBA Store Module.")
    parser.add_argument("configuration", nargs=1, help='The configuration of the SIMBA Store Module.')

    arguments = parser.parse_args()
    main(arguments.configuration[0])

        
