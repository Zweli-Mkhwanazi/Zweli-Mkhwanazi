import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

dataset = pd.read_csv(r"C:\Users\Zwelibanzi Mkhwanazi\Documents\PROJECT B - APP\Website\Clean_Project_A_data.csv") # importing cleaned data as csv

# performing the train test split on the dataset
y = dataset['Loan_Status']
X = dataset.drop('Loan_Status', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# creating the model
algorithm = LogisticRegression()

# performing feature scaling
sc = StandardScaler()
new_Xtrain = sc.fit_transform(X_train)
new_Xtest = sc.fit_transform(X_test)

# fitting the model with the training data
algorithm.fit(new_Xtrain, y_train)

# saving the model onto the disk
pickle.dump(algorithm, open('model.pkl', 'wb'))


