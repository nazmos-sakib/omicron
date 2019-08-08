import io

#import all necessary liberty

import tensorflow as tf
import numpy as np

import pandas as pd


from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import Dropout
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras import backend as k 
from keras.models import load_model


import csv

#spliting dataset into traning set and test set
from sklearn.model_selection import train_test_split
#missing value handle
from sklearn.preprocessing import Imputer
#To shuffle the data set
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
#from sklearn.utils import shuffle

import itertools

from scipy.stats import zscore

import os

#[32, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

'''

session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)

from keras import backend as K

sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)
'''


def get_model():
	global model
	#model = load_model("heart_attack_risk_prediction_fold_no_8_with_cross_validation.h5")
	model = load_model("heart_attack_risk_prediction_percent_split.h5",compile= False)
	model._make_predict_function()
	print("* Model loaded")
	return model


def NN(data):
    data = np.expand_dims(data, axis=0)
    model = get_model()
    predections = model.predict_classes(data,verbose=0)
    return predections[0]

def NN1(data,model):
    data = np.expand_dims(data, axis=0)
    #model = get_model()
    predections = model.predict_classes(data,verbose=0)
    return predections[0]

def NN2(data):
    data = np.expand_dims(data, axis=0)
    #global model
    predections = model.predict_classes(data,verbose=0)
    return predections[0]
