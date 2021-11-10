# Machine Learning Group Project
56:198:554 Machine Learning with Professor Dehganzi, Rutgers University-Camden, Spring 2021  
Group: Doug Jih, Galina Karabelova, Thu Minh Nguyen (alphabetical order)

## Objective
Perform a complete process of supervised machine learning including feature extraction, classification, and analysis; given 523 gram-negative protein sequences and their classification labels.

## Report Outline

1. [Introduction](doc/Introduction.md)
    1. Overview
    1. Given data
    1. Tools
1. [Data preparation](doc/DataPreparation.md)
    1. Features selection & extraction
        1. 55-attribute features
        1. Bigrams
    1. Training / Test data split
        1. Effects of stratifying
        1. Training vs. test sizes
    1. Pipelines
    1. Standardization
        1. Effects: with-mean, with-std
1. [Training and cross-validation](doc/Training.md)
    1. Classifiers and hyperparameters used
        1. Logistic Regression
        1. K-Nearest Neighbors 
        1. Multi-layer Perceptron
        1. Random Forest
        1. Support Vector Machine
        1. Adaptive Boosting
        1. Bagging
    1. Hyperparameter search
    1. Cross-validation
    1. Performance comparison
        1. Scoring
        1. Computation time
        1. Findings of interests
5. [Testing using test set](doc/Testing.md)
    1. Importance of independent test set
    1. Evaluation of top performing models
        1. Versus results using training set
        1. Classification Reports
8. [Conclusion](doc/Conclusion.md)
    1. Summary
    1. Lessons learned
    1. Surprises and challenges
    1. What else you might have tried?
    1. What might you have done differently?
