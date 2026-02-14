"""
input.py

Module for input and input validation of the tabular dataset.
"""

import pandas as pd
import json

class Dataset:

    def __init__(self):
        """
        Initialize Dataset object.
        """
        self.dataset = None
    
    def load(self, input_dataset):
        """
        Load Dataset

        Parameters:
        - input_dataset: str file path or pandas.DataFrame
        """
        
        if isinstance(input_dataset, str):
            
            input_dataset = input_dataset.lower()

            if input_dataset.endswith(".csv"):
                # read CSV file

                try: 
                    self.dataset = pd.read_csv(input_dataset)
                except Exception as e:
                    raise ValueError(f"CSV file cannot be read!\n{e}")

            elif input_dataset.endswith(".parquet"):
                # read Parquet file

                try:
                    self.dataset = pd.read_parquet(input_dataset)
                except Exception as e:
                    raise ValueError(f"Parquet file cannot be read!\n{e}")
            
            elif input_dataset.endswith(".json"):
                # read JSON file

                try:
                    self.dataset = pd.read_json(input_dataset)
                except Exception as e:
                    raise ValueError(f"JSON file cannot be read!\n{e}")

            
            elif input_dataset.endswith(".xlsx"):
                # read Excel file

                try:
                    file = pd.ExcelFile(input_dataset)
                    if len(file.sheet_names) != 1:
                        raise ValueError("Cannot read more than one Excel sheets!")
                    self.dataset = pd.read_excel(file, sheet_name = 0)
                except Exception as e:
                    raise ValueError(f"Excel file not read!\n{e}")

            else:
                # invalid file input

                raise ValueError("Unsupported file format received as input!")
            
        elif isinstance(input_dataset, pd.DataFrame):
            # pandas DataFrame

            self.dataset = input_dataset.copy(deep = True)
        
        else:
            # invalid input

            raise TypeError("Invalid or unsupported input format received!")

        if self.dataset.empty:
            # empty dataset

            raise ValueError("Empty dataset loaded!")
        
        return self.dataset

    def __repr__(self):
        """
        Return string representation of object.
        """

        return f"Dataset(shape = {self.dataset.shape}, columns = {list(self.dataset.columns)})"

    def head(self, n = 5):
        """
        Return first n rows
        """

        return self.dataset.head(n)
    
    def tail(self, n = 5):
        """
        Return last n rows
        """

        return self.dataset.tail(n)
    
    @property
    def num_of_rows(self):
        """
        Return number of rows
        """

        return self.dataset.shape[0]
    
    @property
    def num_of_columns(self):
        """
        Return number of columns
        """

        return self.dataset.shape[1]
    
    @property
    def shape(self):
        """
        Return shape of the dataset
        """

        return self.dataset.shape

    @property
    def columns(self):
        """
        Return all columns
        """

        return list(self.dataset.columns)