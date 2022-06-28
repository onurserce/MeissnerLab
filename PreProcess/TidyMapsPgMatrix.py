
"""
Created on Sun Jun 26 13:27:26 2022

@author: onurserce
"""

import numpy as np
import pandas as pd
import os


def ReadPgMatrix(Path_PgMatrix, sep='\t', index_col=0):

    PgMatrix = pd.read_csv(Path_PgMatrix, sep="\t", index_col=0)

    return PgMatrix


def CreateTidyingTemplateFromPgMatrix(PgMatrix, OutputDirectory):
    # Column name and category re/mapping

    ColumnsSplitted = PgMatrix.columns.str.split("\\")
    NewNames = [e[-1] for e in ColumnsSplitted[4:]]
    Array = np.empty(shape=(len(NewNames)))
    Array[:] = np.nan

    TempDf = pd.DataFrame(index=PgMatrix.columns[4:],
                          columns=['ExperimentID', 'TextToColumnsWithExcel'])
    TempDf.index.name = 'OriginalName'
    TempDf['ExperimentID'] = Array
    TempDf['TextToColumnsWithExcel'] = NewNames

    if not os.path.exists(os.path.join(OutputDirectory, 'mapping.csv')):
        TempDf.to_csv(os.path.join(OutputDirectory, 'mapping.csv'))
        print(os.path.join(OutputDirectory, 'mapping.csv'), 'created!')
    else:
        raise Exception(
            os.path.join(OutputDirectory, 'mapping.csv') + ' already exists!')


def TidyPgMatrixFromMappingFile(PgMatrix, MappingFilePath, OutputDirectory):

    Mapping = pd.read_csv(MappingFilePath)

    # Create MultiIndex
    Categories = [c for c in Mapping.columns if
                  c != 'OriginalName' and c != 'ExperimentID']
    Arrays = [Mapping.loc[:, a] for a in Categories]
    MultiIndex = pd.MultiIndex.from_arrays(arrays=Arrays, names=Categories)
    PgMatrix = PgMatrix.drop(
        columns=[
            'Protein.Ids',
            'Protein.Names',
            'Genes',
            'First.Protein.Description'])
    PgMatrix.columns = MultiIndex
    PgMatrix.index.name = 'Pg'

    PgMatrix.to_hdf(os.path.join(OutputDirectory, 'TidyPgMatrix.hdf'),
                    key='TidyPgMatrix')
    PgMatrix.to_csv(os.path.join(OutputDirectory, 'TidyPgMatrix.csv'))


if __name__ == "__main__":
    import sys
    print("Initiating with args: ", sys.argv)

    Path_PgMatrix = sys.argv[1]
    Folder = os.path.split(Path_PgMatrix)[0]
    PgMatrix = ReadPgMatrix(Path_PgMatrix)

    try:
        CreateTidyingTemplateFromPgMatrix(
            PgMatrix=PgMatrix, OutputDirectory=Folder)
        print('Please edit the mapping.csv file and re-run the script!')
        exit(0)
    except Exception:
        print(
            os.path.join(Folder, 'mapping.csv'), 'found!',
            'Tidying the PgMatrix..')
        input_ = 'continue'

    if input_ == 'continue':
        MappingFilePath = os.path.join(Folder, 'mapping.csv')
        TidyPgMatrixFromMappingFile(PgMatrix=PgMatrix,
                                    MappingFilePath=MappingFilePath,
                                    OutputDirectory=Folder)
        print('Completed. Exiting script!')
        exit(0)
    else:
        print('Exiting script from the else statement! Please debug!')
        exit(0)
