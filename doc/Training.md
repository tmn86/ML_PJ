[<--README.md](../README.md)

# Training and cross-validation

With data preparation done, we trained classification models and compared them. We wrote the [`classification.py`](../classification.py) Python script to perform the following steps:
1. Load training data
1. Set up pipelines of scalers, classifiers, and their hyperparameters
1. Fit the pipelines using combinations of specified scalers, classifiers, and hyperparameters
1. Score the different combinations using cross-validation
1. Save the top-scoring models
1. Record the training, cross-validation, and testing results

Unless otherwise specified, all the resulted are from using the 55-attribute features.

We will discuss the steps in the following sub-sections.

## Classifiers and hyperparameters used

The following are the classifiers and hyperparameters we tried:

| Classifier             | Hyperparameters                                         |
|:-----------------------|:--------------------------------------------------------|
| Logistic Regression    | C                                                       |
| K-Nearest Neighbors    | n_neighbors                                             |
| Multi-layer Perceptron | hidden_layer_sizes, activation, learning_rate           |
| Random Forest          | n_estimators, max_depth                                 |
| Support Vector Machine | C, kernel                                               |
| Adaptive Boosting      | base_estimator, n_estimators                            |
| Bagging                | base_estimator, n_estimators, max_samples, max_features |

In the following sub-sections, we will briefly describe each classifier.

### Logistic Regression

Logistic regression is a linear model where the target variable is binary instead of continuous. Therefore, it is used for classification rather than regression, despite its name. It uses the logistic function to model the probabilities of outcomes and to make predictions on unseen data. It uses iterative calculations to optimize its solution. The solution assumes the classes are linearly separable.

In scikit-learn, we used the [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) class. We varied the following parameter to examine its effect:
* `C`: controls how closely the model fits to training data; higher C (lower regularization) would more likely cause overfitting and lower C (higher regularization) would more likely cause underfitting

Also see: [Classification Report for Logistic Regression](../results/classification_report_Logistic_Regression.md)

### K-Nearest Neighbors

K-nearest neighbors (KNN) is a classification model that uses a data point's nearest neighghbors' labels to determine its label. KNN assumes that similar data points are usually close to one another. Therefore, KNN classifies data points based the known data points nearby. KNN is a simple algorithm without a training process, and it can be used for both classification and regression. However, the accuracy of KNN is not impressive, and for large data sets, the memory requirement can be high (but it is not an issue for this project with a small data set).

In scikit-learn, we used the [`KNeighborsClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) class. We varied the following parameter to examine its effect:
* `n_neighbors`: controls the number of nearest neighbors to consider

Also see: [Classification Report for K-Nearest Neighbors](../results/classification_report_K-Nearest_Neighbors.md)

### Multi-layer Perceptron

Multi-layer perceptron (MLP) is a class of feed-forward artificial neural network. A perceptron in this case is a single neuron model that was a precursor to larger neural networks. MLP consists of three types of layers: the input layer, the output layer, and the hidden layers. The required task such as prediction and classification are performed by the output layer. An arbitrary number of hidden layers that are placed in between the input and output layer are the true computational engine of the MLP. Similar to a feed forward network in an MLP the data flows in the forward direction from input to output layer. MLP uses backpropagation to train its weights. The major use cases of MLP are pattern classification, recognition, prediction and approximation.

In scikit-learn, we used the [`MLPClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html) class. We varied the following parameters to examine their effects:
* `hidden_layer_sizes`: the number of hidden layers and the number of nodes in each layer
* `activation`: the type of nonlinearity introduced to the model
* `learning_rate`: the step size of algorithm in iterative learning

Also see: [Classification Report for Multi-layer Perceptron](../results/classification_report_Multi-layer_Perceptron.md)

### Random Forest

Random Forest is an ensemble classifier using a collection of independent decision trees to get more accurate and generalized prediction through diversity. Each decision tree in the random forest will give out a class prediction and the class with the most votes become the model's prediction. Although each tree may not perform well, in aggregate the trees reinforce one another and mitigate their individual errors.

In scikit-learn, we used the [`RandomForestClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) class. We varied the following parameters to examine their effects:
* `n_estimators`: the number of trees in the forest
* `max_depth`: the maximum depth of tree

Also see: [Classification Report for Random Forest](../results/classification_report_Random_Forest.md)

### Support Vector Machine

Support vector machine (SVM) is a classifier that finds an optimal hyperplane in an N-dimensional space that distinctly separates the data points with maximum margins. The maximized margin helps SVM avoid overfitting and generalize better on unseen data points.

In scikit-learn, we used the [`SVC`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) class. We varied the following parameters to examine their effects:
* `C`: controls how closely the model fits to training data; higher C (lower regularization) would more likely cause overfitting and lower C (higher regularization) would more likely cause underfitting
* `kernel`: the kernel type to be used in the algorithm; allows fitting to occur in a non-linearly transformed space to classify non-linearly separable data points

Also see: [Classification Report for Support Vector Machine](../results/classification_report_Support_Vector_Machine.md)

### Adaptive Boosting

Adaptive boosting is an ensemble classifier that uses a "weak" classifier but iteratively reruns with increased emphasis on incorrectly predicted inputs to improve the overall accuracy. 

In scikit-learn, we used the [`AdaBoostClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html) class. We varied the following parameters to examine their effects:
* `base_estimator`: the base estimator to use
* `n_estimators`: the maximum number of estimators to use

Also see: [Classification Report for Adaptive Boosting](../results/classification_report_Adaptive_Boosting.md)

### Bagging

Bagging is an ensemble classifier that repeatedly and samples a subset of data samples and features to form multiple classification models, and aggregates them to form an overall classification model. By 

In scikit-learn, we used the [`BaggingClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html) class. We varied the following parameters to examine their effects:
* `base_estimator`: the base estimator to use
* `n_estimators`: the number of estimators in the ensemble
* `max_samples`: the percentage of samples to draw (with replacement by default) for each base estimator
* `max_features`: the percentage of features to draw (without replacement by default) for each base estimator

Also see: [Classification Report for Bagging](../results/classification_report_Bagging.md)

## Hyperparameter search

To help evaluate classification performance, we used scikit-learn's [`RandomizedSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html) class. A `RandomizedSearchCV` accepts a list of "estimator" objects and a list of parameter distributions, and in its `fit` method implements an randomized search over up to the specified number of combinations in the given parameter search space. It evaluates each combination's score with cross-validation, and after its `fit` has completed, it makes available the cross-validation results and the best estimator.

We also experimented with [`GridSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html), an exhaustive search over all combinations of the given parameter values. The `GridSearchCV` has the advantage of being easier to set up and predictable, but the disadvantage of being less computationally inefficient. Scikit-learn has a few other brute force parameter search methods: `HalvingGridSearchCV`, and `HalvingRandomSearchCV`. In these other methods, the search is not simply over all combinations of parameters, but each step in the search is influenced by the result of the previous step, giving to higher computational efficiency.

Using a library facility to assist in the hyperparameter search is usually preferable over writing manual loops by hand, because the library is likely more flexible, better tested, and better tuned for performance.

## Cross-validation

Validation is the assessment of a model's ability to generalize to unseen data. In this regard, validation is similar to testing. However, in the usual practice, validation is used to tune a model, whereas testing is used to only evaluate the model and does not feedback. In this way, testing results are the only truly unbiased evaluation of a model, because they have had no influence in the development of the model.

In validation, the training data is split into training and validation parts. Doing so, however, reduces the number of data samples available for training. **Cross-validation** is a common technique to work around the problem. With cross-validation, the training data do not need to be explicitly split into training and validation parts. Instead, a cross-validation algorithm trains a model multiple times, and each time it leaves out a part of the training data for validation.

N-fold cross-validation trains a model N times. In each round, it uses (N-1) / N of training data for training and validates against the remaining 1 / N of data. In this way, all training data are used for both training and validation, but in each round, there is also unbiased validation. The end result *does* have a bias because the results of multiple rounds are used to guide the selection of the "best" model. Also, N-fold cross-validation increases computation time by approximately N times. However, theory and practice indicate that benefits outweigh costs in using cross-validation.

In scikit-learn, `RandomizedSearchCV` has a default cross-validation behavior of using a [`StratifiedKFold`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html) with 5 folds. We used this default setting.

## Performance comparison

The best results, by weighted F1 score, from each type of classifier are listed below:

|   mean_test_f1_weighted |   mean_test_balanced_accuracy |   mean_fit_time | params                                                                                                                                                                                                               |
|------------------:|-----------------:|----------------:|:---------------------------------------------------------------------------------------------------------------------------|
|                0.685409 |                      0.609463 |       0.0452001 | {'logisticregression__C': 302.34514136199306}    |
|                0.585614 |                      0.454633 |      0.00439992 | {'kneighborsclassifier__n_neighbors': 11} |
|                0.719908 |                      0.624777 |        1.777    | {'mlpclassifier__learning_rate': 'constant', 'mlpclassifier__hidden_layer_sizes': (200, 200), 'mlpclassifier__activation': 'relu'}             |
|                0.656029 |                      0.502304 |       0.801401  | {'randomforestclassifier__n_estimators': 385, 'randomforestclassifier__max_depth': 64}   |
|                0.71152  |                      0.594949 |      0.0170003  | {'svc__C': 215.67367368699792, 'svc__kernel': 'rbf'}       |
|                0.58905  |                      0.481307 |      0.0827989  | {'adaboostclassifier__n_estimators': 27, 'adaboostclassifier__base_estimator': None}                    |
|                0.664766 |                      0.56102  |       2.2036    | {'baggingclassifier__base_estimator': LogisticRegression(), 'baggingclassifier__max_features': 0.9585799791154637, 'baggingclassifier__max_samples': 0.7381075229817785, 'baggingclassifier__n_estimators': 55}      |

### Scoring

There are many scoring metrics. We chose weighted F1 score, because according to the scikit-learn documentation, it appeared to be the better choice for an imbalanced data set like the one we had.

### Computation time

Bagging and Multi-layer Perceptron are much more computationally expensive than the others.

Support vector machine and logistic regression are quite fast.

K-nearest neighbors is by far the fastest.

## Findings of interests

We observed that scikit-learn's [`SVC`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html), C-Support Vector Classification, often failed to converge to a solution on our 55-attribute training data with the linear kernel, if the data were not first standardized by standard deviation. Notably, scikit-learn's `SVC` does not by default limit the maximum number of iterations its solver runs. By setting its `max_iter` parameter, we could prevent it from running for too long. 
