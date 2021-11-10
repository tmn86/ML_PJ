[<--README.md](../README.md)

# Introduction

## Overview
We implemented a complete process of multi-class classification using machine learning, including feature extraction, data preparation, training of classification models, prediction using the trained models, and analysis of results. The problem at hand was protein subcellular localization, or identifying in which part of the cell a protein functioned, of Gram-positive bacterial proteins, each of which could function in one of four locations in the cell. We were given a data set of 523 Gram-positive protein sequences and their subcellular locations. We divided the data into a training set and a test set. From the training set, we generated and compared multiple machine learning classification models using various algorithms and hyperparameters with cross-validation. Using the test set, we evaluated the performance of the best-performing models from the training phase.


## Given data
The following are the given data that we used in the project:
* #### [`Label.txt`](../given/Label.txt)
    * Contains subcellular locations, represented by numbers 1 through 4, of the 523 protein sequences
    * The labels are the "true answers" to which classification models are trained to approximate with "probably approximately correct" learning
* #### [`Sequence.txt`](../given/Sequence.txt)
    * Contains the amino acid sequences of all 523 proteins, with 20 possible types of amino acids
    * Used to derive occurrence counts of amino acids in the protein sequences for feature extraction
* #### `List of attributes and their values.csv`
    * Contains a list of 55 physicochemical attributes for each amino acid
    * Used to derive feature vectors in combination with amino acid occurrence counts from the protein sequences
* #### [`bigram0.csv`](../given/bigram0.csv), [`bigram1.csv`](../given/bigram1.csv), [`bigram2.csv`](../given/bigram2.csv)
    * Contains counts of two-element combinations with 0 gap, 1 gap, and 2gaps, respectively
    * These bigrams contain information on amino acid sequencing that is not represented by unigram occurrence counts
    * Used to experiment their effects on classification performance


## Tools
We used the following tools to implement the project:
* Programming language
    * [Python 3.8+](https://www.python.org/)
* Libraries:
    * [scikit-learn 0.24.1](https://scikit-learn.org/)
        * perform all machine learning algorithms
        * preprocess data
        * construct pipelines
        * find optimal hyperparameters of a model
    * [pandas 1.2.4](https://pandas.pydata.org/)
        * read from input files
        * write to output files
        * arrange data in tabular format

