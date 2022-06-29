
"""
Created on Sun Jun 26 13:27:26 2022

@author: onurserce
"""

import os
import pandas as pd
from IO import ReadPgMatrix
from Utility import CreateTidyingTemplateFromPgMatrix

# ToDo: Add replicate support & imputation


def TidyPgMatrixFromMappingFile(PgMatrix, MappingFilePath, OutputDirectory):
    """Tidy and save protein groups matrix using a mapping.csv file."""
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
