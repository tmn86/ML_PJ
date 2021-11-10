from sklearn.model_selection import train_test_split
import pandas as pd

if __name__ == "__main__":
    data_path = "./data/"

    features_types = ["55attrib", "bigram0", "bigram1", "bigram2"]

    X = [pd.read_csv(data_path + f"features_{ft}.csv", header=None) for ft in features_types]
    y = pd.read_csv("./given/Label.txt", header=None)

    splits = train_test_split(*X, y, test_size=0.25, random_state=33, stratify=y)

    output_names = [(f"X_train_{ft}", f"X_test_{ft}") for ft in features_types]
    output_names = [i for s in output_names for i in s] # flatten list
    output_names + ["y_train", "y_test"]
    
    for split, output_name in zip(splits, output_names):
        split.to_csv(data_path + f"{output_name}.csv", index=False, header=False)
