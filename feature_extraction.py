import collections 
import pandas as pd

amino_acids = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]

def get_attributes(attribute_file_path: str) -> pd.DataFrame:
    """Read attribute values and return an attributes data frame"""

    return pd.read_csv(attribute_file_path)[amino_acids]


def get_occurences(sequence_file_path: str) -> pd.DataFrame:
    """Read protein sequences and return an occurrences data frame"""

    occurrences = []
    with open(sequence_file_path) as sequences:
        for sequence in sequences:
            occurrences.append(collections.Counter(sequence)) # add a dict of amino acid counts
    return pd.DataFrame(occurrences)[amino_acids].fillna(0)


def get_features(occurences: pd.DataFrame, attributes: pd.DataFrame) -> pd.DataFrame:
    """Extract features from the given sequence file using the given attributes.

    Let p = number of protein sequences.
    Let c = number of distinct amino acids
    Let a = numeber of attributes

    Inputs:
        O: Occurrences matrix, p by c
        A: Attributes matrix, a by c
    Output:
        F: Features matrix, p by a
    Computation:
        F = matrix multiplication of (O, transpose(A))

    For each protein sequence, an occurence vector is built consisting of occurence
    counts of amino acids in the sequence. Given multiple sequences, an occurence
    matrix results.

    The attributes matrix is extracted from the attributes data.
    """

    return occurences.dot(attributes.T)


def write_features(features_file_path: str, features: pd.DataFrame) -> None:
    """Write the given features to a file."""

    features.to_csv(features_file_path, index=False, header=False)


if __name__ == "__main__":
    data_path = "./data/"
    attributes = get_attributes(data_path + "attributes.csv")
    occurences = get_occurences("given/Sequence.txt")
    features = get_features(occurences, attributes)
    write_features(data_path + "features_55attrib.csv", features)
