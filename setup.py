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

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='simbaStore',
    version='1.0.0',
    description='SIMBA is a framework for performing multi-scale simulations in an HPC environment.',
    url="https://simba-store.readthedocs.io/en/latest/index.html",
    author='Stefan Hoops',
    author_email='shoops@virginia.edu',
    license='Apache 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=["bin/store.py"],
    install_requires=[
        'pandas',
        'jsonschema'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False)
