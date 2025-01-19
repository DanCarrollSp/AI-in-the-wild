#Imports pandas, will install pandas if it is not already installed
try:
    import pandas as pd
except ImportError:
    import os
    os.system('pip install pandas')
    import pandas as pd


###
#Gets the abalone data and reads it as a csv
url = ("https://archive.ics.uci.edu/ml/machine-learning-databases""/abalone/abalone.data")
abalone = pd.read_csv(url, header=None)

#Column the data
abalone.columns = ["Sex", "Length", "Diameter", "Height", "Whole weight", "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
#Drop the Sex column as its not needed (drops the entire column, "Sex" header and all data under it)
abalone = abalone.drop("Sex", axis=1)

print(abalone.head())


###
import matplotlib.pyplot as plt
abalone["Rings"].hist(bins=15)
plt.show()


###
correlation_matrix = abalone.corr()
correlation_matrix["Rings"]


###
# Tries to import sklearn, and installs it if it is not available
try:
    from sklearn.model_selection import train_test_split
except ImportError:
    import os
    os.system('pip install scikit-learn')
    from sklearn.model_selection import train_test_split



###
X = abalone.drop("Rings", axis=1)
X = X.values
y = abalone["Rings"]
y = y.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)



from sklearn.neighbors import KNeighborsRegressor
knn_model = KNeighborsRegressor(n_neighbors=3)


knn_model.fit(X_train, y_train)



###
from sklearn.metrics import mean_squared_error
from math import sqrt

train_preds = knn_model.predict(X_train)
mse = mean_squared_error(y_train, train_preds)
rmse = sqrt(mse)
rmse



###
test_preds = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
rmse



###
# Tries to import seaborn, and installs it if it is not available
try:
    import seaborn as sns
except ImportError:
    import os
    os.system('pip install seaborn')
    import seaborn as sns



###
cmap = sns.cubehelix_palette(as_cmap=True)
f, ax = plt.subplots()
points = ax.scatter(X_test[:, 0], X_test[:, 1], c=test_preds, s=50, cmap=cmap)
f.colorbar(points)
plt.show()



###
from sklearn.model_selection import GridSearchCV
parameters = {"n_neighbors": range(1, 50)}
gridsearch = GridSearchCV(KNeighborsRegressor(), parameters)
gridsearch.fit(X_train, y_train)



###
gridsearch.best_params_



###
train_preds_grid = gridsearch.predict(X_train)
train_mse = mean_squared_error(y_train, train_preds_grid)
train_rmse = sqrt(train_mse)
test_preds_grid = gridsearch.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)

print(train_rmse)
print(test_rmse)



###
parameters = {"n_neighbors": range(1, 50),"weights": ["uniform", "distance"],}
gridsearch = GridSearchCV(KNeighborsRegressor(), parameters)
gridsearch.fit(X_train, y_train)
GridSearchCV(estimator=KNeighborsRegressor(),
             param_grid={'n_neighbors': range(1, 50),
                         'weights': ['uniform', 'distance']})
gridsearch.best_params_
{'n_neighbors': 25, 'weights': 'distance'}
test_preds_grid = gridsearch.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
test_rmse



###
best_k = gridsearch.best_params_["n_neighbors"]
best_weights = gridsearch.best_params_["weights"]
bagged_knn = KNeighborsRegressor(n_neighbors=best_k, weights=best_weights)




from sklearn.ensemble import BaggingRegressor
bagging_model = BaggingRegressor(bagged_knn, n_estimators=100)

bagging_model.fit( X_train, y_train)

test_preds_grid = bagging_model.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
test_rmse