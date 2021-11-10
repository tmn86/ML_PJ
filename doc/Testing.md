[<--README.md](../README.md)

# Testing using test set

Unless otherwise specified, all the resulted are from using the 55-attribute features.

## Importance of independent test set
The testing dataset is a subset of the data, which is independent from the training dataset, but it constitutes of the same probability distribution as the training set for the several classes. We use the test set to evaluate the performance of our model, and see how well it predicts the correct labels of unknown data, also called out-of-sample data. It is important to have an independent test set, because otherwise we may end up having identical or close to similar training and testing datasets, which potentially leads to overfitting. Even though the model will work well on the training set, this will eventually cause the model to perform poorly on any new unfamiliar data. We aim to have two sets that will be independent from one another, but have the same probability distribution.

Please refer to [DataPreparation.md](./DataPreparation.md) for more details about the exact parameters used to achieve the splitting of the data, and to [`data_split.py`](../data_split.py) for the actual implementation.

## Evaluation of top performing models
As mentioned above, the results of our classification model on the test set are indicators of how well the model performs on out-of-sample data. In all our 7 algorithms, we used 75% of the data in the training set, and 25% of it in the test set. Trying with different set of parameters for various algorithms, the best performing sets of hyperparameters for the models produce the following results:

| Classifier             | accuracy, training | f1-score, macro, training | f1-score, weighted, training | accuracy, testing | f1-score, macro, testing | f1-score, weighted, testing |
| ---------------------- | ------------------ | ------------------------- | ---------------------------- | ----------------- | ------------------------ | --------------------------- |
| Logistic Regression    | 73%                | 67%                       | 72%                          | 72%               | 60%                      | 71%                         |
| K-Nearest Neighbors    | 65%                | 48%                       | 63%                          | 57%               | 41%                      | 56%                         |
| Multi-layer Perceptron | 86%                | 84%                       | 86%                          | 76%               | 64%                      | 75%                         |
| Random Forest          | 99%                | 98%                       | 99%                          | 64%               | 56%                      | 64%                         |
| Support Vector         | 84%                | 82%                       | 83%                          | 74%               | 65%                      | 73%                         |
| Adaptive Boosting      | 68%                | 60%                       | 68%                          | 62%               | 53%                      | 61%                         |
| Bagging                | 69%                | 61%                       | 68%                          | 72%               | 54%                      | 72%                         |

The best and worst are:
* Accuracy: as high as 76% for Multi-Layer Perceptron; as low as 57% for K-Nearest Neighbors
* f1-score, macro: as high as 65% for Support Vector Machine; as low as 41% for K-Nearest Neighbors
* f1-score, weighted: as high as 75% for Multi-Layer Perceptron; as low as 56% for K-Nearest Neighbors

Different scoring metrics give different results. **Accuracy** is simply the fraction of predictions that are correct. It is simple, but can give a wrong impression for a dataset that has imbalanced classes, such the dataset this project uses, because accurate predictions in a large class can overwhelm inaccuracy predictions in a small class. **F1 score** is the harmonic average of recall and precision. It equally captures recall and precision, whereas accuracy can let one overwhelm the other. F1 score is usually a better measure for an imbalanced dataset, especially the macro F1 score, which weights all classes equally regardless of their proportion in the dataset.

All the classifiers struggle with the small class 2, with the highest F1 score for class 2 at only 40% by Support Vector Machine.

### Versus results using training set
Once again taking into consideration the best performing set of parameters in the different algorithms, in the majority of the models the difference between the accuracy of the training set and the test set varies at most 10%, with the training set giving the higher score in almost all of them. The one algorithm that showed a significant difference between scores is the Random Forest algorithm with training set accuracy of 99% and testing set accuracy of 64%. That huge gap of performance may indicate overfitting in this specific algorithm. The smaller difference in the rest of the algorithms shows that the data was indeed divided with similar probability distribution in the two sets, and is a good representation of the overall dataset itself.

### Classification Reports
Please refer to the [results folder](../results) to find more detailed information about the performance of each algorithm with various sets of parameters. The bottom of each report file describes the best performing set of hyperparameters for the specific algorithm, and a comparison between the performance on training and test sets is shown. There also is a confusion matrix that gives a good visual representation the correctly and incorrectly labeled data among all combinations of the four classes.
The following is a list of links to the classification reports:
* [Classification Report for Logistic Regression](../results/classification_report_Logistic_Regression.md)
* [Classification Report for K-Nearest Neighbors](../results/classification_report_K-Nearest_Neighbors.md)
* [Classification Report for Multi-layer Perceptron](../results/classification_report_Multi-layer_Perceptron.md)
* [Classification Report for Random Forest](../results/classification_report_Random_Forest.md)
* [Classification Report for Support Vector Machine](../results/classification_report_Support_Vector_Machine.md)
* [Classification Report for Adaptive Boosting](../results/classification_report_Adaptive_Boosting.md)
* [Classification Report for Bagging](../results/classification_report_Bagging.md)
