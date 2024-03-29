#!/usr/bin/env python3

import argparse
from simbastore.storefront import StoreFront
from simbastore.file import File
from simbastore.csv import CSV
import pandas

parser = argparse.ArgumentParser(description="SIMBA Store Front data framework.")
parser.add_argument("configuration", nargs=1, help='The configuration of the SIMBA Store Front.')

arguments = parser.parse_args()
StoreFront.load(arguments.configuration[0])
StoreFront.setCurrentTick(0)

file_store = StoreFront.get('file_store')
name = file_store.getName()
file = file_store.open()

csv_store = StoreFront.get('csv_store')
name = csv_store.getName()
csv = csv_store.open()

print(csv)

csv.loc[123.4560, 126.4456] = [2.22, 7.88]
print(csv.columns)
print(csv.index)

csv2 = pandas.DataFrame([[6.66, 7.88]], columns = csv.columns, index = pandas.MultiIndex.from_arrays([[222.4560], [126.4456]], names = csv.index.names))
csv = pandas.concat([csv, csv2]) 

print(csv)
csv_store.close(save = True, data = csv)

exit
