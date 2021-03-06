#!/usr/bin/env python
# coding: utf-8


from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
import json
import pickle


import sklearn  
from sklearn import preprocessing



app = Flask(__name__)


main_cols = pickle.load(open("columns.pkl", 'rb'))





def clean_data(df_x):
    le = preprocessing.LabelEncoder()
    df_x.Gender = le.fit_transform(df_x.Gender)
    df_x = pd.get_dummies(data = df_x,  columns=["Geography"], drop_first = False)
    return df_x



"""
def standardize_data(dta):
                        
    scaler = pickle.load(open("std_scaler.pkl", 'rb'))
    X_transformed = scaler.transform(dta)
    return X_transformed
"""




@app.route('/')
def home():
    return render_template('index.html')




@app.route('/predict', methods=['POST'])


def predict():
    
    int_features = [x for x in request.form.values()]
    form_data = np.array(int_features)
    
    
    
    #form_data = request.form.to_dict()
    
    df_input = pd.DataFrame.from_records(form_data)
    #df_input = df_input.drop(['submitBtn'], axis=1)
    df_input = pd.DataFrame(df_input)
    
    sample_df = pd.DataFrame(columns = main_cols)
    clean_df = clean_data(df_input)
    main_df = sample_df.append(clean_df,sort=False)
    main_df = main_df.fillna(0)
   
    std_df = main_df.copy()

    
    std_df = std_df.astype(float)

    
    clf = pickle.load(open('model.pkl', 'rb'))
    pred = clf.predict(std_df)
    
    #x = round(pred*100, 2)
   
    x = pred
    if x == 1:
        
        return render_template('index.html', predicted_value="The customer's churn status is {}.  It can be risky to give  the credit to the customer.".format(x))
    else:
        return render_template('index.html', predicted_value="The customer's churn status is {}.  It may not be risky to give  the credit to the customer".format(x))

    
@app.route('/api', methods=['POST', 'GET'])
def api_response():
    from flask import jsonify
    if request.method == 'POST':
        return jsonify(**request.json)
    

    


if __name__ == '__main__':
    app.run(debug=TRUE)







