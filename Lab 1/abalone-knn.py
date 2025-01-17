#Imports pandas
import pandas as pd

#Gets the abalone data and reads it as a csv
url = ("https://archive.ics.uci.edu/ml/machine-learning-databases""/abalone/abalone.data")
abalone = pd.read_csv(url, header=None)

#Column the data
abalone.columns = ["Sex", "Length", "Diameter", "Height", "Whole weight", "Shucked weight", "Viscera weight", "Shell weight", "Rings"]
#Drop the Sex column as its not needed (drops the entire column, "Sex" header and all data under it)
abalone = abalone.drop("Sex", axis=1)

print(abalone.head())





import matplotlib.pyplot as plt
abalone["Rings"].hist(bins=15)
plt.show()