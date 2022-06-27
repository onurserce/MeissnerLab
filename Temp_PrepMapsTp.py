
"""
Created on Sun Jun 26 13:27:26 2022

@author: onurserce
"""

import numpy as np
import pandas as pd
import os

# Read from the config file
DataDirectory = '/Users/onurserce/Desktop/new'
Path_PgMatrix = "/Users/onurserce/Desktop/new/report.pg_matrix.tsv"

PgMatrix = pd.read_csv(Path_PgMatrix, sep="\t", index_col=0)

# Column name and category re/mapping
TempDf = pd.DataFrame(index=PgMatrix.columns, data=PgMatrix.columns.values,
                      columns=['MeltWithExcel'])
TempDf.index.name = 'OriginalName'

if not os.path.exists(os.path.join(DataDirectory, 'mapping.csv')):
    TempDf.to_csv(os.path.join(DataDirectory, 'mapping.csv'))
else:
    print(os.path.join(DataDirectory, 'mapping.csv') + ' already exists!')
    pass


Mapping = pd.read_csv(os.path.join(DataDirectory, 'mapping.csv'))

# Create MultiIndex
Categories = [c for c in Mapping.columns if c != 'OriginalName']
Arrays = [Mapping.loc[:, a] for a in Categories]
MultiIndex = pd.MultiIndex.from_arrays(arrays=Arrays, names=Categories)

PgMatrix.columns = MultiIndex
PgMatrix.index.name = 'Pg'

