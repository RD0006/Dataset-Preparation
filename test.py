from prepare import Dataset, Validator, Cleaner, Extender, Splitter, Exporter

dataset = Dataset("kc_house_data.csv")

validator = (
    Validator(dataset, inplace = False)
    .negative_values("floors")
    .null_values("floors")
    .duplicate_values("id")
    .validate_range("bathrooms", 1)
)

cleaner = (
    Cleaner(dataset)
    .handle_missing_values(all_columns = True)
    .handle_outliers(all_columns = True)
    .fix_categoricals(all_columns = True)
    .drop_column("id")
    .drop_column("date")
    .drop_duplicate_rows()
    .normalize(all_columns = True)
    .standardize(all_columns = True)
)

extender = (
    Extender(dataset)
    .add_gaussian_rows()
    .add_duplicate_rows()
    .add_noisy_rows()
)

splitter = Splitter(dataset)
result = splitter.train_test(0.8)

exporter = Exporter()
exporter.export_to_csv(result["train"], "Training_Dataset.csv", overwrite = 0)
exporter.export_to_csv(result["test"], "Testing_Dataset.csv", overwrite = 0)
