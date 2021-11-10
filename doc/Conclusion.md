[<--README.md](../README.md)

# Conclusion
## Summary
We successfully used Machine Learning in this assignment to classify a multi-class dataset of Gram-positive bacterial proteins. We implemented in code a process that resulted in a classifier that identified each protein's functional location in the cell.

In this project, we had the chance to use seven different classifiers varying from simple algorithms such as "K-Nearest Neighbors" and "Logistic Regression" to more complicated ones such as "Multi-layer Perceptron", "Support Vector Machine"; and also ensemble classifiers that combining multiple weak learners like "Bagging", "Adaptive Boosting", and "Random Forest".

We also had the chance to examine some aspects of data preparation such as feature extraction and scaling.

## Lessons learned

We had learned many interesting things along the way of approaching this project:

- Choosing the right parameters for the algorithm could give a significant change to the accuracy of the results. For example, choosing the right regularization `C` in `Logistic Regression` could give this simple approach 72% of accuracy, but bad `C` could give a bad result which < 50% of accuracy.
- Good feature extraction plays an important role in building good model for prediction. In this project, we mostly used the 55-attribute features because of time constraints. But we also briefly tested using the concatenation of the 55-attribute features and all three bigrams data files.
    * We saw some improvements in Adaptive Boosting and Bagging with the much larger feature vectors (1255 instead of 55), but did not see any clear improvement with the other classifiers.
    * The training time was about an order of magnitude as long with otherwise the same process.
    * We believe that if we could have better feature extraction, however, the result could be improved.
- Time complexity and computational cost are important factors that also decided if an algorithm should be used to train a model. For example, K-Nearest Neighbors give the smallest training time however with lower accuracy. On the other hand, Multi-layer has high accuracy result but much longer training time. 
    * There is a trade-off between accuracy and time complexity that we saw
    * However, with what we had learned, K-Nearest Neighbors would be a lot more expensive with larger data size. Therefore, having basis knowledge of these algorithms definitely benefit us in choosing right model to use in training.
    * Luckily, our data set is small enough that time complexity and computational cost here are trivial.

## Surprises and challenges
- Picking the right parameters was a challenge. As mentioned above, different parameters could give very different outcomes. Thanks to scikit-learn's support for automatic searches for the best parameters, we were able to test try many different parameters and got the best result without having to do so with manually written code.
- Choosing features for features extraction is another challenge that we found was not easy to approach due to our limited knowledge on protein sequences. We decided to use all features to work with and it gave a good overall result.
- Some interesting results we found are:
    * A simple approach with right parameters could give very good outcome.
    * On the other hand, more complicated approach like ensemble classifiers such as Random Forest and Adaptive Boosting did not perform as well as Logistic Regression.
    * Therefore, more complicated methods do not necessarily produce better results. Right methods and right parameters do.

## What else we would like to try
If we have more time, we would like to try:
- More classification algorithms if we have extra time
- Splitting the dataset differently
- Have different features extraction and selection methods
- Feature reduction
- Different validation parameters
- Produce more visualization of the results
