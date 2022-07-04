#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:44:43 2022

@author: onurserce
"""

from IO import ReadPgMatrix
from tqdm import tqdm


PgMatrix = ReadPgMatrix("/Users/onurserce/Desktop/THP1 proteome/TidyPgMatrix.hdf")


def ImputeFromReplicates(PgMatrix, ThresholdRatio=0.65):
    """Imputation from replicates."""
    PgMatrix = PgMatrix.sort_index(axis=1)
    NaBeforeImputation = PgMatrix.isna()
    # Raise exception if the DataFrame doesn't have 'Replicates' column.
    if 'Replicate' not in PgMatrix.columns.names:
        raise Exception("'Replicate' column not found, aborting imputation!!!")

    ReplicateLevel = PgMatrix.columns.names.index('Replicate')
    Unique = PgMatrix.columns.droplevel(ReplicateLevel).unique()

    for U in tqdm(Unique,
                  desc="Imputing missing data using 'Replicate' averages"):
        Slice = PgMatrix.loc[:, U]  # Get the current group of replicates
        NReplicates = len(PgMatrix.loc[:, U].columns)  # Count of replicates
        OverThreshold = (
            Slice.notna().sum(axis=1) / NReplicates
            ) >= ThresholdRatio  # Check if the row is above the threshold
        ToBeImputedMask = Slice.notna()[OverThreshold]  # Create a mask

        ImputedSlice = Slice.where(
            ToBeImputedMask,
            Slice.mean(axis=1),
            axis=0).to_numpy()  # Imputation with the mean
        PgMatrix.loc[:, U] = ImputedSlice  # Back into the DataFrame
        # Conversion to NDArray is necessary!

        NaAfterImputation = PgMatrix.isna()
        Imputed = NaAfterImputation != NaBeforeImputation
        NotImputed = NaAfterImputation & NaBeforeImputation

    return PgMatrix, Imputed, NotImputed


def ImputeWithDownshift():
    pass
