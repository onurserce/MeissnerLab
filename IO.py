#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 08:31:04 2022

@author: onurserce

Input/Output functions
"""

import pandas as pd


def ReadPgMatrix(Path_PgMatrix, sep='\t', index_col=0):
    """Read original DIANN or tidy protein groups or matrix."""
    if Path_PgMatrix.endswith('.tsv'):
        PgMatrix = pd.read_csv(Path_PgMatrix, sep="\t", index_col=0)
    elif Path_PgMatrix.endswith('.hdf'):
        PgMatrix = pd.read_hdf(Path_PgMatrix)
    else:
        raise Exception('File format not known from the suffix.')

    return PgMatrix
