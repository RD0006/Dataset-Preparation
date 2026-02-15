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
from input import Dataset

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
        self.log = {}

    def __get_column(self, column):
        """
        Get column
        """

        dataset = self.dataset.dataset

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
        
        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()

        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            if not dataset[i].isnull().any():
                continue

            if technique == "zero":
                dataset[i].fillna(value = 0, inplace = True)

            elif technique == "mean":
                dataset[i].fillna(value = dataset[i].mean(), inplace = True)
            
            elif technique == "median":
                dataset[i].fillna(value = dataset[i].median(), inplace = True)

            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset[i].fillna(value = mode.iloc[0], inplace = True)

            else:
                raise ValueError("Technique not recognized!")

        return cnt

    def __handle_missing_string_values(self, cols, technique):
        """
        Handle missing string values

        Parameters:
        - column: list
        - technique: str
        """

        dataset = self.dataset.dataset
        
        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()

        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            if not dataset[i].isnull().any():
                continue

            if technique == "NA":
                dataset[i].fillna(value = "NA", inplace = True)

            elif technique == "empty":
                dataset[i].fillna(value = "", inplace = True)
            
            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset[i].fillna(value = mode.iloc[0], inplace = True)

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

        cnt = 0
        for i in cols:
            cnt += dataset[i].isnull().sum()
        
        if technique == "drop":
            dataset.dropna(subset = cols, inplace = True)
            return cnt
        
        for i in cols: 
            
            if not dataset[i].isnull().any():
                continue

            if technique == "False":
                dataset[i].fillna(value = False, inplace = True)

            elif technique == "True":
                dataset[i].fillna(value = True, inplace = True)
            
            elif technique == "mode":
                mode = dataset[i].mode()            
                if mode.empty:
                    raise ValueError(f"Column {i} has no mode!")
                dataset[i].fillna(value = mode.iloc[0], inplace = True)

            else:
                raise ValueError("Technique not recognized!")

        return cnt

    def handle_missing_values(self, column = None, all_columns = False, numeric = "zero", string = "NA", boolean = "False"):
        """
        Handle missing values

        Parameters:
        - column: str, int, or list
        - numeric: str
        - string: str
        - boolean: str
        """

        dataset = self.dataset.dataset
        
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        numeric_list = []
        string_list = []
        boolean_list = []

        for i in cols:
            
            if pd.api.types.is_numeric_dtype(dataset[i]):
                numeric_list.append(i)

            elif pd.api.types.is_string_dtype(dataset[i]):
                string_list.append(i)
            
            elif pd.api.types.is_bool_dtype(dataset[i]):
                boolean_list.append(i)
            
            else:
                raise TypeError(f"Invalid type detected in column {i}!")
        
        cnt = 0
        if numeric_list:
            cnt += self.__handle_missing_numeric_values(numeric_list, numeric)
        if string_list:
            cnt += self.__handle_missing_string_values(string_list, string)
        if boolean_list:
            cnt += self.__handle_missing_boolean_values(boolean_list, boolean)

        self.log["Null Values"] = cnt

        return self

    def remove_duplicate_rows(self, column = None, all_columns = False):
        """
        Remove duplicate rows

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset
        
        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cnt = dataset.duplicated().sum()
            dataset.drop_duplicates(inplace = True)
        else:
            cols = self.__get_column(column)
            cnt = dataset.duplicated(subset = cols).sum()
            dataset.drop_duplicates(subset = cols, inplace = True)
        
        self.log["Duplicate Rows"] = cnt

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

        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for outlier fixing!")

        cnt = 0

        for i in cols:

            if technique == "drop":
                q1 = dataset[i].quantile(0.25)
                q3 = dataset[i].quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                mask = (dataset[i] < lower) | (dataset[i] > upper)
                cnt += mask.sum()
                dataset.drop(dataset[mask].index, inplace = True)

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

            elif technique == "zscore":
                mean, std = dataset[i].mean(), dataset[i].std()
                lower, upper = mean - 3 * std, mean + 3 * std
                lower_mask = dataset[i] < lower
                upper_mask = dataset[i] > upper
                cnt += lower_mask.sum() + upper_mask.sum()
                dataset.loc[lower_mask, i] = lower
                dataset.loc[upper_mask, i] = upper
            else:
                raise ValueError("Technique not recognized!")
        
        self.log["Outliers Handled"] = cnt

        return self

    def fix_categoricals(self, column = None, all_columns = False, technique = "label"):
        """
        Fix categorical columns

        Parameters:
        - column: str, int, or list
        - all_columns: boolean
        - technique: str
        """

        dataset = self.dataset.dataset

        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        cols = [c for c in cols if pd.api.types.is_string_dtype(dataset[c])]
        if not cols:
            raise ValueError("No categorical columns found!")
        
        def value_to_lower_case(x):
            try:
                return x.lower()
            except AttributeError:
                return x
        
        def value_to_upper_case(x):
            try:
                return x.upper()
            except AttributeError:
                return x
                    
        for i in cols:

            if technique == "label":
                dataset[i] = pd.Categorical(dataset[i]).codes
                dataset[i] = dataset[i].replace(-1, np.nan)

            elif technique == "onehot":
                nan_mask = dataset[i].isna()
                temp = pd.get_dummies(dataset[i], prefix = i, drop_first = True)
                dataset.drop(columns = [i], inplace = True)
                for col in temp.columns:
                    dataset[col] = temp[col]
                    dataset.loc[nan_mask, col] = np.nan

            elif technique == "lower":
                dataset[i] = dataset[i].apply(value_to_lower_case)

            elif technique == "upper":
                dataset[i] = dataset[i].apply(value_to_upper_case)

            else:
                raise ValueError("Technique not recognized!")
            
        self.log["Categoricals Fixed"] = len(cols)

        return self
    
    def drop_column(self, column = None, all_columns = False):
        """
        Drop column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        if all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        dataset.drop(cols, axis = 1, inplace = True)

        self.log["Dropped Columns"] = len(cols)

        return self

    def normalize(self, column = None, all_columns = False):
        """
        Normalize column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for normalization!")

        for i in cols:
            temp = (dataset[i].max() - dataset[i].min())
            if temp != 0:
                dataset[i] = (dataset[i] - dataset[i].min()) / temp
            else:
                raise ArithmeticError(f"Column {i} cannot be standardized as max(column) - min(column) is zero")

        self.log["Normalized Columns"] = len(cols)

        return self


    def standardize(self, column = None, all_columns = False):
        """
        Standardize column

        Parameters:
        - column: str, int, or list
        - all_columns: bool
        """

        dataset = self.dataset.dataset

        if column is None and all_columns == False:
            raise ValueError("No column selected!")

        if column is None or all_columns == True:
            cols = dataset.columns.tolist()
        else:
            cols = self.__get_column(column)

        cols = [c for c in cols if pd.api.types.is_numeric_dtype(dataset[c])]
        if not cols:
            raise ValueError("No numeric columns for standardization!")

        for i in cols:
            if dataset[i].std() != 0:
                dataset[i] = (dataset[i] - dataset[i].mean()) / dataset[i].std()
            else:
                raise ArithmeticError(f"Column {i} cannot be standardized as max(column) - min(column) is zero")
            
        self.log["Standardized Columns"] = len(cols)

        return self
