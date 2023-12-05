from preprocessing import preprocess
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import pickle
import numpy as np
import random
import matplotlib.pyplot as plt

data = pd.read_csv("./Dataset/train_snli.csv",sep = "\t",header=0,names = ['Phrase','Suspicious','Class'])
# Data provided by https://www.kaggle.com/code/mpwolke/plagiarism-mit-detection
data = data.dropna()[:1500]

#document -> tf-idf vectors
X,y,vocab = preprocess(data)

# Compare each suspicious document to every other document in database
X = [[X[0][x],X[0][d],y[x]] if d==x else [X[0][x],X[0][d],0] for d in range(len(X[1])) for x in range(len(X[0]))]
y = [X[x][-1] for x in range(len(X))]
X = [[np.array(X[x][:-1]).astype(np.float32) for x in range(len(X))]]

X=np.array(X)[0]
X = X.reshape(len(X),-1)

y_1 = np.array(y)[np.array(y)==1]
X_1 = X[np.array(y)==1]
y_0 = random.sample(list(enumerate(np.array(y)[np.array(y)==0])),sum(np.array(y)==1))
X_0 = X[np.array(y_0)[:,0]]

y_ = np.concatenate((y_1,np.array(y_0)[:,1]))
X_ = np.concatenate((X_1,X_0))

shuf = list(range(len(y_)))

random.shuffle(shuf)
X = X_[shuf]
y = y_[shuf]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define model
tree_model = DecisionTreeClassifier()

# Fit model to data
tree_model.fit(X_train, y_train) #reached an accuracy of 80.62%

# Generate predictions
y_pred = tree_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy of test pre-pruning:", accuracy)
print("Classification Report pre-pruning:")
print(classification_rep)

# Prune tree to reduce overfitting
path = tree_model.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities

# Plot the pruning path
fig, ax = plt.subplots()
ax.plot(ccp_alphas[:-1], impurities[:-1], marker='o', drawstyle="steps-post")
ax.set_xlabel("effective alpha")
ax.set_ylabel("total impurity of leaves")
ax.set_title("Total Impurity vs Effective Alpha for training set")
plt.savefig('./plot/pruning_path.png')

# Find the optimal value for ccp_alpha
optimal_ccp_alpha = ccp_alphas[np.argmin(impurities)]

# Set the ccp_alpha parameter
tree_model.ccp_alpha = (optimal_ccp_alpha)

# Re-fit the tree
tree_model.fit(X_train, y_train)

# Re-test the tree
y_pred_train = tree_model.predict(X_train)
accuracy = accuracy_score(y_train, y_pred_train)
classification_rep = classification_report(y_train, y_pred_train)

print("Accuracy on train:", accuracy)
print("Classification Report:")
print(classification_rep)

y_pred = tree_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy on test:", accuracy)
print("Classification Report:")
print(classification_rep)

pickle.dump(tree_model, open("decision_tree.sav", 'wb'))

