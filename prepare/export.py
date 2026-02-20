"""
export.py

Module for exporting the final dataset in the required format.

Utility functions provided to support the following formats: 
- CSV
- JSON
- DataFrame
- Parquet
- Excel File
"""

import os
import pandas as pd
from .input import Dataset

class Exporter:

    def __init__(self, dataset):
        """
        Initialize Exporter Object

        Parameters:
        - dataset
        """

        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        self.dataset = dataset
    
    def __check_file_overwrite(self, filename, overwrite):
        """
        Helper Function to check if file exists and if overwrite is allowed
        """
        
        if os.path.exists(filename) and not overwrite:
            raise FileExistsError(f"File {filename} already exists and overwrite is set to False!")

    def export_to_csv(self, filename = "Updated_Dataset.csv", overwrite = False):
        """
        Export Dataset to CSV

        Parameters:
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not filename.lower().endswith(".csv"):
            raise ValueError("File Extension must be .csv!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to csv
        try:
            self.dataset.dataset.to_csv(filename, sep = ",", index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to CSV!" + str(e))
        
        return True
    
    def export_to_json(self, filename = "Updated_Dataset.json", overwrite = False):
        """
        Export Dataset to JSON

        Parameters:
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not filename.lower().endswith(".json"):
            raise ValueError("File Extension must be .json!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to json
        try:
            self.dataset.dataset.to_json(filename, orient = "records")
        except Exception as e:
            raise RuntimeError("Cannot export to JSON!" + str(e))
        
        return True
    
    def get_dataframe(self):
        """
        Get Dataset as pandas DataFrame
        """
        return self.dataset.dataset
    
    def export_to_parquet(self, filename = "Updated_Dataset.parquet", overwrite = False):
        """
        Export Dataset to Parquet

        Parameters:
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not filename.lower().endswith(".parquet"):
            raise ValueError("File Extension must be .parquet!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to parquet
        try:
            self.dataset.dataset.to_parquet(filename, index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to PARQUET!" + str(e))
        
        return True
    
    def export_to_excel(self, filename = "Updated_Dataset.xlsx", overwrite = False):
        """
        Export Dataset to Excel

        Parameters:
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not filename.lower().endswith(".xlsx"):
            raise ValueError("File Extension must be .xlsx!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to excel
        try:
            self.dataset.dataset.to_excel(filename, index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to XLSX!" + str(e))
        
        return True
