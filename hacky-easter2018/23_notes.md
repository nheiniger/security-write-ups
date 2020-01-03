23 - Rapbid Learning
====================
> The SERTC (super exciting rabbit travel company) wants to use the latest technology.
> 
> They currently employ an experienced guide, which is classifying the visitors into Goodtails and Luckyspoons. For the trained eye of the guide, this is easy. But how do you get a machine to do it (which would be cheaper)?
> 
> Go and help them implement a learning algorithm! Their platform is available here:
> 
> http://whale.hacking-lab.com:2222 
> 
> Since quality is the main concern of SERTC, they expect an accuracy of at least 99%.

This is a "simple" machine learning classification problem. It can be solved in sevral ways. I chose python, as usual, and found an article explaining how to perform simple classification in python <https://machinelearningmastery.com/machine-learning-in-python-step-by-step/>. This was very useful since my ML skills are more than rusty.

We start by gathering the training data from the provided URL and saving it as CSV:
```bash
for i in `seq 1 500`; do curl -s http://whale.hacking-lab.com:2222/train | jq -r '[.n4m3, .g3nd3r, .ag3, .c0l0r, .w31ght, .l3ngth, .sp00n, .t41l, .g00d] | @csv' >> 23_train-set.csv; done;
```

Then, my script is broken down and explained below, first imports, basic stuff:
```python
#!/usr/bin/python

# shamelessly adapted from https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

import numpy
import pandas
from pandas.plotting import scatter_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import requests
```

Then load the train dataset and apply a mapping to have only integer in our data, feed the data to train the classifier:
```python
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load train dataset
dataframe = pandas.read_csv("23_train-set.csv", header=None, names=['name', 'gender', 'age', 'color', 'weight', 'length', 'spoon', 'tail', 'good'])
mapping = {'gender':{'male':0, 'female':1}, 'color':{'red':0, 'black':1, 'brown':2, 'blue':3, 'white':4, 'purple':5, 'green':6, 'grey':7}}
new_dataframe = dataframe.replace(mapping)

dataset = new_dataframe.values
X = dataset[:,1:8].astype(int)
Y = dataset[:,8].astype(bool)

# train the classifier
cart = DecisionTreeClassifier()
cart.fit(X, Y)
```

Once we have our algorithm trained we can get the test record set from the "gate" URL and transform it in a format that our algorithm will understand:
```python
# load gate dataset
url = 'http://whale.hacking-lab.com:2222/gate'
r1 = requests.get(url)
session = r1.cookies['session_id']
print(session)

# parse JSON to get an array
data_array = r1.json()['data']
gate_array = []
for d in data_array:
    new = []
    if d[1] == 'male':
        new.append(1)
    else:
        new.append(0)
    new.append(d[2])
    if d[3] == 'red':
        new.append(0)
    elif d[3] == 'black':
        new.append(1)
    elif d[3] == 'brown':
        new.append(2)
    elif d[3] == 'blue':
        new.append(3)
    elif d[3] == 'white':
        new.append(4)
    elif d[3] == 'purple':
        new.append(5)
    elif d[3] == 'green':
        new.append(6)
    elif d[3] == 'grey':
        new.append(7)
    new.append(d[4])
    new.append(d[5])
    new.append(d[6])
    new.append(d[7])
    gate_array.append(new)
```

Now apply the algorithm on the data we have to make the predictions:
```python
# make predictions
predictions = cart.predict(gate_array)
json_predictions = []
for p in predictions:
    if p:
        json_predictions.append(1)
    else:
        json_predictions.append(0)
```

Finally submitthe predictions to the website and get the reward:
```python
# submit prediction
url = 'http://whale.hacking-lab.com:2222/predict'
r2 = requests.post(url, json=json_predictions, cookies={'session_id': session})
print(r2.text)

# get reward
url = 'http://whale.hacking-lab.com:2222/reward'
r3 = requests.get(url, cookies={'session_id': session})
print(r3.content)
```

This gets us the egg:
![](./23_egg.png)

As a bonus, here is the code that was used to compare several algorithms and that helped choosing the most adapted one:
```python
scoring = 'accuracy'

# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
```

And the result was:
```
LR: 0.981250 (0.028641)
LDA: 0.975000 (0.041458)
KNN: 0.937500 (0.073951)
CART: 1.000000 (0.000000)
NB: 1.000000 (0.000000)
SVM: 0.968750 (0.031250)
```
