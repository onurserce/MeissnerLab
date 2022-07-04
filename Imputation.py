#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:44:43 2022

@author: onurserce
"""

from IO import ReadPgMatrix
from tqdm import tqdm


PgMatrix = ReadPgMatrix("/Users/onurserce/Desktop/THP1 proteome/TidyPgMatrix.hdf")


def ImputeFromReplicates(PgMatrix):
    """Imputation from replicates."""
    df = PgMatrix.sort_index(axis=1)
    # Raise exception if the DataFrame doesn't have 'Replicates' column.
    if 'Replicate' not in df.columns.names:
        raise Exception("'Replicate' column not found, aborting imputation!!!")

    ReplicateLevel = df.columns.names.index('Replicate')
    Unique = df.columns.droplevel(ReplicateLevel).unique()

    for U in tqdm(Unique,
                  desc="Imputing missing data using 'Replicate' averages"):
        ImputedSlice = df.loc[:, U].where(
            df.loc[:, U].notna(),
            df.loc[:, U].mean(axis=1),
            axis=0)
        # Conversion to NDArray is necessary!
        df.loc[:, U] = ImputedSlice.to_numpy()
# TODO: Keep track of the imputed values!
    return df


def ImputeWithDownshift():
    pass
