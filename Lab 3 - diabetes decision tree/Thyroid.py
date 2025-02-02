import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics#For accuracy calculations
from sklearn.preprocessing import LabelEncoder#Converts category variables into number format
from sklearn import tree


#Loads the dataset into pandas
thyroidData = pd.read_csv("Thyroid_Diff.csv")



#Converts category data into numeric using Label Encoders
labelEncoders = {}#Stores label encoders for each category
for column in thyroidData.columns:
    if thyroidData[column].dtype == 'object':#Checks if column contains a category value
        labelEncoders[column] = LabelEncoder()#Initializes LabelEncoder
        thyroidData[column] = labelEncoders[column].fit_transform(thyroidData[column])#Converts to numerical values


#Defines features and target variable
featureCols = [col for col in thyroidData.columns if col != 'Recurred']#Dont include target column
X = thyroidData[featureCols]#Features (independent variables)
y = thyroidData['Recurred']  #Target variable (dependent variable)


#Splits the data into training set and test set (70-30)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
#Creates the decision tree classifier object with entropy (Information Gain)
clf = DecisionTreeClassifier(criterion='entropy')
#Trains the decision tree classifier using the training data
clf = clf.fit(X_train, y_train)
#Predicts the response for testing data
y_pred = clf.predict(X_test)


#Calculates and prints the accuracy
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
#Plots the decision tree
plt.figure(figsize=(15,8))
tree.plot_tree(clf, filled=True, feature_names=featureCols, class_names=['No', 'Yes'])
plt.title("Decision tree trained on thyroid dataset")
plt.show()