from prepare.input import Dataset
from prepare.validate import *

dataset = Dataset("kc_house_data.csv")

# print(dataset)

print("DATASET DETAILS")
print(dataset.head())
print(dataset.tail())
print(dataset.num_of_rows)
print(dataset.num_of_columns)
print(dataset.shape)
print(dataset.columns)
print()

validator = Validator(dataset, inplace = False)
validator.negative_values("floors").null_values("floors").duplicate_values("id").validate_range("bathrooms", 1)

print("LOGS")
log = validator.get_log()
for i in log:
    print(i, log[i])
validator.drop_invalid_rows()
print()

print("DATASET DETAILS")
print(dataset.num_of_rows)
print(dataset.num_of_columns)
print(dataset.shape)
print(dataset.columns)
print()

print("LOG")
log = validator.get_log()
for i in log:
    print(i, log[i])
