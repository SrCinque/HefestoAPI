from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd

import tensorflow as tf




# Load dataset.
dftrain = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRhuroKnCWjAHU_BxSIi8Fca68wejgeNtv73LwMCocROjDW8kLC_E4gFQjrPvlqs08ylnouLU-tbSec/pub?output=csv') # training data
y_train = dftrain.pop('seguro')

#o dataset vai mudar quando eu fizer a rota de treinamento 


CATEGORICAL_COLUMNS = ['latitude', 'longitude','nav_user','hour_login','sys_user','IP_user']
NUMERIC_COLUMNS = []

feature_columns = []
for feature_name in CATEGORICAL_COLUMNS:
  vocabulary = dftrain[feature_name].unique()  # gets a list of all unique values from given feature column
  feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

for feature_name in NUMERIC_COLUMNS:
  feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
  def input_function():  # inner function, this will be returned
    ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))  # create tf.data.Dataset object with data and its label
    if shuffle:
      ds = ds.shuffle(1000)  # randomize order of data
    ds = ds.batch(batch_size).repeat(num_epochs)  # split dataset into batches of 32 and repeat process for number of epochs
    return ds  # return a batch of the dataset
  return input_function  # return a function object for use




train_input_fn = make_input_fn(dftrain, y_train)  # here we will call the input_function that was returned to us to get a dataset object we can feed to the model


linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)


linear_est.train(train_input_fn)



   

def rest_trainTest(latitude,longitude,nav_user,hour_login,sys_user,user_ip):
    data = {'latitude': latitude, 'longitude':longitude,'nav_user': nav_user,'hour_login': hour_login,'sys_user': sys_user,'IP_user': user_ip}
    dfeval = pd.DataFrame(data, index=[0])
    y_eval = pd.DataFrame({'seguro':'0'}, index=[0])
    eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)

    result = list(linear_est.predict(eval_input_fn))
    resultado = result[0]['probabilities']

    resposta = ''
    if(resultado[0] < 0.50):
       resposta = 'Não é seguro'
    else:
       resposta = 'Seguro'
    return resposta

      



