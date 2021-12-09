# -*- coding: utf-8 -*-
"""Proyek Satu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZJi8WWj_sIIv3OErrDP3zjEjD-Tmo0MZ

##Data Loading
"""

import os
os.environ['KAGGLE_USERNAME'] = "ichsannuriman"
os.environ['KAGGLE_KEY'] = "e20dd538318e3a23d0bbfdf1e29fbdb8"

!kaggle datasets download -d teertha/ushealthinsurancedataset

!unzip -q ushealthinsurancedataset.zip -d .

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns

"""#Data Understanding

##Deskripsi Variabel
"""

df = pd.read_csv('insurance.csv')
df

df.info()

df.describe()

df.describe(include=object)

df.isnull().sum()

"""##Univariate Analysis"""

categorical = ['sex','smoker', 'region']

numerical = ['age','children','bmi','charges']

feature = categorical[0]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df1 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df1)
count.plot(kind='bar', title=feature);

feature = categorical[1]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df1 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df1)
count.plot(kind='bar', title=feature);

feature = categorical[2]
count = df[feature].value_counts()
percent = 100*df[feature].value_counts(normalize=True)
df1 = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df1)
count.plot(kind='bar', title=feature);

df.hist(bins=50, figsize=(20,15))
plt.show()

"""##Multivariate Analysis"""

cat_features = df[categorical].columns.to_list()
 
for col in cat_features:
  sns.catplot(x=col, y="charges", kind="bar", dodge=False, height = 4, aspect = 3,  data=df, palette="Set3")
  plt.title("Relasi 'charges' terhadap - {}".format(col))

sns.pairplot(df, diag_kind = 'kde')

plt.figure(figsize=(10, 8))
correlation_matrix = df[numerical].corr().round(2)
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

"""#Data Preparation"""

from sklearn.preprocessing import  OneHotEncoder
df = pd.concat([df, pd.get_dummies(df['sex'], prefix='sex', drop_first=True)],axis=1)
df = pd.concat([df, pd.get_dummies(df['smoker'], prefix='smoker', drop_first=True)],axis=1)
df = pd.concat([df, pd.get_dummies(df['region'], prefix='region', drop_first=True)],axis=1)
df.drop(['sex','smoker','region'], axis=1, inplace=True)
df

from sklearn.model_selection import train_test_split
 
X = df.drop(["charges"],axis =1)
y = df["charges"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 123)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

from sklearn.preprocessing import StandardScaler
 
numerical_features = ['age','children','bmi']
scaler = StandardScaler()
scaler.fit(X_train[numerical_features])
X_train[numerical_features] = scaler.transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

X_train[numerical_features].describe().round(4)

"""#Model Development"""

models = pd.DataFrame(index=['train_mse', 'test_mse'], 
                      columns=['KNN', 'RandomForest', 'Boosting'])

"""##K-Nearest Neighbor"""

from sklearn.neighbors import KNeighborsRegressor
 
knn = KNeighborsRegressor(n_neighbors=10)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_train)

"""##Random Forest"""

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

RF = RandomForestRegressor(n_estimators=50, max_depth=16, random_state=55, n_jobs=-1)
RF.fit(X_train, y_train)
 
models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

"""##Boosting Algorithm"""

from sklearn.ensemble import AdaBoostRegressor
 
boosting = AdaBoostRegressor(n_estimators=50, learning_rate=0.05, random_state=55)                             
boosting.fit(X_train, y_train)
models.loc['train_mse','Boosting'] = mean_squared_error(y_pred=boosting.predict(X_train), y_true=y_train)

"""#Evaluasi Model"""

X_test.loc[:, numerical_features] = scaler.transform(X_test[numerical_features])

mse = pd.DataFrame(columns=['train', 'test'], index=['KNN','RF','Boosting'])
model_dict = {'KNN': knn, 'RF': RF, 'Boosting': boosting}
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e3 
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e3

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

prediksi = X_test.iloc[:1].copy()
pred_dict = {'y_true':y_test[:1]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)
 
pd.DataFrame(pred_dict)