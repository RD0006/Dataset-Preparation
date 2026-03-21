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

    def __init__(self):
        """
        Initialize Exporter Object
        """
        pass
    
    def __check_file_overwrite(self, filename, overwrite):
        """
        Helper Function to check if file exists and if overwrite is allowed
        """
        
        if os.path.exists(filename) and not overwrite:
            raise FileExistsError(f"File {filename} already exists and overwrite is set to False!")

    def export_to_csv(self, dataset, sep = ",", filename = "Updated_Dataset.csv", overwrite = False):
        """
        Export Dataset to CSV

        Parameters:
        - dataset: Dataset Object
        - filename: String
        - overwrite: Boolean
        """

        # checks
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        if not filename.lower().endswith(".csv"):
            raise ValueError("File Extension must be .csv!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to csv
        try:
            dataset.dataset.to_csv(filename, sep = sep, index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to CSV!" + str(e))
        
        return True
    
    def export_to_json(self, dataset, filename = "Updated_Dataset.json", overwrite = False):
        """
        Export Dataset to JSON

        Parameters:
        - dataset: Dataset Object
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        if not filename.lower().endswith(".json"):
            raise ValueError("File Extension must be .json!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to json
        try:
            dataset.dataset.to_json(filename, orient = "records", force_ascii = False)
        except Exception as e:
            raise RuntimeError("Cannot export to JSON!" + str(e))
        
        return True
    
    def get_dataframe(self, dataset):
        """
        Get Dataset as pandas DataFrame

        Parameters:
        - dataset: Dataset Object
        """

        # checks
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        
        return dataset.dataset
    
    def export_to_parquet(self, dataset, filename = "Updated_Dataset.parquet", overwrite = False):
        """
        Export Dataset to Parquet

        Parameters:
        - dataset: Dataset Object
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        if not filename.lower().endswith(".parquet"):
            raise ValueError("File Extension must be .parquet!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to parquet
        try:
            dataset.dataset.to_parquet(filename, index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to PARQUET!" + str(e))
        
        return True
    
    def export_to_excel(self, dataset, filename = "Updated_Dataset.xlsx", overwrite = False):
        """
        Export Dataset to Excel

        Parameters:
        - dataset: Dataset Object
        - filename: String
        - overwrite: Boolean
        """
        
        # checks
        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        if not filename.lower().endswith(".xlsx"):
            raise ValueError("File Extension must be .xlsx!")
        self.__check_file_overwrite(filename, overwrite)

        # convert to excel
        try:
            dataset.dataset.to_excel(filename, index = False)
        except Exception as e:
            raise RuntimeError("Cannot export to XLSX!" + str(e))
        
        return True
