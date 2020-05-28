import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle

data = pd.read_csv('symptoms.csv')

X = data.iloc[:, :-1].values
y = data.iloc[:, 4].values

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

scaler = StandardScaler()
scaler.fit(X)

#print(X_train)

#X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)
X = scaler.transform(X)
d = scaler.transform([[4,9,2,4]])
#print(X_train)

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X, y)

with open("knnmodel01.pkl", "wb") as f:
        pickle.dump(classifier, f)

y_pred = classifier.predict(d)

print("Score : ",classifier.score(d,[0]))
print("proba : ",classifier.predict_proba(d)[0][1])
print("Prediction : ",y_pred)
print("Test data: ",y)
