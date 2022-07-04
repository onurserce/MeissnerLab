#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:35:51 2021

@author: onurserce
"""

path_to_cell_counter_data = "Cell counts/hbiks.ko.01_20211213_164035.csvasdf"
path_to_cell_counter_datafolder = "Desktop/Cell counts"

import pandas as pd
import os

class Rectangle:
   def __init__(self, length, breadth, unit_cost=0):
       self.length = length
       self.breadth = breadth
       self.unit_cost = unit_cost
   def get_area(self):
       return self.length * self.breadth

def DataType(object):
    pass

def Cell(object):
    pass

def Protein(object):
    pass

def CellCountData(object):
    ".csv imported from Beckmen Coulter automated cell counter."
    # ToDo: should also work for Summary.csv
    pass

def CellCountDataManager(path_to_cell_counter_datafolder):
    "Reads all cell count data, processes, and saves the final state"
    # ToDo: logging. will be also needed for the entire program.
    listdir = os.listdir(path_to_cell_counter_datafolder)
    print(listdir)
    return(listdir)

    
def ReadIndividualCountData(path_to_csv):
    pass

CellCountDataManager(path_to_cell_counter_datafolder)


