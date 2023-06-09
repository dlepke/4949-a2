import pandas as pd
from matplotlib import pyplot as plt
import pickle
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_selection import f_classif

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

df = pd.read_csv('heart.csv', skiprows=1, names=(
    'age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg',
    'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall', 'output'
))

df['sex'].replace([0, 1], ['F', 'M'], inplace=True)
df['cp'].replace([0, 1, 2, 3], ['typical_angina', 'atypical_angina', 'non-anginal_pain', 'asymptomatic'], inplace=True)
df['restecg'].replace([0, 1, 2], ['normal', 'stt_abnormal', 'hypertrophy'], inplace=True)
df['thall'].replace([0, 1, 2, 3], ['NULL', 'fixed', 'normal', 'reversible'], inplace=True)
df['slp'].replace([0, 1, 2], ['down', 'flat', 'up'], inplace=True)
df['exng'].replace([0, 1], ['no', 'yes'], inplace=True)

X = df.copy()
del X['output']

del X['caa']
del X['oldpeak']
del X['exng']
del X['thalachh']

X = pd.get_dummies(X)

del X['thall_NULL']

columns = X.columns

y = df[['output']]

imputer = KNNImputer(n_neighbors=5)
X = imputer.fit_transform(X)

X = pd.DataFrame(X, columns=columns)

heart_disease = df[df['output'] == 0]
no_disease = df[df['output'] == 1]

plt.figure(figsize=(22, 15))

for i in range(len(df.columns) - 1):
    col = df.columns[i]
    plt.subplot(4, 4, i + 1)
    plt.hist([heart_disease[col], no_disease[col]], rwidth=0.8)
    plt.legend(['Heart disease', 'No heart disease'])
    plt.title(col)

plt.show()

ffs = f_classif(X, y)

features = pd.DataFrame()
for i in range(len(X.columns)):
    features = features.append({"feature": X.columns[i], "ffs": ffs[0][i]}, ignore_index=True)

features = features.sort_values(by=['ffs'])
print(features)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(fit_intercept=True, solver='liblinear', random_state=0)

model.fit(X_train, y_train)

with open('model.pkl', 'wb') as files:
    pickle.dump(model, files)

with open('model.pkl', 'rb') as f:
    loaded = pickle.load(f)

predictions = model.predict(X_test)

cm = pd.crosstab(y_test['output'], predictions, rownames=['Actual'], colnames=['Predicted'])
print(cm)
print(classification_report(y_test, predictions))
