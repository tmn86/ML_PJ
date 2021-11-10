from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils.fixes import loguniform
from timeit import default_timer as timer
import joblib
import matplotlib.pyplot as plt
import os
import pandas as pd
import scipy.stats
import sys
import warnings

start_time = timer()

## Ignore any warnings that appear in classifiers
if not sys.warnoptions:
    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"


data_path = "./data/"
results_path = "./results/"


X_train_55attrib = pd.read_csv(data_path + "X_train_55attrib.csv", header=None)
y_train = pd.read_csv(data_path + "y_train.csv", header=None)
X_test_55attrib = pd.read_csv(data_path + "X_test_55attrib.csv", header=None)
y_test = pd.read_csv(data_path + "y_test.csv", header=None)


pipelines_params = [
    ('Logistic Regression', make_pipeline(StandardScaler(), LogisticRegression()), {
            # 'standardscaler__with_mean': [True, False],
            # 'standardscaler__with_std': [True, False],
            'logisticregression__C': loguniform(1e-3, 1e3),
        }),
    ('K-Nearest Neighbors', make_pipeline(StandardScaler(), KNeighborsClassifier()), {
            'kneighborsclassifier__n_neighbors': range(0, 100),
        }),
    ('Multi-layer Perceptron', make_pipeline(StandardScaler(), MLPClassifier()), {
            'mlpclassifier__hidden_layer_sizes': [(50,), (100,), (200,), (50,50), (100,100), (200,200), (50,50,50), (100,100,100), (200,200,200), (50,50,50,50)],
            'mlpclassifier__activation': ['relu', 'tanh', 'logistic'],
            'mlpclassifier__learning_rate': ['constant', 'invscaling', 'adaptive'],
        }),
    ('Random Forest', make_pipeline(StandardScaler(), RandomForestClassifier()), {
            'randomforestclassifier__n_estimators': range(1, 500),
            'randomforestclassifier__max_depth': [4, 16, 64, 256, None],
        }),
    ('Support Vector Machine', make_pipeline(StandardScaler(), SVC()), {
            'svc__C': loguniform(1e-3, 1e3),
            'svc__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        }),
    ('Adaptive Boosting', make_pipeline(StandardScaler(), AdaBoostClassifier()), {
            'adaboostclassifier__base_estimator': [None, KNeighborsClassifier(), LogisticRegression()],
            'adaboostclassifier__n_estimators': range(1, 500),
        }),
    ('Bagging', make_pipeline(StandardScaler(), BaggingClassifier()), {
            'baggingclassifier__base_estimator': [None, KNeighborsClassifier(), LogisticRegression()],
            'baggingclassifier__n_estimators': range(1, 500),
            'baggingclassifier__max_samples': scipy.stats.uniform(),
            'baggingclassifier__max_features': scipy.stats.uniform(),
        }),
]

search_cv_s = [RandomizedSearchCV(item[1], item[2], scoring=['balanced_accuracy', 'f1_weighted'], refit='f1_weighted', cv=5, verbose=1, n_jobs=-1, n_iter=100) for item in pipelines_params]
for pipeline_param, search_cv in zip(pipelines_params, search_cv_s):
    loop_start_time = timer()
    name = pipeline_param[0]
    name_underscore = name.replace(' ', '_')
    print(f'Fitting {name}...')
    search_cv.fit(X_train_55attrib, y_train.values.ravel())
    joblib.dump(search_cv.best_estimator_, results_path + f'best_model_{name_underscore}.xz', compress=True)
    df = pd.DataFrame(search_cv.cv_results_).sort_values(by='rank_test_f1_weighted')
    df.to_csv(results_path + f'training_result_{name_underscore}.csv', index=False)
    y_train_55attrib_pred = search_cv.predict(X_train_55attrib)
    y_test_55attrib_pred = search_cv.predict(X_test_55attrib)
    with open(results_path + f'classification_report_{name_underscore}.md', 'w') as report:
        report.write(f'# Classification Report for {name}\n\n')
        report.write('## Parameter Search Results\n\n')
        report.write(df[['rank_test_f1_weighted', 'mean_test_f1_weighted', 'mean_test_balanced_accuracy', 'mean_fit_time', 'params']].to_markdown(index=False))
        report.write('\n\n')
        report.write('## Best Classifier Found\n\n')
        report.write('```\n')
        report.write(str(search_cv.best_estimator_) + '\n')
        report.write(str(search_cv.best_params_) + '\n')
        report.write('```\n')
        report.write('\n')
        report.write('### Training report\n\n')
        report.write('```\n')
        report.write(classification_report(y_train, y_train_55attrib_pred))
        report.write('```\n')
        report.write('\n')
        report.write('### Testing report\n\n')
        report.write('```\n')
        report.write(classification_report(y_test, y_test_55attrib_pred))
        report.write('```\n')
        report.write('### Confusion matrix\n\n')
        plot_confusion_matrix(search_cv, X_test_55attrib, y_test)
        image_file_name = f'plot_confusion_matrix_{name_underscore}.png'
        plt.savefig(results_path + image_file_name)
        report.write(f'![{image_file_name}](../{results_path + image_file_name})\n\n')

    print(f'Elasped time: {timer() - loop_start_time}')

print(f'Total elasped time: {timer() - start_time}')
