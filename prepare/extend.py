"""
extend.py

Module for extending the dataset.

Utility functions provided for the following:
- adding duplicate rows
- balancing classes - SMOTE
- adding Gaussian rows
- adding noise
"""

# add checks

import numpy as np
import pandas as pd
from .input import Dataset

class Extender:

    def __init__(self, dataset):
        """
        Initialize Extender Object

        Parameters:
        - dataset: Dataset object
        """

        if not isinstance(dataset, Dataset):
            raise TypeError("Dataset object not received!")
        self.dataset = dataset
        self.__log = {}
        self.__initial_row_count = self.dataset.num_of_rows
        self.__count_of_rows = 0

    def add_gaussian_rows(self, n_rows = 10, random_state = 42):
        """
        Add Gaussian Rows to Dataset

        Parameters:
        - n_rows: int
        - random_state: int
        """

        rng = np.random.default_rng(random_state)

        dataset = self.dataset.dataset.copy()

        # get numerical and categorical columns         
        num_cols = [c for c in dataset.columns if pd.api.types.is_numeric_dtype(dataset[c])]
        cat_cols = [c for c in dataset.columns if pd.api.types.is_object_dtype(dataset[c]) or pd.api.types.is_categorical_dtype(dataset[c])]

        # means and standard deviations
        means = dataset[num_cols].mean()
        stds = dataset[num_cols].std().replace(0, 1e-8)

        new_rows = []

        # operation
        for _ in range(n_rows):

            new_row = {}

            # for numerical columns
            for col in num_cols:
                value = rng.normal(loc = means[col], scale = stds[col])
                new_row[col] = value

            # for categorical columns
            for col in cat_cols:
                new_row[col] = rng.choice(dataset[col].values)

            new_rows.append(new_row)

        # add rows to dataset
        new_dataset = pd.DataFrame(new_rows)
        new_dataset = new_dataset[dataset.columns]
        self.dataset.dataset = pd.concat([dataset, new_dataset], ignore_index = True)

        # ensure that data type integrity is maintained
        for col in num_cols:
            if pd.api.types.is_integer_dtype(dataset[col]):
                self.dataset.dataset[col] = (self.dataset.dataset[col].round().astype(dataset[col].dtype))
        
        self.__count_of_rows += len(new_rows)

        # update log
        self.__log["Number of Gaussian Rows Added"] = len(new_rows)

        return self.dataset.dataset
    
    def balance_classes(self, column, k = 5, random_state = 42):
        """
        Balance classes in Dataset by Adding Required Number of Imbalanced Classes

        Parameters:
        - column: String
        - k: int
        - random_state: int
        """

        # add functionality to give any column type

        np.random.seed(random_state)

        dataset = self.dataset.dataset.copy()
        
        # get numerical and categorical columns
        num_cols = [c for c in dataset.columns if pd.api.types.is_numeric_dtype(dataset[c])]
        cat_cols = [c for c in dataset.columns if pd.api.types.is_object_dtype(dataset[c]) or pd.api.types.is_categorical_dtype(dataset[c])]

        # checks
        if column not in cat_cols:
            raise ValueError(f"Categorical column {column} is not present in dataset!")
        
        # get required class counts and major class
        classes_count = dataset[column].value_counts()
        max_count = classes_count.max()

        new_rows = []

        # operation
        for class_, count in classes_count.items():
            dataset_class = dataset[dataset[column] == class_].copy()

            if count < max_count and len(dataset_class) > 1:               
                req = max_count - count
                class_values = dataset_class[num_cols].values
                effective_k = min(k, len(class_values) - 1)

                 # synthetic row generation
                for _ in range(req):

                    idx = np.random.randint(0, len(class_values))
                    sample = class_values[idx]

                    distances = np.linalg.norm(class_values - sample, axis = 1)
                    nearest_idx = np.argsort(distances)[1 : effective_k + 1]
                    if len(nearest_idx) == 0:
                        continue
                    neighbor_idx = np.random.choice(nearest_idx)
                    neighbor = class_values[neighbor_idx]

                    gap = np.random.rand()
                    synthetic_sample = sample + gap * (neighbor - sample)

                    new_row = {}

                    for col, value in zip(num_cols, synthetic_sample):
                        new_row[col] = value

                    new_row[column] = class_

                    for cat in cat_cols:
                        if cat != column:
                            new_row[cat] = np.random.choice(dataset_class[cat].values)
                    
                    new_rows.append(new_row)

        # add rows to dataset
        if new_rows:
            new_dataset = pd.DataFrame(new_rows)
            new_dataset = new_dataset[dataset.columns]
            self.dataset.dataset = pd.concat([dataset, new_dataset], ignore_index = True)

            # ensure that data type integrity is maintained
            for col in num_cols:
                if pd.api.types.is_integer_dtype(dataset[col]):
                    self.dataset.dataset[col] = (self.dataset.dataset[col].round().astype(dataset[col].dtype))

        self.__count_of_rows += len(new_rows)

        # update log
        self.__log["Number of Rows Added for Balancing Classes"] = len(new_rows)

        return self.dataset.dataset
    
    def add_duplicate_rows(self, n_rows = 20, random_state = 42):
        """
        Add Duplicate Rows to Dataset

        Parameters:
        - n_rows: int
        - random_state: int
        """
        
        rng = np.random.default_rng(random_state)
        dataset = self.dataset.dataset.copy()

        # operation to get duplicate rows
        duplicate_indices = rng.choice(dataset.index, size = n_rows, replace = True)
        duplicates = dataset.loc[duplicate_indices].copy()

        # add new rows to dataset
        self.dataset.dataset = pd.concat([dataset, duplicates], ignore_index = True)

        self.__count_of_rows += n_rows

        # update log
        self.__log["Number of Duplicate Rows Added"] = n_rows

        return self.dataset.dataset

    def add_noisy_rows(self, noise_level = 0.01, n_rows = 10, random_state = 42):
        """
        Add Noisy Rows to Dataset

        Parameters:
        - noise_level: float
        - n_rows: int
        - random_state: int
        """

        rng = np.random.default_rng(random_state)
        dataset = self.dataset.dataset.copy()
        
        # get numerical and categorical columns
        num_cols = [c for c in dataset.columns if pd.api.types.is_numeric_dtype(dataset[c])]
        cat_cols = [c for c in dataset.columns if pd.api.types.is_object_dtype(dataset[c]) or pd.api.types.is_categorical_dtype(dataset[c])]

        new_rows = []

        # operation
        for _ in range(n_rows):

            # sampling
            row = dataset.sample(n = 1, random_state = int(rng.integers(1e9))).iloc[0].copy()
            
            new_row = {}
            
            # for numerical columns
            for col in num_cols:
                std = dataset[col].std() if dataset[col].std() > 0 else 1e-8
                noise = rng.normal(0, noise_level * std)
                new_row[col] = row[col] + noise

            # for categorical columns
            for col in cat_cols:
                new_row[col] = row[col]

            new_rows.append(new_row)

        # add new rows to dataset
        new_dataset = pd.DataFrame(new_rows)
        new_dataset = new_dataset[dataset.columns]
        self.dataset.dataset = pd.concat([dataset, new_dataset], ignore_index = True)

        # ensure that data type integrity is maintained 
        for col in num_cols:
            if pd.api.types.is_integer_dtype(dataset[col]):
                self.dataset.dataset[col] = self.dataset.dataset[col].round().astype(dataset[col].dtype)

        self.__count_of_rows += len(new_rows)

        # update log
        self.__log["Number of Noisy Rows Added"] = len(new_rows)

        return self.dataset.dataset
        
    def get_log(self):
        """
        Get log containing the details of rows added
        """
        
        log = self.__log
        log[("Complete Dataset", "Total Number of Rows Added")] = self.__count_of_rows
        log[("Complete Dataset", "Percentage Increase of Rows")] = (self.dataset.num_of_rows - self.__initial_row_count) / self.__initial_row_count * 100
        return log