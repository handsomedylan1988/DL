from __future__ import print_function
import numpy as np
import sPickle
from tools import number2vector
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
import sys
sys.path.append("../Pre/scripts/")
from config import *


batch_size = 256
nb_epoch = 50

# load the dictionary
input = open('../Pre/featdict.pkl', 'rb')
featnamearray = sPickle.load(input)
feattypedict = sPickle.load(input)
featdict = sPickle.load(input)
input.close()

# load the input features
input = open('../Pre/X.pkl', 'rb')
X_mean = sPickle.load(input)
X_std = sPickle.load(input)
X_train_N = sPickle.load(input)
X_train_V = sPickle.load(input)
X_test_N = sPickle.load(input)
X_test_V = sPickle.load(input)
input.close()


# load the output acoustic features
input = open('../Pre/Y.pkl', 'rb')
Y_mean = sPickle.load(input)
Y_std = sPickle.load(input)
Y_train = sPickle.load(input)
Y_test = sPickle.load(input)
input.close()

assert(len(X_train_V) == len(Y_train))
assert(len(X_test_V) == len(Y_test))

# construct model
model = Sequential()
model.add(Dense(512, input_shape=(INPUT_DIM,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(OUTPUT_DIM))
model.add(Activation('linear'))

model.summary()

model.compile(loss='mse',
              optimizer=RMSprop(),
              metrics=['accuracy'])

X_test_V = number2vector(featnamearray, feattypedict, featdict, X_test_V)
X_test = np.hstack((X_test_V, X_test_N))

"""
feed batch to model manually cause vector features can be very large
"""
for i in xrange(nb_epoch):
    print ("epoch:%d" % i)
    batch_number = len(X_train_N) / batch_size
    print(batch_number)
    eidx = 0
    loss = 0
    for n in xrange(batch_number):
        if (n+1) * batch_size < len(X_train_N):
            eidx = (n+1) * batch_size
        else:
            eidx = len(X_train_N)
        X_batch_N = X_train_N[n * batch_size: eidx]
        X_batch_V = X_train_V[n * batch_size: eidx]
        X_batch_V = number2vector(
                featnamearray, feattypedict, featdict, X_batch_V)
        X_batch = np.hstack((X_batch_V, X_batch_N))
        Y_batch = Y_train[n * batch_size: eidx]
        lscalar = model.train_on_batch(X_batch, Y_batch)
        loss = loss + lscalar[0]
        if (n+1) % 100 == 0:
            print ("batch: %d loss: %f " % (n+1, loss / 100))
            loss = 0
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

json_string = model.to_json()
open('mlp_architecture.json', 'w').write(json_string)
model.save_weights('mlp_weights.h5', overwrite=True)
