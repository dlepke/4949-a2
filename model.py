import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
import pickle
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

df = pd.read_csv('chocolate_bars.csv')

X = df[['cocoa_percent', 'num_ingredients', 'ingredients']]


def create_dummy_var(X, column_name):
    imputed_columns = {
        'B': [],
        'C': [],
        'S': [],
        'S*': [],
        'Sa': [],
        'V': [],
        'L': [],
    }
    
    possible_values = ['B', 'C', 'S', 'S*', 'Sa', 'V', 'L']

    for i in range(len(X)):
        row_value = X.loc[i][column_name]
        
        for poss in possible_values:
            # ensure S isn't entered when S* and Sa appear
            if poss == 'S':
                check = 'S,'
            else:
                check = poss
            if pd.isna(row_value):
                imputed_columns[poss].append(0)
            else:
                if check in row_value:
                    imputed_columns[poss].append(1)
                else:
                    imputed_columns[poss].append(0)
        
    for poss in possible_values:
        X[poss] = imputed_columns[poss]
        
    return X


create_dummy_var(X, 'ingredients')

del X['ingredients']
del X['C']

y = df[['rating']]

# X = pd.get_dummies(X)
columns = X.columns

imputer = KNNImputer(n_neighbors=5)
X = imputer.fit_transform(X)

X = pd.DataFrame(X, columns=columns)

X = sm.add_constant(X)

print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = sm.OLS(y_train, X_train).fit()
#
# with open('model.pkl', 'wb') as files:
#     pickle.dump(model, files)
#
# with open('model.pkl', 'rb') as f:
#     loaded = pickle.load(f)

predictions = model.predict(X_test)

print(predictions.head())

print(model.summary())

print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))
