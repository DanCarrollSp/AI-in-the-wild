#Email dataset
from ucimlrepo import fetch_ucirepo
#Plotting data
import pandas as pd
import matplotlib.pyplot as plt
#Used to divide the data into training and testing subsets
from sklearn.model_selection import train_test_split
#Neighbours for KNN model
from sklearn.neighbors import KNeighborsClassifier
#Accuracy_score
from sklearn.metrics import accuracy_score



#Fetchs the Spambase dataset with ID 94 from the UCIML repository
spambase = fetch_ucirepo(id=94)
#Extracts the features 'X' and target labels 'y' from the dataset
X = spambase.data.features  #Features = input variables like word frequencies, email metadata, etc.....
y = spambase.data.targets   #Target labels = 0 for not spam and 1 for spam



#Converts the features and target labels into pandas dataframes
X = pd.DataFrame(X)
y = pd.DataFrame(y)
#Creates a bar chart to visualize the amount of spam vs non spam detected
plt.figure(figsize=(5,5))
y.value_counts().plot(kind='bar')
plt.title("Spam vs Non-Spam Emails")
plt.xlabel("Is it spam?")
plt.ylabel("Amount")
plt.xticks([0, 1], ['Not Spam', 'Spam'], rotation=0)
plt.show()



#Splits the email dataset into training and testing sets (80% training - 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)
#Initializes the KNN model with a specific number of neighbors
knnModel = KNeighborsClassifier(n_neighbors=5)
#Train the model on the training data
knnModel.fit(X_train, y_train.values.ravel())



#Makes predictions using the trained model on the test set
yPred = knnModel.predict(X_test)
#Accuracy output
print("\nAccuracy of the Test Set:")
print(accuracy_score(y_test, yPred))