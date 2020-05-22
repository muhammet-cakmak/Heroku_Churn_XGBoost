#!/usr/bin/env python
# coding: utf-8

# In[87]:


import pandas as pd
import numpy as np
import pickle
import sklearn

import lightgbm as lgb
from sklearn import metrics
from sklearn import metrics


# In[88]:


df = pd.read_csv("Churn_Modelling.csv")

df_x = df.iloc[:, 3:13]
df_y = df.iloc[:, 13]


# In[89]:


def clean_data(df):

    le = sklearn.preprocessing.LabelEncoder()
    df.Gender = le.fit_transform(df.Gender)
    df = pd.get_dummies(data = df, columns=["Geography"], drop_first = False)
    df = df.sort_index(axis=1)
    return df


# In[90]:


df_x = clean_data(df_x)


# In[91]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, test_size = 0.2, random_state = 0)
pickle.dump(df_x.columns, open("columns.pkl", 'wb'))


# In[92]:


"""
scaler = sklearn.preprocessing.MinMaxScaler().fit(X_train)
X_train = scaler.transform(X_train)

# transform testing dataabs
X_test = scaler.transform(X_test)

pickle.dump(scaler, open("std_scaler.pkl", 'wb'))
print(X_test)
print(X_train.shape[1])
"""


# In[93]:


import xgboost as xgb
model = xgb.XGBClassifier(max_depth=50, min_child_weight=1,  n_estimators=200,learning_rate=0.16)
model.fit(X_train, y_train)


# In[94]:


#from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,roc_curve,auc
predictions = model.predict_proba(X_test)
#print ("\naccuracy_score :",accuracy_score(y_test,predictions))


# In[95]:


predictions


# In[96]:


# save the model so created above into a picle.
pickle.dump(model, open('model.pkl', 'wb')) 


# In[ ]:



