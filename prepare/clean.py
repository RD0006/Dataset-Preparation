"""
clean.py

Module for cleaning the dataset.

Utility functions provided for the following: 
- handling missing values
- removing duplicate rows
- removing outliers - numerical
- fixing categorical variables
- drop columns
- normalization
- standardization
"""

import numpy as np
import pandas as pd
from .input import Dataset

class Cleaner:

    def __init__(self, dataset):
        """
        Initialize Cleaner Object

        Parameters:
        - dataset: Dataset object
        """

        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        self.dataset = dataset
        self.__log = {}
        self.__initial_row_count = self.dataset.num_of_rows
        self.__initial_column_count = self.dataset.num_of_columns

    def __get_column(self, column):
        """
        Get column
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")

        # if column is None
        if column is None:
            return dataset.columns.tolist()
        
        # if column is a string value
        elif isinstance(column, str):
            if column not in dataset.columns:
                raise ValueError(f"Column {column} does not exist!")
            return [column]
        
        # if column is an int value
        elif isinstance(column, int):
            if not (column >= 0 and column < len(dataset.columns)):
                raise ValueError(f"Column index {column} is out of range!")
            return [dataset.columns[column]]
        
        # if column is a list
        elif isinstance(column, list):
            temp = []
            for i in column:
                temp.extend(self.__get_column(i))
            return temp
        
        # otherwise, raise TypeError
        else:
            raise TypeError("Incorrect value type passed as column name or index")
     
    def __handle_missing_numeric_values(self, cols, technique):
        """
        Handle missing numeric values

        Parameters:
        - column: list
        - technique: str
        """
        
        dataset = self.dataset.dataset
        
        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        
        # count of null values
        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()

        # if technique is drop, remove rows with any null values
        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            # if no null values found in column
            if not dataset[i].isnull().any():
                continue

            # if technique is zero, replace nulls with the constant 0
            if technique == "zero":
                dataset.loc[ : , i] = dataset[i].fillna(value = 0)

            # if technique is mean, replace nulls with the mean of the column
            elif technique == "mean":
                dataset.loc[ : , i] = dataset[i].fillna(value = dataset[i].mean())
            
            # if technique is median, replace nulls with the median of the column
            elif technique == "median":
                dataset.loc[ : , i] = dataset[i].fillna(value = dataset[i].median())

            # if technique is mode, replace nulls with the mode of the column
            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset.loc[ : , i] = dataset[i].fillna(value = mode.iloc[0])

            # if type unrecognized
            else:
                raise ValueError("Technique not recognized!")

        return cnt

    def __handle_missing_categorical_values(self, cols, technique):
        """
        Handle missing string values

        Parameters:
        - column: list
        - technique: str
        """

        dataset = self.dataset.dataset

        #checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        
        # count of null values
        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()

        # if technique is drop, remove rows with any null values
        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            # if no nulls found in column
            if not dataset[i].isnull().any():
                continue
            
            # if technique is NA, replace null values with the constant NA
            if technique == "NA":
                dataset.loc[ : , i] = dataset[i].fillna(value = "NA")

            # if technique is empty, replace null values with an empty string
            elif technique == "empty":
                dataset.loc[ : , i] = dataset[i].fillna(value = "")
            
            # if technique is mode, replace nulls with the mode of the column
            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset.loc[ : , i] = dataset[i].fillna(value = mode.iloc[0])

            # if technique unrecognized
            else:
                raise ValueError("Technique not recognized!")

        return cnt

    def __handle_missing_boolean_values(self, cols, technique):
        """
        Handle missing boolean values

        Parameters:
        - column: list
        - technique: str
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        
        # count of null values
        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()
        
        # if technique is drop, remove rows with any null values
        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            # if no nulls found in column
            if not dataset[i].isnull().any():
                continue
            
            # if technique is False, replace nulls with bool False
            if technique == "False":
                dataset.loc[ : , i] = dataset[i].fillna(value = False)

            # if technique is True, replace nulls with bool True
            elif technique == "True":
                dataset.loc[ : , i] = dataset[i].fillna(value = True)
            
            # if technique is mode, replace nulls with the mode of the column
            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset.loc[ : , i] = dataset[i].fillna(value = mode.iloc[0])

            # if technique unrecognized
            else:
                raise ValueError("Technique not recognized!")

        return cnt

    def handle_missing_values(self, column = None, all_columns = False, numeric = "zero", categorical = "NA", boolean = "False"):
        """
        Handle missing values

        Parameters:
        - column: str, int, or list
        - numeric: str
        - categorical: str
        - boolean: str
        """

        dataset = self.dataset.dataset
        
        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        # get columns
        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        numeric_list = []
        categorical_list = []
        boolean_list = []

        for i in cols:
            
            # boolean columns
            if pd.api.types.is_bool_dtype(dataset[i]):
                boolean_list.append(i)
            
            # numeric columns
            elif pd.api.types.is_numeric_dtype(dataset[i]):
                numeric_list.append(i)

            # categorical columns
            elif pd.api.types.is_string_dtype(dataset[i]) or pd.api.types.is_object_dtype(dataset[i]):
                categorical_list.append(i)
            
            # type error
            else:
                raise TypeError(f"Invalid type detected in column {i}!")
        
        # call helper functions
        cnt = 0
        if numeric_list:
            cnt += self.__handle_missing_numeric_values(numeric_list, numeric)
        if categorical_list:
            cnt += self.__handle_missing_categorical_values(categorical_list, categorical)
        if boolean_list:
            cnt += self.__handle_missing_boolean_values(boolean_list, boolean)

        # update log
        self.__log["Null Values"] = cnt

        return self

    def drop_duplicate_rows(self):
        """
        Drop duplicate rows
        """

        dataset = self.dataset.dataset
        
        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        
        # operation
        cnt = dataset.duplicated().sum()
        dataset.drop_duplicates(inplace = True)
        
        # update log
        self.__log["Duplicate Rows"] = cnt

        return self

    def handle_outliers(self, column = None, all_columns = False, technique = "iqr"):
        """
        Handle outliers from numerical column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        - technique: str
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        # get columns
        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        # get numeric columns
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for outlier fixing!")

        cnt = 0

        indices = set()

        dataset[cols] = dataset[cols].astype("float")

        for i in cols:

            # if technique is drop, remove all rows having any outliers detected by IQR method
            if technique == "drop":
                q1 = dataset[i].quantile(0.25)
                q3 = dataset[i].quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                mask = (dataset[i] < lower) | (dataset[i] > upper)
                cnt += mask.sum()
                indices.update(dataset[mask].index)

            # if technique is iqr, fix all outliers found using IQR method
            elif technique == "iqr":
                q1 = dataset[i].quantile(0.25)
                q3 = dataset[i].quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                lower_mask = dataset[i] < lower
                upper_mask = dataset[i] > upper
                cnt += lower_mask.sum() + upper_mask.sum()
                dataset.loc[lower_mask, i] = lower
                dataset.loc[upper_mask, i] = upper

            # if technique is zscore, fix all outliers found using z-score method
            elif technique == "zscore":
                mean, std = dataset[i].mean(), dataset[i].std()
                lower, upper = mean - 3 * std, mean + 3 * std
                lower_mask = dataset[i] < lower
                upper_mask = dataset[i] > upper
                cnt += lower_mask.sum() + upper_mask.sum()
                dataset.loc[lower_mask, i] = lower
                dataset.loc[upper_mask, i] = upper

            # if technique unrecognized
            else:
                raise ValueError("Technique not recognized!")
        
        if technique == "drop":
            dataset.drop(index = list(indices), inplace = True)
        
        # update log
        self.__log["Outlier Values Handled"] = cnt

        return self

    def fix_categoricals(self, column = None, all_columns = False, technique = "lower"):
        """
        Fix categorical columns

        Parameters:
        - column: str, int, or list
        - all_columns: boolean
        - technique: str
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        # get columns
        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        # get string columns
        cols = [c for c in cols if pd.api.types.is_string_dtype(dataset[c]) or pd.api.types.is_object_dtype(dataset[c])]
        if not cols:
            raise ValueError("No categorical columns found!")
                    
        for i in cols:

            # if technique is lower, converts all values in column to lowercase and strips whitespaces
            if technique == "lower":
                dataset.loc[ : , i] = dataset[i].str.strip().str.lower()

            # if technique is upper, converts all values in column to uppercase and strips whitespaces
            elif technique == "upper":
                dataset.loc[ : , i] = dataset[i].str.strip().str.upper()

            # if type unrecognized
            else:
                raise ValueError("Technique not recognized!")
            
        # update log
        self.__log["Categoricals Fixed"] = len(cols)

        return self
    
    def drop_column(self, column = None, all_columns = False):
        """
        Drop column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        
        # get columns
        if all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        # drop columns
        dataset.drop(cols, axis = 1, inplace = True)

        # update log
        self.__log["Dropped Columns"] = len(cols)

        return self

    def normalize(self, column = None, all_columns = False):
        """
        Normalize column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        # get columns
        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        # get numeric columns
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for normalization!")

        cnt = 0

        dataset[cols] = dataset[cols].astype(float)

        for i in cols:

            # normalization
            min_val = dataset[i].min()
            temp = (dataset[i].max() - min_val)
            if temp != 0:
                dataset.loc[ : , i] = (dataset[i] - min_val) / temp
                cnt += 1
            else:
                continue

        # update log
        self.__log["Normalized Columns"] = cnt

        return self


    def standardize(self, column = None, all_columns = False):
        """
        Standardize column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        # checks
        if dataset.empty:
            raise RuntimeError("Dataset is empty!")
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        # get columns
        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        # get numeric columns
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for standardization!")

        cnt = 0

        dataset[cols] = dataset[cols].astype(float)

        for i in cols:

            # standardization
            if dataset[i].std() != 0:
                dataset.loc[ : , i] = (dataset[i] - dataset[i].mean()) / dataset[i].std()
                cnt += 1
            else:
                continue
            
        # update log
        self.__log["Standardized Columns"] = cnt

        return self

    def get_log_of_fixed_issues(self):
        """
        Get log containing the list of all issues that were fixed
        """
        
        log = self.__log.copy()

        log[("Complete Dataset", "Total Number of Rows Removed")] = self.__initial_row_count - self.dataset.num_of_rows
        log[("Complete Dataset", "Total Number of Rows Remaining")] = self.dataset.num_of_rows
        log[("Complete Dataset", "Percentage of Dataset Rows Remaining")] = self.dataset.num_of_rows / self.__initial_row_count * 100

        log[("Complete Dataset", "Total Number of Columns Removed")] = self.__initial_column_count - self.dataset.num_of_columns
        log[("Complete Dataset", "Total Number of Columns Remaining")] = self.dataset.num_of_columns
        log[("Complete Dataset", "Percentage of Dataset Columns Remaining")] = self.dataset.num_of_columns / self.__initial_column_count * 100

        return log