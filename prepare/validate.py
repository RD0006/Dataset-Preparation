"""
validate.py

Module for validating the columns of the dataset and optionally fixing issues in-place. 

Column checks and in-place fixes provided for the following issues:
- negative values in a column
- null values in a column
- duplicate values in a column
- appropriate class names in a column
- range validation of values in a column
"""

import math
import numpy as np
import pandas as pd
from .input import Dataset

class Validator:

    def __init__(self, dataset, inplace = False):
        """
        Initialize Validator Object

        Parameters:
        - dataset: Dataset object
        - inplace: bool, optional
        """

        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        self.dataset = dataset
        self.inplace = inplace
        self.__initial_row_count = dataset.num_of_rows
        self.__log = {}
        self.__indices = set()

    def __get_column(self, column):
        """
        Get column
        """

        dataset = self.dataset.dataset

        # if column is a string value
        if isinstance(column, str):
            if column not in dataset.columns:
                raise ValueError(f"Column {column} does not exist!")
            return column
        
        # if column is an int value
        elif isinstance(column, int):
            if not (column >= 0 and column < len(dataset.columns)):
                raise ValueError(f"Column index {column} is out of range!")
            return dataset.columns[column]
        
        # otherwise, raise TypeError
        else:
            raise TypeError("Incorrect value type passed as column name or index")
    
    def negative_values(self, column):
        """
        Count and optionally delete rows with negative values

        Parameters:
        - column: str or int
        """  
       
        dataset = self.dataset.dataset
        col = self.__get_column(column)
        
        # checks
        if dataset[col].isnull().any():
            raise ValueError("Column contains null values!")
        if not pd.api.types.is_numeric_dtype(dataset[col]) or isinstance(dataset[col].dtype, complex) or np.issubdtype(dataset[col].dtype, np.complexfloating):
            raise TypeError("Column must contain int and/or float values!")

        # operation
        rows = dataset[dataset[col] < 0].index

        # update log
        self.__log[(column, "Negative Values")] = len(rows)

        # drop rows if required
        if self.inplace:
            dataset.drop(index = rows, inplace = True)
        else:
            self.__indices.update(rows)
        
        return self

    def null_values(self, column):
        """
        Count and optionally delete rows with null values

        Parameters:
        - column: str or int
        """

        dataset = self.dataset.dataset
        col = self.__get_column(column)
        
        # operation
        rows = dataset[dataset[col].isnull()].index

        # update log
        self.__log[(column, "Null Values")] = len(rows)

        # drop rows if required
        if self.inplace :
            dataset.drop(index = rows, inplace = True)
        else:
            self.__indices.update(rows)
        
        return self

    def duplicate_values(self, column):
        """
        Count and optionally delete rows with duplicate values

        Parameters:
        - column: str or int
        """

        dataset = self.dataset.dataset
        col = self.__get_column(column)
        
        # operation
        rows = dataset[dataset.duplicated(subset = [col])].index
        
        # update log
        self.__log[(column, "Duplicate Values")] = len(rows)

        # drop rows if required
        if self.inplace :
            dataset.drop(index = rows, inplace = True)
        else:
            self.__indices.update(rows)
        
        return self

    def validate_class_names(self, column, class_names):
        """
        Count and optionally delete rows with incorrect class names

        Parameters:
        - column: str or int
        - class_names: list of valid class names
        """
        
        # checks
        if not isinstance(class_names, list):
            raise TypeError("Class names should be in a list!")

        dataset = self.dataset.dataset
        col = self.__get_column(column)

        # operation
        rows = dataset[dataset[col].isin(class_names)  == False].index
        
        # update log
        self.__log[(column, "Wrong Class Names")] = len(rows)

        # drop rows if required
        if self.inplace :
            dataset.drop(index = rows, inplace = True)
        else:
            self.__indices.update(rows)

        return self

    def validate_range(self, column, start = -math.inf, end = math.inf):
        """
        Count and optionally delete rows with values not in correct range

        Parameters:
        - column: str or int
        - start: int 
        - end: int
        """
        
        dataset = self.dataset.dataset
        col = self.__get_column(column)

        # checks
        if not (isinstance(start, (int, float)) and isinstance(end, (int, float))):
            raise TypeError("Range should be numeric!")
        if dataset[col].isnull().any():
            raise ValueError("Column contains null values!")
        if not pd.api.types.is_numeric_dtype(dataset[col]) or isinstance(dataset[col].dtype, complex) or np.issubdtype(dataset[col].dtype, np.complexfloating):
            raise TypeError("Column must contain int and/or float values!")

        # operation
        rows = dataset[(dataset[col] < start) | (dataset[col] > end)].index

        # update log
        self.__log[(column, "Values not in Range")] = len(rows)

        # drop rows if required
        if self.inplace :
            dataset.drop(index = rows, inplace = True)
        else:
            self.__indices.update(rows)

        return self
    

    def get_log(self):
        """
        Get log containing the list of all issues
        """
        
        log = self.__log
        if self.inplace == True:
            log[("Complete Dataset", "Total Number of Invalid Rows Updated")] = len(self.__indices)
            log[("Complete Dataset", "Total Percentage of Invalid Rows Updated")] = len(self.__indices) / self.__initial_row_count * 100
        else:
            log[("Complete Dataset", "Total Number of Invalid Rows Found")] = len(self.__indices)
            log[("Complete Dataset", "Total Percentage of Invalid Rows Found")] = len(self.__indices) / self.__initial_row_count * 100
        return log
    
    def drop_invalid_rows(self):
        """
        Fix all issues by dropping all invalid rows
        """

        if self.inplace == True:
            return -1
        elif self.__indices:
            self.dataset.dataset.drop(index = list(self.__indices), inplace = True)
            cnt = len(self.__indices)
            self.__log = {}
            self.__indices = set()
            return cnt
        else:
            return 0