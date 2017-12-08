import pandas as pd
data = pd.read_csv('regression_dataset.csv')

X=data.loc[:, data.columns != 'y']
Y=data['y']


from sklearn.utils import shuffle
data= shuffle(data).reset_index(drop=True)
X=data.loc[:, data.columns != 'y']
Y=data['y']
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=100)
print ('Number of samples in training data:',len(x_train))
print ('Number of samples in validation data:',len(x_test))
#train logistic regression
from sklearn import linear_model
logreg_model = linear_model.LogisticRegression()
print ('Training a logistic Regression Model..')
logreg_model.fit(x_train, y_train)
training_accuracy= round(logreg_model.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy=round(logreg_model.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)
parameters = logreg_model.get_params()
print('parameters of this model:\n',parameters)
coefficients = logreg_model.coef_
print('coefficients of this model:\n',coefficients)
interceptions = logreg_model.intercept_
print('interceptions of this model:\n',interceptions)

from sklearn import svm
svc = svm.SVC()
print ('Training a SVM Model..')
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=100)
svc.fit(x_train, y_train)
train_accuracy= round(svc.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy= round(svc.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)

from sklearn import linear_model
perceptron_model=linear_model.Perceptron()
print ('Training a perceptron Model..')
perceptron_model.fit(x_train, y_train)
training_accuracy=round(perceptron_model.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy=round(perceptron_model.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(x_train, y_train)
print ('Training a KMeans Model..')
training_accuracy= round(knn.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy= round(knn.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)

import xgboost as xgb
xgb_model = xgb.XGBClassifier(n_estimators=1000)
print ('Training a xgboost Model..')
xgb_model.fit(x_train, y_train, eval_metric='mlogloss')
training_accuracy=round(xgb_model.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy=round(xgb_model.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)

from sklearn.ensemble import RandomForestClassifier
randomforest_model = RandomForestClassifier(n_estimators=1000)
print ('Training a random forest Model..')
randomforest_model.fit(x_train, y_train)
training_accuracy=round(randomforest_model.score(x_train, y_train) * 100, 2)
print('Accuraacy of the model on training data: ',training_accuracy)
test_accuracy=round(randomforest_model.score(x_test, y_test) * 100, 2)
print('Accuraacy of the model on test data: ',test_accuracy)
