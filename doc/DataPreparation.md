[<--README.md](../README.md)

# Data preparation

We needed to prepare data before we could train classification models, because the data as given were not immediately usable.

The desirable form of data consists of training vectors and target values. Training vectors consist of features in columns and data samples in rows. Target values consist of a single column and classification values in rows. Classification models try to map training vectors to target values using various algorithms and error measures. The end goal is to have a classification model that predicts well on data that were *not* used in its training.

## Features selection & extraction

Good features are essential for successful classification by machine learning, because features are inputs to classification models. In this project, we experimented with a 55-attribute feature vector and bigram vectors.

### 55-attribute features

As the baseline, we computed a 55-attribute feature vector for each of the 523 protein sequences. Each feature vector consisted of 55 numerical values, where each of which was a sum of products of amino acid occurrence counts and amino acid physicochemical attribute values. In specific:

```
    Let p = number of protein sequences, c = number of distinct amino acids, a = number of attributes
    Inputs:
        O: Occurrences matrix, p by c
        A: Attributes matrix, a by c
    Output:
        F: Features matrix, p by a
    Computation:
        F = matrix multiplication of (O, transpose(A))
```

For example, if in a fictitious protein sequence amino acid "A" has an a attribute value of 3.2 and occurs 4 times, amino acid "B" has an attribute value of 7.4 and occurs 1 time, then the resulting feature value is 3.2 * 4 + 7.4 * 1 = 20.2.

The resulting feature vectors in this case were a 523-by-55 matrix.

Not knowing the specifics of protein physicochemical properties, we can nevertheless infer some likely pros and cons of these feature vectors:
* Pros: Incorporates a diverse set of 55 physicochemical properties
* Cons: Does not at all account for the sequencings or structures of the proteins; only aggregate counts of individual amino acid types

We wrote the [`feature_extraction.py`](../feature_extraction.py) Python script to generate the 55-attribute features file [`features_55attrib.csv`](../data/features_55attrib.csv).

### Bigrams

We were also given three bigrams data files, [bigram0.csv](../given/bigram0.csv), [bigram1.csv](../given/bigram0.csv) and [bigram2.csv](../given/bigram0.csv). These contained counts of two-element combinations with 0 gap, 1 gap, and 2 gaps, respectively. Given 20 amino acid types, there are 20 * 20 = 400 combinations of bigrams. In case of 0 gap, the two elements in a bigram are immediately consecutive. In case of 1 gap, the two elements in a bigram have one other amino acid in between; and in case of 2 gap, two in between.

Perceived pros and cons:
* Pros: Contain information on amino acid sequencing
* Cons:
    * We did not have physicochemical properties at hand to use with bigrams;
    * Larger feature size of 400 will be more computationally expensive and can cause some models more difficulty in fitting

For the bigrams feature vectors, we simply used the given files except with the header row and label column removed.

## Training / Test data split

In machine learning, the ability of a learning model to generalize is key. Being able to fit a given set of inputs and outputs is not the goal; being able to accurately **predict** outputs using previously unseen inputs is the goal.

To have an objective test of a model's ability to generalize, it is a standard practice in machine learning to split data into training and test sets. The test set will only be used in the final evaluation of trained models, but not anytime during data standardization and training, to ensure that no information from the test set leaks into the training set.

For data split, we wrote the [`data_split.py`](../data_split.py) Python script. In the script, we use the scikit-learn [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) function to split the several feature sets and labels. We used the following parameters:
* `test_size=0.25` -- This allocates 25% of data samples to the test set, and the remaining 75% to the training set. This is the default behavior of the function.
* `random_state=33` -- Setting this to a fixed value ensures repeatability. The choice of number is arbitrary.
* `stratify=y` -- This asks the function to stratify according to `y`, which is the labels vector.

### Effects of stratifying

Stratifying ensures that the data are split in a way to preserve the relative proportions of different classes in the training and test sets. With the given labels in this project, the counts of classes are as follows:

|Class|Count|Proportion|
--- | --- | ---
|1|174|33.3%|
|2|18|3.4%|
|3|208|39.8%|
|4|123|23.5%|

With stratifying enabled, `train_test_split` maintains the proportions of the classes in the resulting two sets.

### Training vs. test sizes

Selecting training versus test sizes is a trade-off. On the one hand, having more data samples for training tends to produce better-fitting models. On the other hand, having more data samples for test helps to better evaluate model's generalized performance.

There is no definite right answer. Usual suggestions give training a majority of data samples. `train_test_split` has a default behavior of giving 25% to the test set. This was what we used.

## Pipelines

Scikit-learn provides a [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) class to help chain multiple stages of machine learning processes. It provides both convenience and safety:
* Convenience: It allows us to specify the constituent components once, and run fitting and prediction on all of them in the correct sequence without having to individually invoking them
* Safety: It helps prevents data leakage from the test set to the training set, by ensuring the same data are consistently used throughout the stages

Given the benefits and recommendations by scikit-learn, we used pipelines in the project.

## Standardization

The last thing we considered before training classification models was *standardization* of features data. According to scikit-learn, "Standardization of datasets is a common requirement for many machine learning estimators implemented in scikit-learn" (https://scikit-learn.org/stable/modules/preprocessing.html#standardization-or-mean-removal-and-variance-scaling).

Scikit-learn provides a [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) class that implements the standardization. In standardization, the mean and standard deviation of each feature's values across the training data samples are calculated, and each feature value is adjusted as follows:

```
    z = (x - u) / s, where x is a data sample, u is the mean of training samples, and s is the standard deviation of training samples
```

### Effects: with-mean, with-std

`StandardScaler` has options to individually enable or disable centering by mean (`with-mean`) and scaling by standard deviation (`with-std`).

Centering by mean could be undesirable for sparse data (with a lot of zero values), whereas there is no obvious downside to scaling by standard deviation, except for some extra computation that is easy and fast for computers.

We did a trial run of using the four combinations of `with-mean` and `with-std` on various classifiers with their default parameters to get a sense of how the `StandardScaler` with the different combinations of parameters affected the classifiers' training accuracy.

#### Logistic Regression

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:----------------------------------------|
|                 1 |          0.6889   |        0.0438169 |       0.0464006 | {'with_std': True, 'with_mean': True}   |
|                 2 |          0.686336 |        0.0327726 |       0.0421977 | {'with_std': True, 'with_mean': False}  |
|                 3 |          0.668387 |        0.0133869 |       0.0476029 | {'with_std': False, 'with_mean': True}  |
|                 4 |          0.624895 |        0.0209376 |       0.0375916 | {'with_std': False, 'with_mean': False} |

#### K-Nearest Neighbors

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:----------------------------------------|
|                 1 |          0.584193 |        0.0649371 |      0.00519876 | {'with_std': True, 'with_mean': True}   |
|                 1 |          0.584193 |        0.0649371 |      0.00519981 | {'with_std': True, 'with_mean': False}  |
|                 3 |          0.479422 |        0.0427352 |      0.0046001  | {'with_std': False, 'with_mean': True}  |
|                 3 |          0.479422 |        0.0427352 |      0.00419998 | {'with_std': False, 'with_mean': False} |

#### Multi-layer Perceptron

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:-----------------------------------------
|                 1 |          0.688802 |        0.0364244 |       0.348597  | {'with_std': True, 'with_mean': False}  |
|                 2 |          0.683707 |        0.0396014 |       0.382798  | {'with_std': True, 'with_mean': True}   |
|                 3 |          0.426128 |        0.0752833 |       0.0990016 | {'with_std': False, 'with_mean': True}  |
|                 4 |          0.347095 |        0.0720448 |       0.0569999 | {'with_std': False, 'with_mean': False} |

#### Random Forest

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:-----------------------------------------
|                 1 |          0.658293 |        0.05497   |        0.222398 | {'with_std': False, 'with_mean': True}  |
|                 2 |          0.655761 |        0.0540628 |        0.192997 | {'with_std': False, 'with_mean': False} |
|                 3 |          0.635281 |        0.0536122 |        0.202797 | {'with_std': True, 'with_mean': False}  |
|                 4 |          0.635183 |        0.0445895 |        0.217398 | {'with_std': True, 'with_mean': True}   |

#### Support Vector Machine

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:-----------------------------------------
|                 1 |          0.556151 |        0.0321637 |       0.0123973 | {'with_std': True, 'with_mean': True}   |
|                 1 |          0.556151 |        0.0265664 |       0.012599  | {'with_std': True, 'with_mean': False}  |
|                 3 |          0.39023  |        0.0298353 |       0.0118001 | {'with_std': False, 'with_mean': False} |
|                 4 |          0.387699 |        0.0369458 |       0.0133983 | {'with_std': False, 'with_mean': True}  |

#### Adaptive Boosting

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:-----------------------------------------
|                 1 |          0.548523 |        0.0456564 |        0.1436   | {'with_std': True, 'with_mean': True}   |
|                 1 |          0.548523 |        0.0456564 |        0.1482   | {'with_std': False, 'with_mean': True}  |
|                 1 |          0.548523 |        0.0456564 |        0.142999 | {'with_std': True, 'with_mean': False}  |
|                 1 |          0.548523 |        0.0456564 |        0.133798 | {'with_std': False, 'with_mean': False} |

#### Bagging

|   rank_test_score |   mean_test_score |   std_test_score |   mean_fit_time | params                                  |
|------------------:|------------------:|-----------------:|----------------:|:-----------------------------------------
|                 1 |          0.650633 |        0.0557976 |       0.0629991 | {'with_std': False, 'with_mean': False} |
|                 2 |          0.635378 |        0.0366016 |       0.0707995 | {'with_std': True, 'with_mean': True}   |
|                 3 |          0.632782 |        0.0513697 |       0.0679985 | {'with_std': True, 'with_mean': False}  |
|                 4 |          0.627653 |        0.0440032 |       0.0687986 | {'with_std': False, 'with_mean': True}  |

#### Summary
In summary, standardization appears to have different effects on different classifiers:
* `with_std` appears clearly beneficial for
    * Logistic Regression
    * K-Nearest Neighbors
    * Multi-layer Perceptron
    * Support Vector Machine
* `with_std` has no clear effect on
    * Random Forest
    * Adaptive Boosting
    * Bagging
* `with_mean` has no clear effect on any of the classifier

Based on this result, we ran the classification training with both `with_std` and `with_mean` to `True`.