
"""
Created on Sun Jun 26 13:27:26 2022

@author: onurserce
"""

import pandas as pd
import os


def ReadPgMatrix(Path_PgMatrix, sep='\t', index_col=0):
    
    PgMatrix = pd.read_csv(Path_PgMatrix, sep="\t", index_col=0)
    
    return PgMatrix


def CreateTemplateForSamples(PgMatrix, OutputDirectory):
    # Column name and category re/mapping
    TempDf = pd.DataFrame(index=PgMatrix.columns, data=PgMatrix.columns.values,
                          columns=['MeltWithExcel'])
    TempDf.index.name = 'OriginalName'

    if not os.path.exists(os.path.join(OutputDirectory, 'mapping.csv')):
        TempDf.to_csv(os.path.join(OutputDirectory, 'mapping.csv'))
        print(os.path.join(OutputDirectory, 'mapping.csv'), 'created!')
    else:
        raise Exception(
            os.path.join(OutputDirectory, 'mapping.csv') + ' already exists!')


def TidyPgMatrixFromMappingFile(PgMatrix, MappingFilePath, OutputDirectory):
    
    Mapping = pd.read_csv(MappingFilePath)

    # Create MultiIndex
    Categories = [c for c in Mapping.columns if c != 'OriginalName']
    Arrays = [Mapping.loc[:, a] for a in Categories]
    MultiIndex = pd.MultiIndex.from_arrays(arrays=Arrays, names=Categories)
    PgMatrix.columns = MultiIndex
    PgMatrix.index.name = 'Pg'

    PgMatrix.to_hdf(os.path.join(OutputDirectory, 'TidyPg.h5'), key='PgMatrix')
    PgMatrix.to_csv(os.path.join(OutputDirectory, 'TidyPg.csv'))


if __name__ == "__main__":
    import sys

    print("Initiating with args: ", sys.argv)
    
    Path_PgMatrix = sys.argv[1]
    
    Folder = os.path.split(Path_PgMatrix)[0]
    PgMatrix = ReadPgMatrix(Path_PgMatrix)
    
    
    try:
        CreateTemplateForSamples(PgMatrix=PgMatrix, OutputDirectory=Folder)
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
        
