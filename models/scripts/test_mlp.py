#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 17:03:40

import numpy as np
from keras.models import model_from_json
from keras.optimizers import RMSprop
import sPickle
from tools import number2vector

input = open('../Pre/featdict.pkl', 'rb')
featnamearray, feattypedict, featdict = sPickle.load(input)
input.close()


input = open('../Pre/X.pkl', 'rb')
X_mean = sPickle.load(input)
X_std = sPickle.load(input)
X_train_N = sPickle.load(input)
X_train_V = sPickle.load(input)
X_test_N = sPickle.load(input)
X_test_V = sPickle.load(input)
input.close()

input = open('../Pre/Y.pkl', 'rb')
Y_mean = sPickle.load(input)
Y_std = sPickle.load(input)
Y_train = sPickle.load(input)
Y_test = sPickle.load(input)
input.close()

model = model_from_json(open("mlp_architecture.json").read())
model.load_weights('mlp_weights.h5')

model.compile(loss='mse', optimizer=RMSprop())

X_test_V = number2vector(featnamearray, feattypedict, featdict, X_test_V)
X_test = np.hstack((X_test_V, X_test_N))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score)

Y_predict = model.predict(X_test, verbose=0)
Y_predict = (Y_predict * Y_std) + Y_mean
Y_predict = Y_predict.astype(np.float32)
Y_predict.tofile("Y_predict")
