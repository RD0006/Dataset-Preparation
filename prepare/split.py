"""
split.py

Module for splitting the dataset.

Utility functions provided for the following:
- splitting the dataset into training and testing sets
- splitting the dataset into training, testing, and validation sets
"""

import random
from .input import Dataset

class Splitter:

    def __init__(self, dataset):
        """
        Initialize Splitter Object

        Parameters:
        - dataset: Dataset object
        """

        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        self.dataset = dataset
        self.__log = {}

    def __check_args(self, train, test, validate = 0):
        """
        Helper Function to Check Split Ratio
        """

        if abs(train + test + validate - 1.0) > 1e-8:
            raise ValueError("Split Ratio does not sum up to 1.0!")

    def train_test(self, train = None, test = None, shuffle = False):
        """
        Split Dataset into Training and Testing Datasets

        Parameters:
        - train: float
        - test: float
        - shuffle: bool
        """

        # checks
        if train is None and test is None:
            raise ValueError("At least one of train or test arguments must be given!")
        elif train is None:
            train = 1.0 - test
        else:
            test = 1.0 - train    
        self.__check_args(train, test)

        dataset = self.dataset.dataset.copy()
        num_of_rows = self.dataset.num_of_rows
        result = {
            "train" : None,
            "test" : None
        }

        # shuffling, if applicable
        if shuffle:
            dataset = dataset.sample(frac = 1).reset_index(drop = True)
        
        # operation
        n_train = round(train * num_of_rows)
        result["train"] = Dataset(dataset[ : n_train])
        result["test"] = Dataset(dataset[n_train : ])

        # update log
        self.__log.clear()
        self.__log["Number of Rows in train Dataset"] = result["train"].num_of_rows
        self.__log["Number of Rows in test Dataset"] = result["test"].num_of_rows

        return result

    def train_validate_test(self, train = 0.65, validate = 0.10, test = 0.25, shuffle = False):
        """
        Split Dataset into Training, Validation, and Testing Datasets

        Parameters:
        - train: float
        - validate: float
        - test: float
        - shuffle: bool
        """

        # checks
        if [train, test, validate].count(None) > 1:
            raise ValueError("At least two out of train, test, and validate arguments must be given!")
        elif train is None:
            train = 1.0 - test - validate
        elif test is None:
            test = 1.0 - train - validate
        elif validate is None:
            validate = 1.0 - train - test
        self.__check_args(train, test, validate)

        dataset = self.dataset.dataset.copy()
        num_of_rows = self.dataset.num_of_rows
        result = {
            "train" : None,
            "validate" : None,
            "test" : None
        }

        # shuffling, if applicable
        if shuffle:
            dataset = dataset.sample(frac = 1).reset_index(drop = True)
        
        # operation
        n_train = round(train * num_of_rows)
        n_validate = round(validate * num_of_rows)
        result["train"] = Dataset(dataset[ : n_train])
        result["validate"] = Dataset(dataset[n_train : n_train + n_validate])
        result["test"] = Dataset(dataset[n_train + n_validate : ])
        
        # update log
        self.__log.clear()
        self.__log["Number of Rows in train Dataset"] = result["train"].num_of_rows
        self.__log["Number of Rows in validate Dataset"] = result["validate"].num_of_rows
        self.__log["Number of Rows in test Dataset"] = result["test"].num_of_rows

        return result
        
    def get_log(self):
        """
        Get log containing the details of the split dataset
        """
        return self.__log